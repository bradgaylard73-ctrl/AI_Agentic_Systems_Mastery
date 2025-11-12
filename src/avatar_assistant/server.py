from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
import tempfile
from .run import run as run_pipeline

app = FastAPI(title="Avatar Assistant API")

class TextIn(BaseModel):
    text: str

@app.post("/run/text")
def run_text(body: TextIn):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(body.text)
        temp_path = f.name
    out = run_pipeline(temp_path)
    return {"ok": True, "output_dir": out}

@app.post("/run/file")
def run_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "missing filename")
    suffix = Path(file.filename).suffix or ".bin"
    with tempfile.NamedTemporaryFile("wb", suffix=suffix, delete=False) as f:
        f.write(file.file.read())
        temp_path = f.name
    out = run_pipeline(temp_path)
    return {"ok": True, "output_dir": out}
