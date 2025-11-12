import json,time
from pathlib import Path
from .transcribe import transcribe
from .summarize import summarize
def run(path:str)->str:
    ts=time.strftime("%Y%m%d-%H%M%S")
    out=Path("data/runs")/ts
    out.mkdir(parents=True,exist_ok=True)
    t=transcribe(path); (out/"transcript.txt").write_text(t,encoding="utf-8")
    s=summarize(t); (out/"summary.md").write_text(s,encoding="utf-8")
    (out/"manifest.json").write_text(json.dumps({"input":path,"created":ts,"artifacts":["transcript.txt","summary.md"]},indent=2),encoding="utf-8")
    return str(out)
if __name__=="__main__":
    import sys
    if len(sys.argv)<2: print("usage: python -m avatar_assistant.run <path>"); sys.exit(2)
    print("wrote:", run(sys.argv[1]))
