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

    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Summarize the following text in at most {max_words} words. Be concise and preserve key information."},
                {"role": "user", "content": transcript[:8000]},
            ],
            max_tokens=max(200, max_words * 2),
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _heuristic_summary(transcript, max_words)