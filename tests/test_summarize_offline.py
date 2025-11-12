import os
from src.avatar_assistant.summarize import summarize

def test_offline_heuristic_path(monkeypatch):
    monkeypatch.setenv("AA_OFFLINE", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text = "Alpha. Beta gamma delta? Epsilon!"
    out = summarize(text, max_words=5)
    assert isinstance(out, str)
    assert len(out.split()) <= 5