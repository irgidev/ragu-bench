# ragu-bench

Model-agnostic LLM benchmark and cost-aware routing for Bahasa Indonesia RAG.

## Problem

A team serving a Bahasa Indonesia RAG assistant has to pick models and pay for them without public numbers that compare candidates on the same task set. Vendor claims do not answer the two questions that decide the architecture: how much grounded-answer quality and correct refusal behavior differ across model tiers, and how much money a router saves when a cheap model handles most traffic and escalates only the uncertain queries.

## Approach

- One shared gold set of Bahasa Indonesia questions over the BPJS Kesehatan public-services domain: a 30-item smoke set (`v0`, built in this repo) now, migrating to the `ragu` project's released gold set once available.
- Same harness, same retrieval configuration, same scoring for every candidate: one cheap API model, one stronger API model, one local open-source model via Ollama, and an Indonesian model if access allows.
- Every run records groundedness, correct-refusal behavior, time-to-first-token and total latency, and cost per query from official price pages with the check date.
- Three routing strategies measured on the same items: cheap-always, expensive-always, and a cost-aware router that escalates only on low-confidence signals (a structured self-check plus the retrieval score).

## Results

Nothing has been measured yet. The tables below stay empty until a committed run in `results/` produces real numbers. No placeholder or invented values.

### Leaderboard (per model)

| Model | Gold set | Run date | Endpoint region | Grounded accuracy | Correct-refusal rate | p50 latency | p95 latency | Avg cost/query (USD) | Gold-set total (USD / IDR) |
|---|---|---|---|---|---|---|---|---|---|
| pending first run | | | | | | | | | |

### Routing strategies

| Strategy | Quality | Escalated queries | Avg cost/query (USD) | p50 / p95 latency |
|---|---|---|---|---|
| pending first run | | | | |

## Repository layout

```
src/bench/
  schemas.py    shared data contracts (gold items, run records, evaluation rows)
  models/       OpenAI-compatible model adapters          (model harness stream)
  runner.py     gold-set runner writing results/runs/     (model harness stream)
  metrics/      groundedness, refusal, latency, cost      (metrics+router stream)
  router/       routing policy and strategies             (metrics+router stream)
data/gold/      gold sets (v0 smoke now, ragu v1 later)
results/        committed run JSONs, leaderboard, charts, REPORT.md
tests/          schema, harness, metrics, router tests
prompts/        internal sub-stream briefs
```

## Reproducing

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
ruff check .
pytest -q
```

Model runs additionally need keys in `.env` (copy `.env.example`). CI runs lint and tests only and never needs keys.

## Limitations

- The current gold set is a 30-item smoke set (`v0`). Small sets make per-model differences noisier; conclusions tighten when the `ragu` project's larger gold set lands.
- Latency is measured from one machine at one point in time. Cost uses official price pages at a recorded check date. Both move.
- Scoring method (deterministic heuristics versus LLM judge) is fixed before scoring and documented with every published result.

## Status

Milestone and work-stream ownership are tracked in [STATUS.md](STATUS.md).
