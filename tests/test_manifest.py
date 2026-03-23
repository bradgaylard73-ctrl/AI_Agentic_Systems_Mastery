import json
from pathlib import Path

import avatar_assistant.manifest as manifest_mod


def test_append_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", tmp_path / "data" / "manifest.json")
    manifest_mod.append_manifest_entry({"workflow": "test", "topic": "hello"})

    path = tmp_path / "data" / "manifest.json"
    assert path.exists()
    entries = json.loads(path.read_text())
    assert len(entries) == 1
    assert entries[0]["workflow"] == "test"
    assert "timestamp" in entries[0]


def test_append_multiple(tmp_path, monkeypatch):
    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", tmp_path / "data" / "manifest.json")
    manifest_mod.append_manifest_entry({"workflow": "a"})
    manifest_mod.append_manifest_entry({"workflow": "b"})

    entries = json.loads((tmp_path / "data" / "manifest.json").read_text())
    assert len(entries) == 2
    assert entries[0]["workflow"] == "a"
    assert entries[1]["workflow"] == "b"


def test_append_recovers_from_corrupt(tmp_path, monkeypatch):
    path = tmp_path / "data" / "manifest.json"
    path.parent.mkdir(parents=True)
    path.write_text("NOT VALID JSON")

    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", path)
    manifest_mod.append_manifest_entry({"workflow": "recovered"})

    entries = json.loads(path.read_text())
    assert len(entries) == 1
    assert entries[0]["workflow"] == "recovered"
