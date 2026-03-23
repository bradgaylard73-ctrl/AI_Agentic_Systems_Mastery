# src/avatar_assistant/retrieval.py
"""Keyword-based chunk retrieval from JSONL embedding files."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from .config import EMBEDDING_DIR
from .logging_utils import get_logger, log_event

_WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _WORD_RE.findall(text or "")]


def _load_chunks(asset_ids: List[str]) -> List[Dict[str, Any]]:
    """Load all JSONL records for the given asset IDs."""
    lg = get_logger()
    chunks: List[Dict[str, Any]] = []
    for aid in asset_ids:
        path = EMBEDDING_DIR / f"{aid}.jsonl"
        if not path.exists():
            log_event(lg, "retrieval.asset_missing", asset_id=aid, path=str(path))
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    chunks.append(json.loads(line))
                except json.JSONDecodeError:
                    log_event(lg, "retrieval.parse_error", asset_id=aid)
    return chunks


def _score_chunk(chunk: Dict[str, Any], query_tokens: List[str]) -> float:
    """Score a chunk by keyword overlap with the query."""
    if not query_tokens:
        return 0.0

    query_set = set(query_tokens)
    text_tokens = set(_tokenize(chunk.get("text", "")))
    title_tokens = set(_tokenize(chunk.get("title", "")))

    # Title matches count double
    text_hits = len(query_set & text_tokens)
    title_hits = len(query_set & title_tokens)

    return (text_hits + title_hits * 2) / len(query_set)


def retrieve_chunks(
    topic: str,
    asset_ids: List[str],
    max_chunks: int = 5,
) -> List[Dict[str, Any]]:
    """Retrieve the most relevant chunks for a topic from the given assets."""
    lg = get_logger()
    query_tokens = _tokenize(topic)
    chunks = _load_chunks(asset_ids)

    if not chunks:
        log_event(lg, "retrieval.no_chunks", topic=topic, asset_ids=asset_ids)
        return []

    scored = []
    for chunk in chunks:
        score = _score_chunk(chunk, query_tokens)
        scored.append({**chunk, "_score": round(score, 4)})

    scored.sort(key=lambda c: c["_score"], reverse=True)
    result = scored[:max_chunks]

    log_event(
        lg,
        "retrieval.complete",
        topic=topic,
        total_chunks=len(chunks),
        returned=len(result),
    )
    return result
