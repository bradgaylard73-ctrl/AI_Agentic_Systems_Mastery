from pathlib import Path
import os

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- API KEYS ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- PROJECT ROOT ---
# This resolves to:  src/avatar_assistant/config.py  → up 2 levels → repo root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --- EMBEDDING DIRECTORY ---
# retrieval.py expects this constant to exist
EMBEDDING_DIR = PROJECT_ROOT / "embedding"
