# Avatar Assistant — Architecture

## Modules

| Module | Purpose |
|--------|---------|
| `cli.py` | Argument parsing, command dispatch (`run`, `workflow-a`, `evaluate-workflow-a`) |
| `run.py` | Audio pipeline orchestrator: transcribe → summarize → persist |
| `transcribe.py` | Audio/text input → text (OpenAI Whisper or .txt passthrough) |
| `summarize.py` | Text → summary (OpenAI API with heuristic fallback) |
| `retrieval.py` | Keyword-based chunk retrieval from JSONL embedding files |
| `manifest.py` | Append workflow/evaluation records to `data/manifest.json` |
| `workflows/workflow_a.py` | Retrieval-aware generation: topic + assets → summary, outline, scripts |
| `content_ingest.py` | Asset ingestion: manifest → summary → embedding JSONL → index |
| `evaluate.py` | Scoring (F1, cosine), quality heuristics, workflow evaluation |
| `evaluate_batch.py` | Batch evaluation over dev dataset |
| `metrics.py` | Metrics builder, atomic manifest writes |
| `logging_utils.py` | Structured JSON-line logging |
| `config.py` | Environment config (API keys, paths) |
| `server.py` | FastAPI endpoints for text/file processing |

## Data Flows

### Audio Pipeline (`ava run`)
```
Audio/Text → transcribe() → summarize() → build_metrics()
  → data/runs/<timestamp>/{transcript.txt, summary.md, manifest.json}
```

### Workflow A (`ava workflow-a`)
```
Topic + Asset IDs → retrieve_chunks() → generate summary/outline/scripts
  → console output + data/manifest.json
```

### Content System
- Asset manifests: `content/<id>/<id>.asset.yaml` (YAML)
- Global index: `content/index.yaml`
- Embeddings: `embedding/<id>.jsonl` (one JSON record per line)
- Summaries: `summaries/<id>_summary.txt`

## Offline Mode

When `AA_OFFLINE=1` or no `OPENAI_API_KEY`:
- Summarization uses sentence-extraction heuristic
- Workflow A generates content from keyword-matched chunk text
- All tests run in this mode (CI sets `AA_OFFLINE=1`)
