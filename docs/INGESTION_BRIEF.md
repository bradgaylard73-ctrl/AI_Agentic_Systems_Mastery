# Avatar Assistant — Ingestion System Brief

**Purpose:** This document briefs an automated agent on how the Avatar Assistant content ingestion system works, so it can independently ingest new assets.

**Repository:** `AI_Agentic_Systems_Mastery`
**Project root:** the repo root (all paths below are relative to it)

---

## What the System Does

Avatar Assistant is a knowledge capture and retrieval system. Content is organised into **assets** — structured documents that get summarised, chunked, and embedded as vectors for semantic retrieval. Workflow A queries these assets by topic and generates summaries, outlines, and scripts from the most relevant chunks.

---

## Directory Structure

```
content/
  index.yaml                          # Global registry of all assets
  <asset_id>/
    <asset_id>.asset.yaml             # Asset manifest (metadata)
    raw/                              # Raw source files (markdown, text)
summaries/
  <asset_id>_summary.txt              # Plain text summary (1-3 sentences)
embedding/
  <asset_id>.jsonl                    # JSONL chunks with vector embeddings
```

---

## The Four Artefacts Per Asset

### 1. Asset Manifest — `content/<id>/<id>.asset.yaml`

YAML file with this structure:

```yaml
id: my_asset                          # Unique snake_case identifier
title: "Human-readable title"
category: governance_framework         # Free-text category
version: 1.0
description: >
  A 2-4 sentence description of the asset content.
source_files:
  research_note: content/my_asset/raw/source_document.md
  summary: summaries/my_asset_summary.txt
  embedding: embedding/my_asset.jsonl
  raw_notes: content/my_asset/raw/
tags:
  - tag1
  - tag2
created: 2026-03-23
updated: 2026-03-23
status: ready
```

**Required fields:** `id`, `title`, `category`, `description`, `source_files` (with `research_note`, `summary`, `embedding`), `tags`, `status`

### 2. Summary — `summaries/<id>_summary.txt`

- Plain text, 2-5 sentences
- Captures the core purpose and key concepts
- Used as fallback context when chunks aren't available

### 3. Embedding Chunks — `embedding/<id>.jsonl`

One JSON object per line. Each chunk:

```json
{
  "id": "my_asset_001",
  "asset": "my_asset",
  "type": "research_topic",
  "title": "Section Title",
  "text": "The actual content text for this chunk...",
  "vector": [0.123, -0.456, ...]
}
```

**Chunking strategy:**
- For short documents (< 500 words): single chunk containing the full summary
- For long documents (500+ words): split by section headings (`## `), one chunk per section
- Each chunk's `text` should be capped at ~2000 characters
- The `vector` field contains a 1536-dim embedding from OpenAI `text-embedding-3-small`
- The embedding input should be `"{title}: {text}"` to include the heading in the vector

**Generating vectors:**
```python
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=f"{chunk_title}: {chunk_text}"[:8000],
)
vector = response.data[0].embedding  # List[float], length 1536
```

If the API is unavailable (offline mode), omit the `vector` field. Retrieval will fall back to keyword matching.

### 4. Content Index — `content/index.yaml`

A YAML list. Add one entry per asset:

```yaml
- id: my_asset
  title: "Human-readable title"
  category: governance_framework
  manifest: content/my_asset/my_asset.asset.yaml
  summary: summaries/my_asset_summary.txt
  embedding: embedding/my_asset.jsonl
  status: ready
```

---

## Ingestion Procedure

### Option A: Using the built-in pipeline

If the asset has a simple structure (single research note → single chunk):

```bash
PYTHONPATH=src python3 -m avatar_assistant.content_ingest <asset_id>
```

This requires the manifest YAML to already exist. It will:
1. Load the manifest
2. Generate a summary from the research note (if missing)
3. Create a single-chunk embedding JSONL with vector (if API available)
4. Update `content/index.yaml`

### Option B: Manual multi-chunk ingestion (recommended for large documents)

For documents that benefit from section-level chunking:

1. **Create the directory:** `content/<asset_id>/raw/`
2. **Copy the source document** into `raw/`
3. **Write the asset manifest** at `content/<asset_id>/<asset_id>.asset.yaml`
4. **Write the summary** at `summaries/<asset_id>_summary.txt`
5. **Split the document into chunks** by section heading
6. **Generate vector embeddings** for each chunk via OpenAI API
7. **Write the JSONL** at `embedding/<asset_id>.jsonl`
8. **Update `content/index.yaml`** with the new entry

### Option C: Using the Python API directly

```python
from avatar_assistant.content_ingest import load_manifest, update_index

# After manually creating manifest, summary, and embedding files:
manifest = load_manifest("my_asset")
update_index(manifest)
```

---

## Currently Ingested Assets

| ID | Title | Chunks | Category |
|----|-------|--------|----------|
| `wallace_line` | The Wallace Line | 1 | natural_history |
| `forward_by_nature_philosophy` | Forward by Nature — Core Philosophy | 1 | core_philosophy |
| `psychographic_profile` | User Psychographic Profile | 1 | user_model |
| `milestone_ingestion_pipeline` | Ingestion Pipeline Foundation | 1 | project_milestone |
| `project_roadmap_2025_optimised` | AI Agentic System Roadmap | 1 | system_roadmap |
| `agent_journal` | Agentic Systems Build Journal | 1 | uncategorised |
| `idea_seeds` | Idea Seeds Vault | 1 | creativity |
| `dpif_white_paper` | DPIF White Paper | 14 | governance_framework |

---

## Conventions

- **Asset IDs** are `snake_case`, unique, descriptive (e.g. `dpif_white_paper`)
- **Chunk IDs** follow `{asset_id}_{NNN}` pattern (e.g. `dpif_white_paper_001`)
- **Status** should be `ready` for fully ingested assets, `unknown` for partial
- **Tags** are lowercase, no spaces, use underscores
- **Dates** use ISO format `YYYY-MM-DD`
- **Text encoding** is always UTF-8

## Quality Checks After Ingestion

1. Asset appears in `content/index.yaml` with `status: ready`
2. Summary file exists and is 2-5 sentences
3. Embedding JSONL has at least one record per line, valid JSON
4. Each chunk has `id`, `asset`, `title`, `text` fields
5. Chunks with vectors have `vector` field with 1536 floats
6. `ava workflow-a --topic "<relevant query>" --assets <asset_id>` returns content
7. `pytest -q` still passes with `AA_OFFLINE=1`

---

## Key Source Files

| File | Purpose |
|------|---------|
| `src/avatar_assistant/content_ingest.py` | Ingestion pipeline (load manifest, generate summary, create embedding, update index) |
| `src/avatar_assistant/retrieval.py` | Load JSONL chunks, score by vector cosine similarity or keyword fallback |
| `src/avatar_assistant/config.py` | `PROJECT_ROOT`, `EMBEDDING_DIR` constants |
| `content/index.yaml` | Global asset registry |
