import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))
from agent import validate, prep
from retriever import Retriever

def test_retriever_finds_champion_note():
    r = Retriever(["2026-01-01 pricing call", "2026-02-01 champion left the company"])
    assert "champion" in r.search("champion")[0]

def test_guardrail_blocks_promises():
    raw = '{"summary":"x","risks":[],"opportunities":[],"next_actions":["guarantee a refund"],"confidence":0.9}'
    assert validate(raw) == (None, "blocked_language")

def test_guardrail_rejects_bad_json():
    assert validate("not json")[1] == "invalid_json"

def test_fallback_flags_human_review():
    out = prep("ACC-102")
    assert out["needs_human_review"] and out["risks"]
