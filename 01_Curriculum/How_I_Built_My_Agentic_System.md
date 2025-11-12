# How I Built My Agentic System

## 1. Objective
Describe the goal of the project and what problem it solves.

## 2. Architecture Summary
- CLI entry (`cli.py`)
- Core pipeline (`run.py`, `transcribe.py`, `summarize.py`)
- Logging & metrics (`logging_utils.py`, `config.py`)
- Evaluation & scoring (`evaluate.py`)
- API layer (`server.py`)

## 3. Development Phases
**M1 – Setup:** environment, repo, venv  
**M2 – Loop:** record → transcribe → summarize  
**M3 – Hardening:** metrics, tests, CI  
**M4 – Integration:** packaging + API  
**M5 – Reflection:** lessons, outcomes

## 4. Key Lessons
- What you learned about agentic system design  
- What was hardest to understand initially  
- How tests and logging improved reliability  

## 5. Next Steps
- Add `/evaluate` route to API  
- Add Dockerfile for deployment  
- Experiment with multiple agents / queue orchestration  
