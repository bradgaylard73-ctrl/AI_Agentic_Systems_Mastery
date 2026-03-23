# src/avatar_assistant/workflows/workflow_a.py
"""Workflow A: retrieval-aware content generation."""

import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

from ..config import OPENAI_API_KEY
from ..logging_utils import get_logger, log_event
from ..metrics import _utc_now_iso
from ..retrieval import retrieve_chunks

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORKFLOW_VERSION = "0.1.0"


@dataclass
class WorkflowResult:
    summary: str
    outline: str
    scripts: Dict[str, str]
    metadata: Dict[str, Any] = field(default_factory=dict)


def _build_context(chunks: List[Dict[str, Any]]) -> str:
    """Build a context string from retrieved chunks."""
    parts = []
    for chunk in chunks:
        title = chunk.get("title", "Untitled")
        text = chunk.get("text", "")
        parts.append(f"{title}: {text}")
    return "\n\n".join(parts)


def _heuristic_summary(topic: str, context: str) -> str:
    """Generate a summary from context using heuristic extraction."""
    sentences = _SENT_SPLIT.split(context.strip())
    # Include enough sentences to exceed 50 words
    result_parts = [f"Summary on \"{topic}\":"]
    word_count = len(result_parts[0].split())
    for sent in sentences:
        result_parts.append(sent.strip())
        word_count += len(sent.split())
        if word_count >= 80:
            break
    # If still short, pad with the full context
    if word_count < 50:
        result_parts.append(context)
    return " ".join(result_parts)


def _heuristic_outline(topic: str, chunks: List[Dict[str, Any]]) -> str:
    """Generate a bullet-point outline from chunk titles and content."""
    lines = [f"Outline: {topic}", ""]
    for i, chunk in enumerate(chunks, 1):
        title = chunk.get("title", "Untitled")
        text = chunk.get("text", "")
        first_sent = _SENT_SPLIT.split(text.strip())[0] if text else ""
        lines.append(f"{i}. {title}")
        if first_sent:
            lines.append(f"   - {first_sent}")
    return "\n".join(lines)


def _heuristic_scripts(topic: str, summary: str) -> Dict[str, str]:
    """Generate a simple intro script from the summary."""
    return {
        "intro": (
            f"Welcome to this exploration of {topic}. "
            f"{summary} "
            f"Let's dive deeper into these ideas."
        ),
    }


def _api_generate(topic: str, context: str) -> Dict[str, str]:
    """Use OpenAI API to generate summary, outline, and scripts."""
    from openai import OpenAI

    client = OpenAI()
    prompt = (
        f"You are a content generation assistant. Given the topic and context below, "
        f"produce a JSON object with three keys:\n"
        f"- \"summary\": a 100-200 word summary\n"
        f"- \"outline\": a structured outline with numbered sections\n"
        f"- \"scripts\": an object mapping script names to script text "
        f"(at least an \"intro\" script)\n\n"
        f"Topic: {topic}\n\n"
        f"Context:\n{context[:6000]}\n\n"
        f"Respond with valid JSON only."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You produce structured content in JSON format."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```\w*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    return json.loads(raw)


def run_workflow_a(
    topic: str,
    asset_ids: List[str],
    max_chunks: int = 5,
) -> WorkflowResult:
    """Run Workflow A: retrieve → generate → return structured result."""
    lg = get_logger()
    start_ts = time.time()

    log_event(lg, "workflow_a.start", topic=topic, asset_ids=asset_ids, max_chunks=max_chunks)

    # 1. Retrieve
    chunks = retrieve_chunks(topic, asset_ids, max_chunks)
    context = _build_context(chunks) if chunks else f"No context available for topic: {topic}"
    used_record_ids = [c.get("id", "") for c in chunks]

    # 2. Generate
    offline = os.getenv("AA_OFFLINE") == "1"
    has_key = bool(OPENAI_API_KEY)
    mode = "heuristic"

    if not offline and has_key:
        try:
            parsed = _api_generate(topic, context)
            summary = parsed.get("summary", "")
            outline = parsed.get("outline", "")
            scripts_raw = parsed.get("scripts", {})
            scripts = {str(k): str(v) for k, v in scripts_raw.items()} if isinstance(scripts_raw, dict) else {}
            mode = "api"
        except Exception as exc:
            log_event(lg, "workflow_a.api_fallback", error=str(exc))
            summary = _heuristic_summary(topic, context)
            outline = _heuristic_outline(topic, chunks)
            scripts = _heuristic_scripts(topic, summary)
    else:
        summary = _heuristic_summary(topic, context)
        outline = _heuristic_outline(topic, chunks)
        scripts = _heuristic_scripts(topic, summary)

    # 3. Build metadata
    elapsed_ms = round((time.time() - start_ts) * 1000)
    metrics = {
        "elapsed_ms_total": elapsed_ms,
        "retrieval_num_chunks": len(chunks),
        "mode": mode,
        "timestamp": _utc_now_iso(),
    }

    metadata = {
        "metrics": metrics,
        "topic": topic,
        "asset_ids": list(asset_ids),
        "retrieved_chunks": len(chunks),
        "used_record_ids": used_record_ids,
        "workflow_version": WORKFLOW_VERSION,
    }

    log_event(
        lg,
        "workflow_a.complete",
        elapsed_ms=elapsed_ms,
        mode=mode,
        num_chunks=len(chunks),
    )

    return WorkflowResult(
        summary=summary,
        outline=outline,
        scripts=scripts,
        metadata=metadata,
    )
