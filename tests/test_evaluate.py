# tests/test_evaluate.py
from src.avatar_assistant.evaluate import score_summary

def test_score_summary_basic_overlap():
    ref = "cat sat on the mat"
    cand = "the cat sat on mat"
    s = score_summary(ref, cand)
    assert s["f1"] > 0.5
    assert 0.0 <= s["cosine"] <= 1.0
    assert 0.0 <= s["aggregate"] <= 1.0