# src/avatar_assistant/manifest.py
"""Project-level manifest for tracking workflow runs and evaluations."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict

from .config import PROJECT_ROOT
from .logging_utils import get_logger, log_event
from .metrics import _utc_now_iso

MANIFEST_PATH = PROJECT_ROOT / "data" / "manifest.json"


def append_manifest_entry(entry: Dict[str, Any]) -> None:
    """Append a workflow or evaluation record to the project manifest."""
    lg = get_logger()

    entry = {**entry, "timestamp": _utc_now_iso()}

    manifest_dir = MANIFEST_PATH.parent
    manifest_dir.mkdir(parents=True, exist_ok=True)

    entries = []
    if MANIFEST_PATH.exists():
        try:
            raw = MANIFEST_PATH.read_text(encoding="utf-8")
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                entries = parsed
        except (json.JSONDecodeError, OSError):
            log_event(lg, "manifest.read_error", path=str(MANIFEST_PATH))

    entries.append(entry)

    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=str(manifest_dir), suffix=".tmp"
    ) as tmp:
        json.dump(entries, tmp, indent=2)
        tmp_path = tmp.name

    os.replace(tmp_path, str(MANIFEST_PATH))
    log_event(lg, "manifest.entry_appended", total_entries=len(entries))
