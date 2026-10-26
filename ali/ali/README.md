# ALI - Personal AI Assistant (JARVIS-style)

## Setup (Windows)
1. Install Python 3.10+ from python.org (tick "Add to PATH").
2. Get an API key at https://console.anthropic.com
3. Open this folder in VS Code / Visual Studio.
4. Easiest: double-click `run.bat`. First run installs everything and creates `.env`.
5. Open `.env`, paste your key after `ANTHROPIC_API_KEY=`, save, run `run.bat` again.

## Manual setup (terminal)
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env      (then edit .env)
    python main.py              (text chat)
    python main.py --voice      (voice mode: say "Ali, what time is it?")

## Voice troubleshooting
If `pip install PyAudio` fails, run `pip install pipwin` then `pipwin install pyaudio`.
Text mode works without a microphone (you can delete PyAudio from requirements.txt).

## Try saying
- "Open YouTube and play lo-fi music"
- "Remember that my favourite colour is blue"
- "How's my computer doing?"
- "Take a note: buy milk"

## Customise
- Personality: `PERSONALITY` in `ali/brain.py`
- New abilities: add a function + schema in `ali/tools.py`
- Allowed apps: `APPS` dict in `ali/tools.py`
- Memory is stored in `data/memory.json`
