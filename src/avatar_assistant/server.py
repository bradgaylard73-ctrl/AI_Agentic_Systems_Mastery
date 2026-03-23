# src/avatar_assistant/server.py
"""FastAPI server exposing Avatar Assistant as a web app."""

from pathlib import Path
import tempfile
from typing import List, Optional

import yaml
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .config import PROJECT_ROOT
from .evaluate import basic_quality_score, evaluate_workflow_a
from .logging_utils import get_logger, log_event
from .run import run as run_pipeline
from .workflows.workflow_a import run_workflow_a

app = FastAPI(title="Avatar Assistant")
lg = get_logger()

STATIC_DIR = Path(__file__).parent / "static"


# ── Models ──────────────────────────────────────────────


class TextIn(BaseModel):
    text: str


class WorkflowIn(BaseModel):
    topic: str
    asset_ids: List[str]
    max_chunks: int = 5


# ── Pages ───────────────────────────────────────────────


@app.get("/", response_class=HTMLResponse)
def index():
    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        raise HTTPException(500, "Frontend not found")
    return html_path.read_text(encoding="utf-8")


# ── API: Assets ─────────────────────────────────────────


@app.get("/api/assets")
def list_assets():
    index_path = PROJECT_ROOT / "content" / "index.yaml"
    if not index_path.exists():
        return []
    with index_path.open(encoding="utf-8") as f:
        assets = yaml.safe_load(f) or []
    return [
        {
            "id": a["id"],
            "title": a.get("title", a["id"]),
            "category": a.get("category", ""),
            "status": a.get("status", "unknown"),
        }
        for a in assets
    ]


# ── API: Run Pipeline ──────────────────────────────────


def _read_run_results(out_dir: str):
    """Read artifacts from a pipeline run directory."""
    out = Path(out_dir)
    transcript = ""
    summary = ""
    if (out / "transcript.txt").exists():
        transcript = (out / "transcript.txt").read_text(encoding="utf-8")
    if (out / "summary.md").exists():
        summary = (out / "summary.md").read_text(encoding="utf-8")
    score = basic_quality_score(summary) if summary else None
    return {
        "ok": True,
        "output_dir": out_dir,
        "transcript": transcript,
        "summary": summary,
        "quality_score": score,
    }


@app.post("/run/text")
def run_text(body: TextIn):
    log_event(lg, "api.run.text.start")
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write(body.text)
            temp_path = f.name
        out = run_pipeline(temp_path)
        return _read_run_results(out)
    except Exception as exc:
        log_event(lg, "api.run.text.error", error=str(exc))
        raise HTTPException(500, detail=str(exc))


@app.post("/run/file")
def run_file(file: UploadFile = File(...)):
    log_event(lg, "api.run.file.start", filename=file.filename)
    if not file.filename:
        raise HTTPException(400, "missing filename")
    try:
        suffix = Path(file.filename).suffix or ".bin"
        with tempfile.NamedTemporaryFile("wb", suffix=suffix, delete=False) as f:
            f.write(file.file.read())
            temp_path = f.name
        out = run_pipeline(temp_path)
        return _read_run_results(out)
    except Exception as exc:
        log_event(lg, "api.run.file.error", error=str(exc))
        raise HTTPException(500, detail=str(exc))


# ── API: Workflow A ─────────────────────────────────────


@app.post("/api/workflow-a")
def api_workflow_a(body: WorkflowIn):
    log_event(lg, "api.workflow_a.start", topic=body.topic, assets=body.asset_ids)
    try:
        result = run_workflow_a(
            topic=body.topic,
            asset_ids=body.asset_ids,
            max_chunks=body.max_chunks,
        )
        return {
            "ok": True,
            "summary": result.summary,
            "outline": result.outline,
            "scripts": result.scripts,
            "metadata": result.metadata,
        }
    except Exception as exc:
        log_event(lg, "api.workflow_a.error", error=str(exc))
        raise HTTPException(500, detail=str(exc))


# ── API: Evaluate ───────────────────────────────────────


@app.post("/api/evaluate")
def api_evaluate(body: WorkflowIn):
    log_event(lg, "api.evaluate.start", topic=body.topic, assets=body.asset_ids)
    try:
        eval_result = evaluate_workflow_a(
            topic=body.topic,
            asset_ids=body.asset_ids,
            max_chunks=body.max_chunks,
        )
        return {"ok": True, **eval_result}
    except Exception as exc:
        log_event(lg, "api.evaluate.error", error=str(exc))
        raise HTTPException(500, detail=str(exc))
