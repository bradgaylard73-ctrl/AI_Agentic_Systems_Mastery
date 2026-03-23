import json
import os
from pathlib import Path

import avatar_assistant.retrieval as retrieval_mod
from avatar_assistant.workflows.workflow_a import WorkflowResult, run_workflow_a


def _write_jsonl(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def test_run_workflow_a_offline(tmp_path, monkeypatch):
    monkeypatch.setattr(retrieval_mod, "EMBEDDING_DIR", tmp_path)
    monkeypatch.setenv("AA_OFFLINE", "1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    _write_jsonl(
        tmp_path / "topic_a.jsonl",
        [
            {
                "id": "topic_a_001",
                "asset": "topic_a",
                "title": "Nature and Conservation",
                "text": (
                    "Conservation biology is a discipline that studies the preservation "
                    "of biodiversity. It involves understanding ecosystems, species "
                    "interactions, and the impact of human activities on natural habitats. "
                    "Protected areas serve as refuges for endangered species and help "
                    "maintain ecological balance across landscapes."
                ),
            },
            {
                "id": "topic_a_002",
                "asset": "topic_a",
                "title": "Wildlife Migration Patterns",
                "text": (
                    "Many animal species migrate seasonally to find food, breeding "
                    "grounds, or more favorable climates. Migration routes can span "
                    "thousands of kilometers across continents and oceans. Understanding "
                    "these patterns is crucial for wildlife conservation efforts."
                ),
            },
        ],
    )

    result = run_workflow_a(
        topic="nature conservation wildlife",
        asset_ids=["topic_a"],
        max_chunks=3,
    )

    # Structural checks
    assert isinstance(result, WorkflowResult)
    assert isinstance(result.summary, str)
    assert isinstance(result.outline, str)
    assert isinstance(result.scripts, dict)
    assert isinstance(result.metadata, dict)

    # Summary must exceed 50 words (evaluate_workflow_a checks this)
    assert len(result.summary.split()) >= 50

    # Scripts must have at least one entry
    assert len(result.scripts) >= 1

    # Metadata keys
    assert result.metadata["topic"] == "nature conservation wildlife"
    assert result.metadata["workflow_version"] == "0.1.0"
    assert isinstance(result.metadata["metrics"]["retrieval_num_chunks"], int)
    assert isinstance(result.metadata["metrics"]["elapsed_ms_total"], int)
    assert result.metadata["metrics"]["mode"] == "heuristic"
    assert isinstance(result.metadata["used_record_ids"], list)


def test_workflow_result_dataclass():
    r = WorkflowResult(
        summary="test summary",
        outline="test outline",
        scripts={"intro": "hello"},
        metadata={"topic": "test"},
    )
    assert r.summary == "test summary"
    assert r.scripts["intro"] == "hello"
    assert r.metadata["topic"] == "test"
