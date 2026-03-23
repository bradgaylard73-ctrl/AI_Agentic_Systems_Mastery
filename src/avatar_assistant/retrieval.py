# src/avatar_assistant/retrieval.py
"""Chunk retrieval from JSONL embedding files.

Uses vector cosine similarity when embeddings are available,
falls back to keyword matching otherwise.
"""

import json
import math
import os
import re
from typing import Any, Dict, List, Optional

from .config import EMBEDDING_DIR
from .logging_utils import get_logger, log_event

_WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)


# ── Vector helpers ──────────────────────────────────────


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _embed_query(text: str) -> Optional[List[float]]:
    """Embed a query string via OpenAI. Returns None if unavailable."""
    if os.getenv("AA_OFFLINE") == "1" or not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000],
        )
        return response.data[0].embedding
    except Exception:
        return None


# ── Keyword helpers ─────────────────────────────────────


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _WORD_RE.findall(text or "")]


def _keyword_score(chunk: Dict[str, Any], query_tokens: List[str]) -> float:
    """Score a chunk by keyword overlap with the query."""
    if not query_tokens:
        return 0.0
    query_set = set(query_tokens)
    text_tokens = set(_tokenize(chunk.get("text", "")))
    title_tokens = set(_tokenize(chunk.get("title", "")))
    text_hits = len(query_set & text_tokens)
    title_hits = len(query_set & title_tokens)
    return (text_hits + title_hits * 2) / len(query_set)


# ── Core retrieval ──────────────────────────────────────


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


def retrieve_chunks(
    topic: str,
    asset_ids: List[str],
    max_chunks: int = 5,
) -> List[Dict[str, Any]]:
    """Retrieve the most relevant chunks for a topic from the given assets.

    Uses vector cosine similarity when chunks have embeddings and the API is
    available. Falls back to keyword matching otherwise.
    """
    lg = get_logger()
    chunks = _load_chunks(asset_ids)

    if not chunks:
        log_event(lg, "retrieval.no_chunks", topic=topic, asset_ids=asset_ids)
        return []

    # Check if chunks have vectors and we can embed the query
    has_vectors = any("vector" in c for c in chunks)
    query_vector = _embed_query(topic) if has_vectors else None

    if query_vector and has_vectors:
        mode = "vector"
        scored = []
        for chunk in chunks:
            vec = chunk.get("vector")
            if vec:
                score = _cosine_similarity(query_vector, vec)
            else:
                # Fallback for chunks without vectors in a mixed set
                score = _keyword_score(chunk, _tokenize(topic))
            scored.append({
                **{k: v for k, v in chunk.items() if k != "vector"},
                "_score": round(score, 4),
            })
    else:
        mode = "keyword"
        query_tokens = _tokenize(topic)
        scored = []
        for chunk in chunks:
            score = _keyword_score(chunk, query_tokens)
            scored.append({
                **{k: v for k, v in chunk.items() if k != "vector"},
                "_score": round(score, 4),
            })

    scored.sort(key=lambda c: c["_score"], reverse=True)
    result = scored[:max_chunks]

    log_event(
        lg,
        "retrieval.complete",
        topic=topic,
        mode=mode,
        total_chunks=len(chunks),
        returned=len(result),
    )
    return result
