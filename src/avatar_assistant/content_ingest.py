from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


# Resolve project root: .../AI_Agentic_Systems_Mastery
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONTENT_DIR = PROJECT_ROOT / "content"
SUMMARIES_DIR = PROJECT_ROOT / "summaries"
EMBEDDING_DIR = PROJECT_ROOT / "embedding"


@dataclass
class AssetManifest:
    id: str
    title: str
    category: str
    description: str
    status: str
    source_files: Dict[str, str]
    tags: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AssetManifest":
        return cls(
            id=data["id"],
            title=data["title"],
            category=data.get("category", "uncategorised"),
            description=data.get("description", "").strip(),
            status=data.get("status", "unknown"),
            source_files=data["source_files"],
            tags=data.get("tags", []),
        )


def load_manifest(asset_id: str) -> AssetManifest:
    manifest_path = CONTENT_DIR / asset_id / f"{asset_id}.asset.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found for asset '{asset_id}': {manifest_path}")

    with manifest_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    manifest = AssetManifest.from_dict(data)
    return manifest


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def generate_summary_if_missing(manifest: AssetManifest) -> Path:
    """
    If the summary file does not exist, generate a simple summary by
    extracting the first non-heading paragraph from the research note.
    """
    summary_rel = manifest.source_files.get("summary")
    research_rel = manifest.source_files.get("research_note")

    if not summary_rel:
        raise ValueError(f"Manifest for '{manifest.id}' has no 'summary' path in source_files")

    if not research_rel:
        raise ValueError(f"Manifest for '{manifest.id}' has no 'research_note' path in source_files")

    summary_path = PROJECT_ROOT / summary_rel
    research_path = PROJECT_ROOT / research_rel

    if summary_path.exists():
        return summary_path  # Do not overwrite existing summary

    if not research_path.exists():
        raise FileNotFoundError(
            f"Research note not found for asset '{manifest.id}': {research_path}"
        )

    text = research_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines()]

    # Very simple heuristic: take the first non-empty, non-heading paragraph(s)
    paragraphs: List[str] = []
    current_para: List[str] = []

    def flush_para():
        nonlocal current_para
        if current_para:
            paragraphs.append(" ".join(current_para).strip())
            current_para = []

    for line in lines:
        if not line:
            flush_para()
            continue
        if line.startswith("#"):  # skip headings
            flush_para()
            continue
        current_para.append(line)

    flush_para()

    if not paragraphs:
        # fallback: use first 400 chars of whole file
        summary_text = text.strip()[:400]
    else:
        # Take the first paragraph, truncated if necessary
        summary_text = paragraphs[0]
        if len(summary_text) > 600:
            summary_text = summary_text[:600].rsplit(" ", 1)[0] + "..."

    ensure_parent_dir(summary_path)
    summary_path.write_text(summary_text.strip() + "\n", encoding="utf-8")

    print(f"[ingest] Generated summary for asset '{manifest.id}' at {summary_path}")
    return summary_path


def _get_embedding_vector(text: str):
    """Call OpenAI embeddings API. Returns a list of floats or None on failure."""
    import os
    if os.getenv("AA_OFFLINE") == "1" or not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000],
        )
        return response.data[0].embedding
    except Exception as exc:
        print(f"[ingest] Embedding API failed, storing text only: {exc}")
        return None


def generate_embedding(manifest: AssetManifest) -> Path:
    """
    Generate a JSONL embedding file for the asset.
    Calls OpenAI embeddings API when available, otherwise stores text only.
    """
    embedding_rel = manifest.source_files.get("embedding")
    summary_rel = manifest.source_files.get("summary")

    if not embedding_rel:
        raise ValueError(f"Manifest for '{manifest.id}' has no 'embedding' path in source_files")

    if not summary_rel:
        raise ValueError(f"Manifest for '{manifest.id}' has no 'summary' path in source_files")

    embedding_path = PROJECT_ROOT / embedding_rel
    summary_path = PROJECT_ROOT / summary_rel

    if not summary_path.exists():
        raise FileNotFoundError(
            f"Summary not found for asset '{manifest.id}' at {summary_path}. "
            f"Run generate_summary_if_missing() first."
        )

    summary_text = summary_path.read_text(encoding="utf-8").strip()
    if not summary_text:
        raise ValueError(f"Summary for asset '{manifest.id}' is empty at {summary_path}")

    embed_input = f"{manifest.title}: {summary_text}"
    vector = _get_embedding_vector(embed_input)

    record = {
        "id": f"{manifest.id}_001",
        "asset": manifest.id,
        "type": "research_topic",
        "title": manifest.title,
        "text": summary_text,
    }
    if vector is not None:
        record["vector"] = vector

    ensure_parent_dir(embedding_path)
    with embedding_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    mode = "vector" if vector else "text-only"
    print(f"[ingest] Wrote embedding JSONL ({mode}) for asset '{manifest.id}' to {embedding_path}")
    return embedding_path


def update_index(manifest: AssetManifest) -> Path:
    index_path = CONTENT_DIR / "index.yaml"
    ensure_parent_dir(index_path)

    if index_path.exists():
        with index_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
    else:
        data = []

    if not isinstance(data, list):
        raise ValueError(f"content/index.yaml must be a list of items, got {type(data)}")

    entry = {
        "id": manifest.id,
        "title": manifest.title,
        "category": manifest.category,
        "manifest": f"content/{manifest.id}/{manifest.id}.asset.yaml",
        "summary": manifest.source_files.get("summary"),
        "embedding": manifest.source_files.get("embedding"),
        "status": manifest.status,
    }

    updated = False
    for i, item in enumerate(data):
        if item.get("id") == manifest.id:
            data[i] = entry
            updated = True
            break

    if not updated:
        data.append(entry)

    with index_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    print(f"[ingest] Updated index.yaml for asset '{manifest.id}' at {index_path}")
    return index_path


def ingest_asset(asset_id: str) -> None:
    """
    High-level ingestion pipeline for a single asset:
    - load manifest
    - ensure summary exists
    - generate embedding JSONL
    - update global index
    """
    print(f"[ingest] Starting ingestion for asset: {asset_id!r}")
    manifest = load_manifest(asset_id)

    # Ensure summary
    summary_path = generate_summary_if_missing(manifest)

    # Ensure embedding
    embedding_path = generate_embedding(manifest)

    # Update index
    index_path = update_index(manifest)

    print("[ingest] Completed ingestion.")
    print(f"          summary:   {summary_path}")
    print(f"          embedding: {embedding_path}")
    print(f"          index:     {index_path}")


def main(argv: List[str] | None = None) -> None:
    """
    Entry point so this module can be called as a script, if needed:
    python -m avatar_assistant.content_ingest wallace_line
    """
    import argparse

    parser = argparse.ArgumentParser(description="Ingest a content asset into the system.")
    parser.add_argument("asset_id", help="Asset id (e.g. 'wallace_line')")
    args = parser.parse_args(argv)

    ingest_asset(args.asset_id)


if __name__ == "__main__":
    main()
