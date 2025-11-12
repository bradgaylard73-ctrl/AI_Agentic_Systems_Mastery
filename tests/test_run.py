from pathlib import Path
import json, os
from avatar_assistant.run import run
def test_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setenv("AA_DATA_DIR", str(tmp_path/"runs"))
    p = tmp_path/"sample.txt"
    p.write_text("We discussed goals, blockers, next steps. Action: write tasks.")
    out = Path(run(str(p)))
    assert (out/"transcript.txt").exists()
    assert (out/"summary.md").exists()
    m = json.loads((out/"manifest.json").read_text())
    assert m["metrics"]["summary_chars"] > 10
