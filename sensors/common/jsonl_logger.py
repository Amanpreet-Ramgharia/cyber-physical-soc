import json
import os
from datetime import datetime, timezone

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def append_jsonl(path: str, event: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":"), ensure_ascii=False) + "\n")

def base_event(*, event_type: str, sensor: str, location: str, host: str) -> dict:
    return {
        "ts": now_iso(),
        "event_type": event_type,
        "sensor": sensor,
        "location": location,
        "host": host,
    }
