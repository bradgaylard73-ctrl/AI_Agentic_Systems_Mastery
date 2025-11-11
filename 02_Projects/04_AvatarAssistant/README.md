# Avatar Assistant

## Objective
Build a voice-first avatar that captures thoughts, turns them into structured logs, and makes them searchable and summarizable for creative work.

## Problem Statement
- **Inputs:** microphone audio, optional text notes, reference docs.
- **System levers:** ASR accuracy, chunking strategy, embedding model, retrieval settings, summarization prompts.
- **Outputs:** timestamped entries in a local DB + daily/weekly summaries.
- **Constraints and assumptions:** runs on Mac, offline-first where possible, clear audit trail.

## Success Metrics
- Loop success rate ≥ 80% (no manual fixes)
- Median latency ≤ 1.5 s (mic to summary)
- WER ≤ 10% on your voice
- Retrieval groundedness ≥ 0.8 (answer uses cited chunks)
- Zero-crash sessions over a 30-minute run

## Scope
- **In:** local recording, transcription, storage, retrieval, summarization, CLI.
- **Out (v1):** cloud LLM fine-tuning, web UI, multi-user support.

## Architecture Sketch
- **CLI** starts a session → **Recorder** saves WAV → **ASR** transcribes → **Chunker** segments → **Embedder** writes vectors → **Store** (SQLite + vector table) → **Summarizer** writes daily summary → **Exporter** writes Markdown.
- Config in `.env` and `PROJECT.yaml`.

## Milestones
M1: 2025-11-20 — Architecture + dependencies running  
M2: 2025-12-10 — First end-to-end loop (record → transcribe → summarize)  
M3: 2026-01-05 — Refactor, docs, repeatable demo script

## How to Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest -q