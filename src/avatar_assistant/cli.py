import argparse
import os
import sys

from avatar_assistant.run import run as run_pipeline
from avatar_assistant.evaluate import (
    basic_quality_score,
    evaluate_workflow_a,
)
from avatar_assistant.manifest import append_manifest_entry
from avatar_assistant.workflows.workflow_a import run_workflow_a
from avatar_assistant.logging_utils import get_logger, log_event


def main() -> None:
    lg = get_logger()

    ap = argparse.ArgumentParser(prog="ava")
    sp = ap.add_subparsers(dest="cmd")

    # ----------------------------------------------------
    # Command: ava run --audio ... [--check]
    # ----------------------------------------------------
    pr = sp.add_parser("run", help="run pipeline")
    pr.add_argument("--audio", required=True, help="path to audio or .txt")
    pr.add_argument(
        "--check",
        action="store_true",
        help="score summary quality using a simple heuristic",
    )

    # ----------------------------------------------------
    # Command: ava workflow-a
    # ----------------------------------------------------
    pw = sp.add_parser("workflow-a", help="run retrieval-aware Workflow A")
    pw.add_argument("--topic", required=True, help="topic or prompt for the workflow")
    pw.add_argument(
        "--assets",
        nargs="+",
        required=True,
        help="one or more asset IDs to retrieve from",
    )
    pw.add_argument(
        "--max-chunks",
        type=int,
        default=5,
        help="maximum number of chunks to retrieve",
    )

    # ----------------------------------------------------
    # Command: ava evaluate-workflow-a
    # ----------------------------------------------------
    pe = sp.add_parser(
        "evaluate-workflow-a",
        help="run a simple evaluation for Workflow A and record it to manifest",
    )
    pe.add_argument("--topic", required=True)
    pe.add_argument("--assets", nargs="+", required=True)
    pe.add_argument("--max-chunks", type=int, default=3)

    # ----------------------------------------------------
    # Command: ava gui
    # ----------------------------------------------------
    pg = sp.add_parser("gui", help="launch the web GUI")
    pg.add_argument("--port", type=int, default=8000, help="port to serve on")
    pg.add_argument(
        "--no-open",
        action="store_true",
        help="don't auto-open browser",
    )

    args = ap.parse_args()

    # ----------------------------------------------------
    # Handler: ava run
    # ----------------------------------------------------
    if args.cmd == "run":
        log_event(lg, "pipeline.run.start", audio=args.audio, check=args.check)
        try:
            out = run_pipeline(args.audio)
            if args.check:
                import pathlib

                s = pathlib.Path(out, "summary.md").read_text(encoding="utf-8")
                score = basic_quality_score(s)
                print("quality_score:", score)
                log_event(lg, "pipeline.run.quality_scored", score=score)

            print("OK:", out)
            log_event(lg, "pipeline.run.end", output_dir=out)
            sys.exit(0)
        except Exception as exc:
            log_event(
                lg,
                "pipeline.run.error",
                error=str(exc),
                audio=args.audio,
                check=args.check,
            )
            print(f"Error running pipeline: {exc}", file=sys.stderr)
            sys.exit(1)

    # ----------------------------------------------------
    # Handler: ava workflow-a
    # ----------------------------------------------------
    if args.cmd == "workflow-a":
        log_event(
            lg,
            "workflow_a.start",
            topic=args.topic,
            assets=args.assets,
            max_chunks=args.max_chunks,
        )
        try:
            result = run_workflow_a(
                topic=args.topic,
                asset_ids=args.assets,
                max_chunks=args.max_chunks,
            )

            metrics = result.metadata.get("metrics", {})

            # Human-readable output
            print("=== SUMMARY ===")
            print(result.summary)
            print()
            print("=== OUTLINE ===")
            print(result.outline)
            print()
            print("=== SCRIPTS ===")
            for name, text in result.scripts.items():
                print(f"[{name}]")
                print(text)
                print()

            manifest_entry = {
                "workflow": "workflow_a",
                "topic": result.metadata.get("topic", args.topic),
                "asset_ids": result.metadata.get("asset_ids", args.assets),
                "max_chunks": args.max_chunks,
                "metrics": metrics,
                "retrieved_chunks": result.metadata.get("retrieved_chunks"),
                "used_record_ids": result.metadata.get("used_record_ids", []),
                "workflow_version": result.metadata.get("workflow_version"),
            }
            append_manifest_entry(manifest_entry)

            log_event(
                lg,
                "workflow_a.end",
                elapsed_ms_total=metrics.get("elapsed_ms_total"),
                retrieval_num_chunks=metrics.get("retrieval_num_chunks"),
            )
            sys.exit(0)
        except Exception as exc:
            log_event(
                lg,
                "workflow_a.error",
                error=str(exc),
                topic=args.topic,
                assets=args.assets,
            )
            print(f"Error running workflow-a: {exc}", file=sys.stderr)
            sys.exit(1)

    # ----------------------------------------------------
    # Handler: ava evaluate-workflow-a
    # ----------------------------------------------------
    if args.cmd == "evaluate-workflow-a":
        log_event(
            lg,
            "evaluate_workflow_a.start",
            topic=args.topic,
            assets=args.assets,
            max_chunks=args.max_chunks,
        )
        try:
            eval_result = evaluate_workflow_a(
                topic=args.topic,
                asset_ids=args.assets,
                max_chunks=args.max_chunks,
            )
            log_event(
                lg,
                "evaluate_workflow_a.end",
                topic=args.topic,
                assets=args.assets,
                **eval_result,
            )

            print("=== EVALUATION (Workflow A) ===")
            for k, v in eval_result.items():
                print(f"{k}: {v}")
            sys.exit(0)
        except Exception as exc:
            log_event(
                lg,
                "evaluate_workflow_a.error",
                error=str(exc),
                topic=args.topic,
                assets=args.assets,
            )
            print(f"Error evaluating workflow-a: {exc}", file=sys.stderr)
            sys.exit(1)

    # ----------------------------------------------------
    # Handler: ava gui
    # ----------------------------------------------------
    if args.cmd == "gui":
        import threading
        import time
        import webbrowser

        log_event(lg, "gui.start", port=args.port)
        url = f"http://localhost:{args.port}"

        if not args.no_open:
            def _open_browser():
                time.sleep(1)
                webbrowser.open(url)
            threading.Thread(target=_open_browser, daemon=True).start()

        print(f"Starting Avatar Assistant at {url}")
        print("Press Ctrl+C to stop.")
        try:
            import uvicorn
            uvicorn.run(
                "avatar_assistant.server:app",
                host="127.0.0.1",
                port=args.port,
                log_level="warning",
            )
        except KeyboardInterrupt:
            print("\nStopped.")
        sys.exit(0)

    # ----------------------------------------------------
    # Default: no subcommand → show basic info
    # ----------------------------------------------------
    print("avatar-assistant 0.1.0")
    print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
    sys.exit(0)


if __name__ == "__main__":
    main()
