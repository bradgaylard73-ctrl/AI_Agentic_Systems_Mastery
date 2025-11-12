import re
def basic_quality_score(summary_md:str)->float:
    score = 0.0
    if re.search(r"^# ", summary_md, re.M): score += 0.3
    bullets = len(re.findall(r"^\s*[-*]\s+", summary_md, re.M))
    score += min(bullets, 5)*0.1
    if re.search(r"\b(Action|Next steps|Tasks?)\b", summary_md, re.I): score += 0.2
    return round(min(score, 1.0), 2)
