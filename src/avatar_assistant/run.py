import json, time, os
from pathlib import Path
from .transcribe import transcribe
from .summarize import summarize
from .logging_utils import get_logger

def run(path: str) -> str:
    lg = get_logger()
    t0 = time.time()
    ts = time.strftime("%Y%m%d-%H%M%S")
    out = Path(os.getenv("AA_DATA_DIR", "data/runs")) / ts
    out.mkdir(parents=True, exist_ok=True)
    lg.info("run start: %s -> %s", path, out)

    transcript = transcribe(path)
    (out / "transcript.txt").write_text(transcript, encoding="utf-8")
    lg.info("transcribed chars=%d", len(transcript))

    summary = summarize(transcript)
    (out / "summary.md").write_text(summary, encoding="utf-8")

    metrics = {
        "dur_s": round(time.time() - t0, 3),
        "transcript_chars": len(transcript),
        "summary_chars": len(summary),
    }
    manifest = {
        "input": path,
        "created": ts,
        "artifacts": ["transcript.txt", "summary.md"],
        "metrics": metrics,
        "notes": "Phase-3 hardened loop",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    lg.info("run ok dur_s=%.3f", metrics["dur_s"])
    return str(out)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: python -m avatar_assistant.run <path-to-audio-or-.txt>")
        sys.exit(2)
    print("wrote:", run(sys.argv[1]))
