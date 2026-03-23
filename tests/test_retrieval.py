import json
from pathlib import Path

import avatar_assistant.retrieval as retrieval_mod


def _write_jsonl(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def test_retrieve_chunks_basic(tmp_path, monkeypatch):
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)

    _write_jsonl(
        tmp_path / "animals.jsonl",
        [
            {"id": "animals_001", "asset": "animals", "title": "Dogs and Cats", "text": "Dogs are loyal pets and cats are independent animals."},
            {"id": "animals_002", "asset": "animals", "title": "Fish", "text": "Fish live in water and come in many colours."},
            {"id": "animals_003", "asset": "animals", "title": "Birds and Flight", "text": "Birds can fly using their wings and feathers."},
        ],
    )

    results = retrieval_mod.retrieve_chunks("dogs loyal pets", ["animals"], max_chunks=2)
    assert len(results) == 2
    # The dogs chunk should score highest
    assert results[0]["id"] == "animals_001"
    assert "_score" in results[0]
    assert results[0]["_score"] >= results[1]["_score"]


def test_retrieve_missing_asset(tmp_path, monkeypatch):
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)
    results = retrieval_mod.retrieve_chunks("anything", ["nonexistent"], max_chunks=5)
    assert results == []


def test_retrieve_empty_topic(tmp_path, monkeypatch):
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)
    _write_jsonl(
        tmp_path / "test.jsonl",
        [{"id": "t1", "asset": "test", "title": "Hello", "text": "World"}],
    )
    results = retrieval_mod.retrieve_chunks("", ["test"], max_chunks=5)
    assert len(results) == 1
    assert results[0]["_score"] == 0.0
