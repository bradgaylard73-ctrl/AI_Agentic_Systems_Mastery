# PROJECT_TITLE

## Objective
One sentence defining the user outcome and the system boundary.

## Problem Statement
- Inputs
- System levers
- Outputs
- Constraints and assumptions

## Success Metrics
List 3–5 measurable, falsifiable metrics.

## Scope
In-scope and out-of-scope bullets.

## Architecture Sketch
Describe components and data flow. Add a diagram in `docs/` if useful.

## Milestones
- M1: YYYY-MM-DD — Definition complete and baseline running
- M2: YYYY-MM-DD — First measurable result
- M3: YYYY-MM-DD — Refactor and docs

## How to Run
```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Env
cp .env.example .env

# Tests
pytest -q
```

## Notes
Short log of decisions and tradeoffs.