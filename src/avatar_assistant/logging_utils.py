# src/avatar_assistant/logging_utils.py
import json
import logging
import sys
import time
from typing import Any, Dict

class JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": int(time.time()),
            "level": record.levelname.lower(),
            "logger": record.name,
        }
        # message
        msg = record.getMessage()
        if msg:
            payload["message"] = msg
        # event + extras
        if hasattr(record, "event"):
            payload["event"] = getattr(record, "event")
        if hasattr(record, "fields"):
            # expect a dict
            try:
                payload.update(getattr(record, "fields"))
            except Exception:
                payload["fields_error"] = "non-dict fields"
        return json.dumps(payload, ensure_ascii=False)

def get_logger(name: str = "avatar_assistant") -> logging.Logger:
    lg = logging.getLogger(name)
    if getattr(lg, "_json_configured", False):
        return lg
    lg.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(JsonLineFormatter())
    lg.handlers.clear()
    lg.addHandler(h)
    lg._json_configured = True  # type: ignore[attr-defined]
    return lg

def log_event(lg: logging.Logger, event: str, **fields: Any) -> None:
    lg.info("", extra={"event": event, "fields": fields})