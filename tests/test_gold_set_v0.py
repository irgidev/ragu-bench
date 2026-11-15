from pathlib import Path

from bench.schemas import GoldSet

GOLD_V0 = Path(__file__).parents[1] / "data" / "gold" / "gold_v0.json"


def test_gold_v0_loads_and_has_30_items():
    gold_set = GoldSet.load(GOLD_V0)
    assert gold_set.version == "v0-smoke"
    assert len(gold_set.items) == 30


def test_gold_v0_behavior_mix():
    gold_set = GoldSet.load(GOLD_V0)
    answers = [i for i in gold_set.items if i.expected_behavior == "answer"]
    refuses = [i for i in gold_set.items if i.expected_behavior == "refuse"]
    assert len(answers) == 24
    assert len(refuses) == 6
    assert all(i.refusal_reason for i in refuses)


def test_gold_v0_grounding_has_provenance():
    gold_set = GoldSet.load(GOLD_V0)
    for item in gold_set.items:
        if item.expected_behavior != "answer":
            continue
        assert item.grounding, item.id
        for source in item.grounding:
            assert source.accessed == "2026-11-15", item.id
            assert (
                "bpjs-kesehatan.go.id" in source.url or "wikisource.org" in source.url
            ), item.id
            assert len(source.quote) > 10, item.id


def test_gold_v0_ids_unique_and_prefixed():
    gold_set = GoldSet.load(GOLD_V0)
    gold_set.validate()
    assert all(item.id.startswith("v0-") for item in gold_set.items)
