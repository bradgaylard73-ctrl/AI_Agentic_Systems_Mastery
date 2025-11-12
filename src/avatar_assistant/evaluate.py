# src/avatar_assistant/evaluate.py
import json
import math
import re
from pathlib import Path
from typing import Dict, Tuple
from .logging_utils import get_logger, log_event

WORD_RE = re.compile(r"\b[\w'-]+\b", flags=re.UNICODE)

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
    den = math.sqrt(sum(v*v for v in a.values())) * math.sqrt(sum(v*v for v in b.values()))
    return float(num / den) if den else 0.0

def _precision_recall_f1(ref_tokens, cand_tokens) -> Tuple[float, float, float]:
    if not ref_tokens or not cand_tokens:
        return 0.0, 0.0, 0.0
    ref_set = set(ref_tokens)
    cand_set = set(cand_tokens)
    inter = len(ref_set & cand_set)
    p = inter / max(1, len(cand_set))
    r = inter / max(1, len(ref_set))
    f1 = (2*p*r / (p + r)) if (p + r) else 0.0
    return float(p), float(r), float(f1)

def score_summary(reference: str, candidate: str) -> Dict[str, float]:
    """Public API used by evaluate_batch.py. Keep name stable."""
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
    lg = get_logger()
    run = Path(run_dir)
    ref = Path(reference_path)
    cand = (run / "summary.md").read_text(encoding="utf-8")
    reference = ref.read_text(encoding="utf-8")
    scores = score_summary(reference, cand)
    log_event(lg, "evaluation_complete", run=str(run), reference=str(ref), **scores)
    (run / "scores.json").write_text(json.dumps(scores, indent=2), encoding="utf-8")
    return scores

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