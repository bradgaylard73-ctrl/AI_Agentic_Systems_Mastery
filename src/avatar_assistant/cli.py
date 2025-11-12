import argparse, os, sys
from avatar_assistant.run import run as run_pipeline
from avatar_assistant.evaluate import basic_quality_score

def main():
    ap = argparse.ArgumentParser(prog="ava")
    sp = ap.add_subparsers(dest="cmd")
    pr = sp.add_parser("run", help="run pipeline")
    pr.add_argument("--audio", required=True, help="path to audio or .txt")
    pr.add_argument("--check", action="store_true", help="score summary")
    args = ap.parse_args()

    if args.cmd == "run":
        out = run_pipeline(args.audio)
        if args.check:
            import pathlib
            s = pathlib.Path(out, "summary.md").read_text(encoding="utf-8")
            print("quality_score:", basic_quality_score(s))
        print("OK:", out)
        sys.exit(0)

    print("avatar-assistant 0.1.0")
    print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
    sys.exit(0)

if __name__ == "__main__":
    main()
