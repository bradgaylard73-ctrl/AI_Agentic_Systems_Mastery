# src/avatar_assistant/metrics.py
import json, os, sys, time, tempfile, datetime as dt
from typing import Dict, Any

def _utc_now_iso() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, int(len(text) / 4))  # ≈1 token per 4 chars

def build_metrics(*, summary: str, audio_duration_sec: float, run_started_ts: float,
                  model: str | None = None, tokens_in: int | None = None,
                  tokens_out: int | None = None) -> Dict[str, Any]:
    finished = time.time()
    return {
        "summary_length": len(summary.split()) if summary else 0,
        "summary_chars": len(summary) if summary else 0,
        "input_duration_sec": float(audio_duration_sec or 0.0),
        "processing_time_sec": round(finished - run_started_ts, 3),
        "tokens_in": int(tokens_in or 0),
        "tokens_out": int(tokens_out if tokens_out is not None else _estimate_tokens(summary)),
        "model": model or "unknown",
        "run_started_at": dt.datetime.fromtimestamp(run_started_ts, tz=dt.timezone.utc)
                              .isoformat().replace("+00:00","Z"),
        "run_finished_at": _utc_now_iso(),
    }

def write_metrics_into_manifest(manifest_path: str, metrics: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(manifest_path) or ".", exist_ok=True)
    data = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    data["metrics"] = {**data.get("metrics", {}), **metrics}

    d = os.path.dirname(manifest_path) or "."
    with tempfile.NamedTemporaryFile("w", delete=False, dir=d) as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = tmp.name
    os.replace(tmp_path, manifest_path)

    print(json.dumps({"event": "metrics_recorded", "metrics": metrics}), file=sys.stderr)