# src/avatar_assistant/summarize.py
import os, re

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def _heuristic_summary(text: str, max_words: int = 60) -> str:
    """Offline fallback: join first sentences up to max_words."""
    if not text:
        return ""
    parts = _SENT_SPLIT.split(text.strip())
    words = []
    for sent in parts:
        for w in sent.split():
            if len(words) >= max_words:
                return " ".join(words).strip()
            words.append(w)
        if len(words) >= max_words:
            break
    return " ".join(words).strip()

def summarize(transcript: str, max_words: int = 60) -> str:
    """Returns a short summary. Uses heuristic when offline or no key present."""
    offline = os.getenv("AA_OFFLINE") == "1"
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    if offline or not has_key:
        return _heuristic_summary(transcript, max_words)

    # If you later wire OpenAI, keep it behind this guard:
    # from openai import OpenAI
    # client = OpenAI()
    # ... call the API ...
    # return api_summary
    return _heuristic_summary(transcript, max_words)  # temporary until API wired