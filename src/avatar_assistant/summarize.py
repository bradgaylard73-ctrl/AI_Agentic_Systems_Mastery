from .config import OPENAI_API_KEY
def summarize(text:str)->str:
    if not text.strip(): return "# Summary\n\n(no content)"
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            c=OpenAI(api_key=OPENAI_API_KEY)
            msg=[{"role":"system","content":"Concise markdown summary with bullets and actions."},
                 {"role":"user","content":f"Summarize:\n\n{text}"}]
            r=c.chat.completions.create(model="gpt-4o-mini",messages=msg,temperature=0.2)
            return r.choices[0].message.content
        except Exception as e: return f"# Summary\n\n[LLM error] {e}\n"
    lines=[ln.strip() for ln in text.splitlines() if ln.strip()]
    head=lines[:5]
    return "# Summary (offline)\n\n- "+"\n- ".join(head[:10])
