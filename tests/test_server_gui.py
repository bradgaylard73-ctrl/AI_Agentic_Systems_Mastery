import json
import os
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

import avatar_assistant.retrieval as retrieval_mod
import avatar_assistant.manifest as manifest_mod
from avatar_assistant.server import app

client = TestClient(app)


def test_index_returns_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "Avatar Assistant" in r.text
    assert "text/html" in r.headers["content-type"]


def test_list_assets():
    r = client.get("/api/assets")
    assert r.status_code == 200
    assets = r.json()
    assert isinstance(assets, list)
    if assets:
        assert "id" in assets[0]
        assert "title" in assets[0]
        assert "category" in assets[0]


def test_run_text():
    r = client.post("/run/text", json={"text": "Hello world. This is a test."})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "transcript" in data
    assert "summary" in data
    assert "quality_score" in data


def test_workflow_a_api(tmp_path, monkeypatch):
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)
    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", tmp_path / "data" / "manifest.json")
    monkeypatch.setenv("AA_OFFLINE", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Write sample embedding
    jsonl_path = tmp_path / "test_asset.jsonl"
    record = {
        "id": "test_001",
        "asset": "test_asset",
        "title": "Test Topic",
        "text": "This is a test chunk with enough words to produce a reasonable summary for the workflow output.",
    }
    jsonl_path.write_text(json.dumps(record) + "\n")

    r = client.post("/api/workflow-a", json={
        "topic": "test topic",
        "asset_ids": ["test_asset"],
        "max_chunks": 3,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "summary" in data
    assert "outline" in data
    assert "scripts" in data
    assert "metadata" in data


def test_evaluate_api(tmp_path, monkeypatch):
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)
    monkeypatch.setattr(manifest_mod, "MANIFEST_PATH", tmp_path / "data" / "manifest.json")
    monkeypatch.setenv("AA_OFFLINE", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    jsonl_path = tmp_path / "test_asset.jsonl"
    record = {
        "id": "test_001",
        "asset": "test_asset",
        "title": "Test Topic",
        "text": "This is a test chunk with enough words to produce a reasonable summary for evaluation purposes.",
    }
    jsonl_path.write_text(json.dumps(record) + "\n")

    r = client.post("/api/evaluate", json={
        "topic": "test topic",
        "asset_ids": ["test_asset"],
        "max_chunks": 2,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "summary_word_count" in data
    assert "num_scripts" in data
