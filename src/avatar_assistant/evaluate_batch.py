import json
from pathlib import Path
from .evaluate import score_summary
from .logging_utils import get_logger, log_event
from .summarize import summarize

def evaluate_dir(dev_dir: str, out_path: str, threshold: float = 0.40) -> float:
    lg = get_logger()
    dev = Path(dev_dir)

    stems_txt = {p.stem for p in dev.glob("*.txt")}
    stems_ref = {p.stem.replace(".ref","") for p in dev.glob("*.ref.txt")}
    stems = sorted(stems_txt & stems_ref)
    if not stems:
        raise FileNotFoundError(f"No .txt/.ref.txt pairs in {dev_dir}")

    items, aggregates = [], []
    for s in stems:
        src = dev / f"{s}.txt"
        ref = dev / f"{s}.ref.txt"

        transcript = src.read_text(encoding="utf-8")
        reference = ref.read_text(encoding="utf-8")
        candidate = summarize(transcript)

        scores = score_summary(reference, candidate)
        items.append({"id": s, **scores})
        aggregates.append(scores["aggregate"])
        log_event(lg, "dev_item_scored", id=s, **scores)

    macro = sum(aggregates) / len(aggregates)
    report = {"macro_aggregate": round(macro, 4), "count": len(items), "items": items}
    Path(out_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    log_event(lg, "dev_eval_complete", macro_aggregate=report["macro_aggregate"], count=report["count"])
    return float(macro)

def _main(argv) -> int:
    import sys
    if len(argv) < 3:
        print("usage: python -m src.avatar_assistant.evaluate_batch <dev_dir> <out.json> [threshold]", file=sys.stderr)
        return 2
    dev_dir, out_path = argv[1], argv[2]
    thr = float(argv[3]) if len(argv) > 3 else 0.40
    try:
        macro = evaluate_dir(dev_dir, out_path, thr)
        print(json.dumps({"macro_aggregate": round(macro, 4)}, indent=2))
        return 0 if macro >= thr else 1
    except Exception as e:
        get_logger().error(str(e))
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(_main(sys.argv))
