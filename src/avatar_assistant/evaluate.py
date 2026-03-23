# src/avatar_assistant/evaluate.py

import json
import math
import re
from pathlib import Path
from typing import Any, Dict, Sequence, Tuple

from .logging_utils import get_logger, log_event

WORD_RE = re.compile(r"\b[\w'-]+\b", flags=re.UNICODE)


# ------------------------------------------------------------
# Token helpers
# ------------------------------------------------------------

def _tokens(text: str):
    return [t.lower() for t in WORD_RE.findall(text or "")]


def _counts(tokens):
    d: Dict[str, int] = {}
    for t in tokens:
        d[t] = d.get(t, 0) + 1
    return d


def _cosine(a: Dict[str, int], b: Dict[str, int]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    num = sum(a[t] * b[t] for t in common)
    den = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return float(num / den) if den else 0.0


def _precision_recall_f1(ref_tokens, cand_tokens) -> Tuple[float, float, float]:
    if not ref_tokens or not cand_tokens:
        return 0.0, 0.0, 0.0
    ref_set = set(ref_tokens)
    cand_set = set(cand_tokens)
    inter = len(ref_set & cand_set)
    p = inter / max(1, len(cand_set))
    r = inter / max(1, len(ref_set))
    f1 = (2 * p * r / (p + r)) if (p + r) else 0.0
    return float(p), float(r), float(f1)


# ------------------------------------------------------------
# Existing public API — DO NOT BREAK
# ------------------------------------------------------------

def score_summary(reference: str, candidate: str) -> Dict[str, float]:
    """
    Public API used by evaluate_batch.py. Must remain stable.
    """
    ref_t = _tokens(reference)
    cand_t = _tokens(candidate)

    p, r, f1 = _precision_recall_f1(ref_t, cand_t)
    cos = _cosine(_counts(ref_t), _counts(cand_t))
    agg = (f1 + cos) / 2.0

    return {
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1": round(f1, 4),
        "cosine": round(cos, 4),
        "aggregate": round(agg, 4),
    }


def evaluate_run(run_dir: str, reference_path: str) -> Dict[str, float]:
    """
    Existing evaluation: compare summary.md in run_dir to a reference text file.
    """
    lg = get_logger()
    run = Path(run_dir)
    ref = Path(reference_path)

    cand = (run / "summary.md").read_text(encoding="utf-8")
    reference = ref.read_text(encoding="utf-8")

    scores = score_summary(reference, cand)
    log_event(lg, "evaluation_complete", run=str(run), reference=str(ref), **scores)

    (run / "scores.json").write_text(json.dumps(scores, indent=2), encoding="utf-8")
    return scores


# ------------------------------------------------------------
# NEW: Needed by cli.py → basic_quality_score
# ------------------------------------------------------------

def basic_quality_score(text: str) -> float:
    """
    Very simple heuristic quality score used by 'ava run --check'.
    Returns float in [0,1].
    """
    tokens = _tokens(text)
    num_words = len(tokens)
    if num_words == 0:
        return 0.0

    # 0 at 0 words, 1 at 300+ words
    length_factor = min(num_words / 300.0, 1.0)

    # Structure bonus
    structure_bonus = 0.0
    if "." in text or "?" in text or "!" in text:
        structure_bonus += 0.1
    if "\n\n" in text:
        structure_bonus += 0.1

    score = length_factor + structure_bonus
    return max(0.0, min(score, 1.0))


# ------------------------------------------------------------
# NEW: Workflow A evaluator
# ------------------------------------------------------------

from avatar_assistant.workflows.workflow_a import run_workflow_a
from avatar_assistant.manifest import append_manifest_entry


def evaluate_workflow_a(
    topic: str,
    asset_ids: Sequence[str],
    max_chunks: int = 3,
) -> Dict[str, Any]:
    """
    Minimal evaluator for Workflow A.
    - Runs Workflow A once.
    - Computes simple heuristic metrics.
    - Writes an evaluation entry to manifest.json.
    """
    result = run_workflow_a(topic=topic, asset_ids=list(asset_ids), max_chunks=max_chunks)

    summary = result.summary or ""
    summary_word_count = len(summary.split())

    try:
        num_scripts = len(result.scripts)
    except Exception:
        num_scripts = 0

    retrieval_metrics = result.metadata.get("metrics", {})
    retrieval_num_chunks = retrieval_metrics.get("retrieval_num_chunks")

    evaluation = {
        "summary_word_count": summary_word_count,
        "num_scripts": num_scripts,
        "retrieval_num_chunks": retrieval_num_chunks,
        "summary_too_short": summary_word_count < 50,
    }

    entry = {
        "workflow": "workflow_a",
        "topic": topic,
        "assets": list(asset_ids),
        "max_chunks": max_chunks,
        "type": "evaluation",
        "evaluation": evaluation,
    }
    append_manifest_entry(entry)

    return evaluation


# ------------------------------------------------------------
# Existing CLI entrypoint (unchanged)
# ------------------------------------------------------------

def _main(argv) -> int:
    import sys
    if len(argv) < 3:
        print("usage: python -m src.avatar_assistant.evaluate <run_dir> <reference.txt>", file=sys.stderr)
        return 2
    run_dir, reference = argv[1], argv[2]
    try:
        scores = evaluate_run(run_dir, reference)
        print(json.dumps(scores, indent=2))
        return 0
    except FileNotFoundError as e:
        get_logger().error(str(e))
        return 2
    except Exception as e:
        get_logger().error(str(e))
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(_main(sys.argv))
