"""Tiny JSON-file memory so Ali remembers facts and notes between runs."""
import json
from datetime import datetime
from . import config

FILE = config.DATA_DIR / "memory.json"


def _load():
    if FILE.exists():
        try:
            return json.loads(FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"facts": {}, "notes": []}


def _save(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def remember(key, value):
    d = _load()
    d["facts"][key] = value
    _save(d)
    return f"Remembered: {key} = {value}"


def forget(key):
    d = _load()
    if d["facts"].pop(key, None) is None:
        return f"I had nothing stored under '{key}'."
    _save(d)
    return f"Forgotten: {key}"


def add_note(text):
    d = _load()
    d["notes"].append({"time": datetime.now().isoformat(timespec="minutes"), "text": text})
    _save(d)
    return "Note saved."


def read_notes():
    notes = _load()["notes"]
    if not notes:
        return "No notes yet."
    return "\n".join(f"- [{n['time']}] {n['text']}" for n in notes[-20:])


def facts_summary():
    facts = _load()["facts"]
    if not facts:
        return "(nothing stored yet)"
    return "\n".join(f"- {k}: {v}" for k, v in facts.items())
