"""Things Ali can actually DO. Add your own by writing a function,
adding it to FUNCTIONS, and adding a schema to SCHEMAS."""
import os
import platform
import subprocess
import urllib.parse
import webbrowser
from datetime import datetime

import psutil

from . import memory

# Apps Ali is allowed to open (edit freely). Windows-friendly defaults.
APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "explorer": "explorer",
    "cmd": "cmd",
    "vscode": "code",
    "chrome": "chrome",
    "edge": "msedge",
    "spotify": "spotify",
}


def get_time():
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


def system_status():
    mem = psutil.virtual_memory()
    out = [
        f"OS: {platform.system()} {platform.release()}",
        f"CPU usage: {psutil.cpu_percent(interval=0.5)}%",
        f"RAM usage: {mem.percent}% of {mem.total / 1e9:.1f} GB",
    ]
    bat = psutil.sensors_battery() if hasattr(psutil, "sensors_battery") else None
    if bat:
        out.append(f"Battery: {bat.percent:.0f}% ({'charging' if bat.power_plugged else 'on battery'})")
    return "\n".join(out)


def open_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened {url}"


def web_search(query):
    webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(query))
    return f"Opened a web search for: {query}"


def play_youtube(query):
    webbrowser.open("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query))
    return f"Opened YouTube results for: {query}"


def open_app(name):
    key = name.lower().strip()
    if key not in APPS:
        return f"I'm not allowed to open '{name}'. Allowed: {', '.join(APPS)}"
    try:
        if platform.system() == "Windows":
            os.startfile(APPS[key])  # noqa
        else:
            subprocess.Popen([APPS[key]])
        return f"Opened {key}"
    except Exception as e:
        return f"Couldn't open {key}: {e}"


FUNCTIONS = {
    "get_time": lambda **_: get_time(),
    "system_status": lambda **_: system_status(),
    "open_website": lambda url, **_: open_website(url),
    "web_search": lambda query, **_: web_search(query),
    "play_youtube": lambda query, **_: play_youtube(query),
    "open_app": lambda name, **_: open_app(name),
    "remember": lambda key, value, **_: memory.remember(key, value),
    "forget": lambda key, **_: memory.forget(key),
    "add_note": lambda text, **_: memory.add_note(text),
    "read_notes": lambda **_: memory.read_notes(),
}


def _s(name, desc, props=None, req=None):
    return {
        "name": name,
        "description": desc,
        "input_schema": {"type": "object", "properties": props or {}, "required": req or []},
    }


_str = lambda d: {"type": "string", "description": d}

SCHEMAS = [
    _s("get_time", "Get the current date and time."),
    _s("system_status", "Get CPU, RAM and battery status of this computer."),
    _s("open_website", "Open a website in the default browser.", {"url": _str("Website URL or domain")}, ["url"]),
    _s("web_search", "Search Google in the browser.", {"query": _str("Search query")}, ["query"]),
    _s("play_youtube", "Open YouTube search results for a song/video.", {"query": _str("What to play")}, ["query"]),
    _s("open_app", f"Open an app. Allowed: {', '.join(APPS)}.", {"name": _str("App name")}, ["name"]),
    _s("remember", "Store a long-term fact about the user (name, preferences, routines).",
       {"key": _str("Short label"), "value": _str("The fact")}, ["key", "value"]),
    _s("forget", "Delete a stored fact.", {"key": _str("Label to delete")}, ["key"]),
    _s("add_note", "Save a note or reminder for the user.", {"text": _str("Note text")}, ["text"]),
    _s("read_notes", "Read back the user's saved notes."),
]


def run(name, args):
    fn = FUNCTIONS.get(name)
    if not fn:
        return f"Unknown tool: {name}"
    try:
        return str(fn(**(args or {})))
    except Exception as e:
        return f"Tool error: {e}"
