import pytest

from bench.schemas import (
    GoldItem,
    GoldSet,
    GroundingSource,
    ModelAnswer,
    RunRecord,
    SchemaError,
    gold_item_from_dict,
)


def _grounding() -> list[GroundingSource]:
    return [
        GroundingSource(
            url="https://example.go.id/faq",
            accessed="2026-11-15",
            quote="Iuran PBI ditanggung pemerintah.",
        )
    ]


def test_answer_item_requires_grounding():
    with pytest.raises(SchemaError, match="grounding"):
        GoldItem(id="t1", question="Q?", ideal_answer="A", expected_behavior="answer", grounding=[])


def test_refuse_item_requires_reason():
    with pytest.raises(SchemaError, match="refusal_reason"):
        GoldItem(id="t2", question="Q?", ideal_answer="", expected_behavior="refuse")


def test_refuse_item_allows_empty_grounding():
    item = GoldItem(
        id="t3",
        question="Q?",
        ideal_answer="",
        expected_behavior="refuse",
        refusal_reason="outside corpus scope",
    )
    assert item.grounding == []


def test_unknown_item_key_rejected():
    bad = {
        "id": "t4",
        "question": "Q?",
        "ideal_answer": "A",
        "expected_behavior": "answer",
        "grounding": [],
        "typo_key": 1,
    }
    with pytest.raises(SchemaError, match="unknown keys"):
        gold_item_from_dict(bad)


def test_unknown_behavior_rejected():
    with pytest.raises(SchemaError, match="expected_behavior"):
        GoldItem(
            id="t5",
            question="Q?",
            ideal_answer="A",
            expected_behavior="maybe",
            grounding=_grounding(),
        )


def test_gold_set_round_trip(tmp_path):
    gold_set = GoldSet(
        version="v0-test",
        generated_at="2026-11-15",
        description="unit test set",
        items=[
            GoldItem(
                id="a1",
                question="Berapa iuran PBI?",
                ideal_answer="Ditanggung pemerintah.",
                expected_behavior="answer",
                grounding=_grounding(),
                tags=["iuran"],
            ),
            GoldItem(
                id="r1",
                question="Kurs dolar hari ini?",
                ideal_answer="",
                expected_behavior="refuse",
                refusal_reason="outside corpus scope",
            ),
        ],
    )
    path = tmp_path / "gold.json"
    gold_set.save(path)
    loaded = GoldSet.load(path)
    assert loaded == gold_set


def test_duplicate_gold_ids_rejected():
    gold_set = GoldSet(
        version="v0-test",
        generated_at="2026-11-15",
        description="dup",
        items=[
            GoldItem(
                id="a1",
                question="Q1?",
                ideal_answer="A",
                expected_behavior="answer",
                grounding=_grounding(),
            ),
            GoldItem(
                id="a1",
                question="Q2?",
                ideal_answer="A",
                expected_behavior="answer",
                grounding=_grounding(),
            ),
        ],
    )
    with pytest.raises(SchemaError, match="duplicate"):
        gold_set.validate()


def _run_record() -> RunRecord:
    return RunRecord(
        run_id="run-001",
        model="test-model",
        gold_set_version="v0-test",
        endpoint_region="id",
        created_at="2026-11-15T00:00:00Z",
        price_usd_per_1m_input=0.1,
        price_usd_per_1m_output=0.4,
        price_checked_on="2026-11-15",
        config={"temperature": 0},
        answers=[
            ModelAnswer(
                item_id="a1", answer_text="jawaban", refused=False, total_ms=120.5, ttft_ms=40.1
            ),
            ModelAnswer(
                item_id="r1", answer_text="Maaf, di luar cakupan.", refused=True, total_ms=90.0
            ),
        ],
    )


def test_run_record_round_trip(tmp_path):
    run = _run_record()
    path = tmp_path / "run.json"
    run.save(path)
    loaded = RunRecord.load(path)
    assert loaded == run


def test_run_record_duplicate_answers_rejected():
    run = _run_record()
    run.answers.append(ModelAnswer(item_id="a1", answer_text="dup", refused=False, total_ms=1.0))
    with pytest.raises(SchemaError, match="duplicate"):
        run.validate()


def test_run_record_missing_fields_rejected():
    run = _run_record()
    run.run_id = ""
    with pytest.raises(SchemaError, match="missing required fields"):
        run.validate()
