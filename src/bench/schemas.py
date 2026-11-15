"""Shared data contracts for ragu-bench.

Artifacts that cross work-stream boundaries are defined here:

- ``GoldSet``/``GoldItem``/``GroundingSource``: benchmark items with grounding.
  Built by the parent P1 session (smoke set v0) and later migrated to the
  ``ragu`` project's released gold set.
- ``ModelAnswer``/``RunRecord``: what the model harness writes per run.
- ``ItemEvaluation``/``StrategyReportRow``: what metrics and the router
  analysis produce.

Stream-specific code may subclass or extend these, but must not redefine the
fields incompatibly. Schema changes are proposed in ``STATUS.md`` and
integrated by the parent P1 session.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

ExpectedBehavior = Literal["answer", "refuse"]
BehaviorValues = ("answer", "refuse")
StrategyName = Literal["cheap_always", "expensive_always", "router"]


class SchemaError(ValueError):
    """Raised when an artifact does not satisfy the shared schema."""


@dataclass
class GroundingSource:
    """An authoritative snippet that an ``answer`` item must be grounded in."""

    url: str
    accessed: str  # ISO date of retrieval, e.g. "2026-11-15"
    quote: str


@dataclass
class GoldItem:
    """One benchmark question and what correct model behavior looks like."""

    id: str
    question: str
    ideal_answer: str
    expected_behavior: ExpectedBehavior
    grounding: list[GroundingSource] = field(default_factory=list)
    refusal_reason: str | None = None
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.expected_behavior not in BehaviorValues:
            raise SchemaError(f"{self.id}: unknown expected_behavior {self.expected_behavior!r}")
        if self.expected_behavior == "answer" and not self.grounding:
            raise SchemaError(f"{self.id}: 'answer' items require at least one grounding source")
        if self.expected_behavior == "refuse" and not self.refusal_reason:
            raise SchemaError(f"{self.id}: 'refuse' items require refusal_reason")


@dataclass
class GoldSet:
    """A versioned collection of gold items plus its provenance metadata."""

    version: str
    generated_at: str  # ISO date
    description: str
    items: list[GoldItem]

    def validate(self) -> None:
        if not self.version:
            raise SchemaError("gold set requires a version string")
        ids = [item.id for item in self.items]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            raise SchemaError(f"duplicate gold item ids: {duplicates}")

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(asdict(self), ensure_ascii=False, indent=2) + "\n"
        Path(path).write_text(payload, encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> GoldSet:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        try:
            gold_set = cls(
                version=raw["version"],
                generated_at=raw["generated_at"],
                description=raw["description"],
                items=[gold_item_from_dict(d) for d in raw["items"]],
            )
        except KeyError as exc:
            raise SchemaError(f"gold set JSON missing key {exc}") from exc
        gold_set.validate()
        return gold_set


_GOLD_ITEM_KEYS = {
    "id",
    "question",
    "ideal_answer",
    "expected_behavior",
    "grounding",
    "refusal_reason",
    "tags",
}


def gold_item_from_dict(raw_item: dict[str, Any]) -> GoldItem:
    """Build a :class:`GoldItem` from its serialized form, rejecting unknown keys."""
    unknown = set(raw_item) - _GOLD_ITEM_KEYS
    if unknown:
        raise SchemaError(f"gold item {raw_item.get('id', '?')}: unknown keys {sorted(unknown)}")
    try:
        return GoldItem(
            id=raw_item["id"],
            question=raw_item["question"],
            ideal_answer=raw_item["ideal_answer"],
            expected_behavior=raw_item["expected_behavior"],
            grounding=[grounding_from_dict(g) for g in raw_item.get("grounding", [])],
            refusal_reason=raw_item.get("refusal_reason"),
            tags=list(raw_item.get("tags", [])),
        )
    except KeyError as exc:
        raise SchemaError(f"gold item {raw_item.get('id', '?')}: missing key {exc}") from exc


def grounding_from_dict(raw_grounding: dict[str, Any]) -> GroundingSource:
    unknown = set(raw_grounding) - {"url", "accessed", "quote"}
    if unknown:
        raise SchemaError(f"grounding entry: unknown keys {sorted(unknown)}")
    try:
        return GroundingSource(
            url=raw_grounding["url"],
            accessed=raw_grounding["accessed"],
            quote=raw_grounding["quote"],
        )
    except KeyError as exc:
        raise SchemaError(f"grounding entry: missing key {exc}") from exc


@dataclass
class ModelAnswer:
    """One gold item answered by one model within one run."""

    item_id: str
    answer_text: str
    refused: bool
    total_ms: float
    ttft_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    error: str | None = None  # non-None when the model call itself failed


@dataclass
class RunRecord:
    """The full record of one model evaluated against one gold set."""

    run_id: str
    model: str
    gold_set_version: str
    endpoint_region: str
    created_at: str  # ISO datetime
    price_usd_per_1m_input: float | None = None
    price_usd_per_1m_output: float | None = None
    price_checked_on: str | None = None  # ISO date the official price page was verified
    config: dict[str, Any] = field(default_factory=dict)
    answers: list[ModelAnswer] = field(default_factory=list)

    def validate(self) -> None:
        missing = [
            key
            for key in ("run_id", "model", "gold_set_version", "endpoint_region", "created_at")
            if not getattr(self, key)
        ]
        if missing:
            raise SchemaError(f"run record missing required fields: {missing}")
        item_ids = [answer.item_id for answer in self.answers]
        if len(item_ids) != len(set(item_ids)):
            raise SchemaError(f"run {self.run_id}: duplicate answer item_ids")

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(asdict(self), ensure_ascii=False, indent=2) + "\n"
        Path(path).write_text(payload, encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> RunRecord:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        try:
            run_record = cls(
                run_id=raw["run_id"],
                model=raw["model"],
                gold_set_version=raw["gold_set_version"],
                endpoint_region=raw["endpoint_region"],
                created_at=raw["created_at"],
                price_usd_per_1m_input=raw.get("price_usd_per_1m_input"),
                price_usd_per_1m_output=raw.get("price_usd_per_1m_output"),
                price_checked_on=raw.get("price_checked_on"),
                config=dict(raw.get("config", {})),
                answers=[
                    ModelAnswer(
                        item_id=a["item_id"],
                        answer_text=a["answer_text"],
                        refused=a["refused"],
                        total_ms=a["total_ms"],
                        ttft_ms=a.get("ttft_ms"),
                        input_tokens=a.get("input_tokens"),
                        output_tokens=a.get("output_tokens"),
                        error=a.get("error"),
                    )
                    for a in raw.get("answers", [])
                ],
            )
        except KeyError as exc:
            raise SchemaError(f"run record JSON missing key {exc}") from exc
        run_record.validate()
        return run_record


@dataclass
class ItemEvaluation:
    """Metric verdict for one item in one run; produced by ``bench.metrics``."""

    item_id: str
    gold_expected: ExpectedBehavior
    groundedness: float | None = None  # 0..1; None when nothing answerable was produced
    refusal_correct: bool | None = None  # None when the gold item expects an answer
    notes: str | None = None


@dataclass
class StrategyReportRow:
    """One aggregate row of the routing strategy comparison table."""

    strategy: StrategyName
    quality: float
    escalated_pct: float | None  # router strategy only
    avg_cost_usd: float
    p50_latency_ms: float
    p95_latency_ms: float
