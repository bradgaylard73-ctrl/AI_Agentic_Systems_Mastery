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


def test_retrieve_with_vectors(tmp_path, monkeypatch):
    """When chunks have vectors and query can be embedded, use cosine similarity."""
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)

    # Chunks with mock vectors: [1,0,0] is "close" to query [0.9,0.1,0], [0,0,1] is far
    _write_jsonl(
        tmp_path / "vec_test.jsonl",
        [
            {"id": "v1", "asset": "vec_test", "title": "Close", "text": "close match", "vector": [1.0, 0.0, 0.0]},
            {"id": "v2", "asset": "vec_test", "title": "Far", "text": "far away", "vector": [0.0, 0.0, 1.0]},
        ],
    )

    # Mock _embed_query to return a vector close to v1
    monkeypatch.setattr(retrieval_mod, "_embed_query", lambda t: [0.9, 0.1, 0.0])

    results = retrieval_mod.retrieve_chunks("anything", ["vec_test"], max_chunks=2)
    assert len(results) == 2
    assert results[0]["id"] == "v1"
    assert results[0]["_score"] > results[1]["_score"]
    # Vectors should be stripped from results
    assert "vector" not in results[0]


def test_retrieve_vector_fallback_to_keyword(tmp_path, monkeypatch):
    """When chunks have vectors but API is unavailable, fall back to keywords."""
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)
    monkeypatch.setenv("AA_OFFLINE", "1")

    _write_jsonl(
        tmp_path / "mixed.jsonl",
        [
            {"id": "m1", "asset": "mixed", "title": "Dogs", "text": "dogs are great", "vector": [1.0, 0.0]},
            {"id": "m2", "asset": "mixed", "title": "Cats", "text": "cats are independent", "vector": [0.0, 1.0]},
        ],
    )

    results = retrieval_mod.retrieve_chunks("dogs great", ["mixed"], max_chunks=2)
    assert len(results) == 2
    # Keyword match should rank dogs first
    assert results[0]["id"] == "m1"
