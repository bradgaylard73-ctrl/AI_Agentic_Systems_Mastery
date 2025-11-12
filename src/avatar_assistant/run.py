# src/avatar_assistant/run.py
import json, os, sys, time
from pathlib import Path

from .transcribe import transcribe
from .summarize import summarize
from .logging_utils import get_logger, log_event
from .metrics import build_metrics, write_metrics_into_manifest

# Exit codes
EXIT_OK = 0
EXIT_INPUT_ERROR = 2
EXIT_RUNTIME_ERROR = 1

def run(path: str) -> str:
    lg = get_logger()
    run_started_ts = time.time()

    ts = time.strftime("%Y%m%d-%H%M%S")
    out_root = Path(os.getenv("AA_DATA_DIR", "data/runs"))
    out = out_root / ts
    out.mkdir(parents=True, exist_ok=True)

    log_event(lg, "run_start", input=path, out=str(out))

    # Validate input early
    p = Path(path)
    if not p.exists() or not p.is_file():
        log_event(lg, "input_not_found", path=path)
        raise FileNotFoundError(f"input not found: {path}")

    # 1) Transcribe
    transcript = transcribe(path)
    (out / "transcript.txt").write_text(transcript, encoding="utf-8")
    log_event(lg, "transcription_complete", transcript_chars=len(transcript))

    # 2) Summarize
    summary = summarize(transcript)
    (out / "summary.md").write_text(summary, encoding="utf-8")
    log_event(lg, "summary_complete", summary_chars=len(summary), summary_length=len(summary.split()) if summary else 0)

    # 3) Metrics
    audio_duration_sec = 0.0  # wire real duration later
    metrics = build_metrics(
        summary=summary,
        audio_duration_sec=audio_duration_sec,
        run_started_ts=run_started_ts,
        model=None,
        tokens_in=None,
        tokens_out=None,
    )
    metrics["transcript_chars"] = len(transcript)

    # 4) Manifest
    manifest_path = str(out / "manifest.json")
    manifest = {
        "input": path,
        "created": ts,
        "artifacts": ["transcript.txt", "summary.md"],
        "notes": "Phase-3 hardened loop",
    }
    Path(manifest_path).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_metrics_into_manifest(manifest_path, metrics)
    log_event(lg, "metrics_recorded", **metrics)

    log_event(lg, "run_complete", out=str(out))
    return str(out)

def _main(argv) -> int:
    if len(argv) < 2:
        print("usage: python -m src.avatar_assistant.run <path-to-audio-or-.txt>", file=sys.stderr)
        return EXIT_INPUT_ERROR
    path = argv[1]
    try:
        run_dir = run(path)
        print("wrote:", run_dir)
        return EXIT_OK
    except FileNotFoundError as e:
        get_logger().error(str(e))
        return EXIT_INPUT_ERROR
    except SystemExit as e:
        # re-raise explicit exits
        raise e
    except Exception as e:
        get_logger().error(str(e))
        return EXIT_RUNTIME_ERROR

if __name__ == "__main__":
    sys.exit(_main(sys.argv))