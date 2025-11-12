from pathlib import Path
from .config import OPENAI_API_KEY
def transcribe(pth:str)->str:
    p=Path(pth)
    if not p.exists(): raise FileNotFoundError(p)
    if p.suffix.lower()==".txt": return p.read_text(encoding="utf-8")
    if OPENAI_API_KEY and p.suffix.lower() in {".mp3",".wav",".m4a",".mp4",".aac",".flac",".webm"}:
        try:
            from openai import OpenAI
            c=OpenAI(api_key=OPENAI_API_KEY)
            with open(p,"rb") as f: r=c.audio.transcriptions.create(model="whisper-1",file=f)
            return r.text
        except Exception as e: return f"[transcription-error] {e}"
    return "[no-transcription] Provide a .txt or set OPENAI_API_KEY and use audio."
