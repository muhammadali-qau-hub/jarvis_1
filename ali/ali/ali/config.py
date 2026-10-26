import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("ALI_MODEL", "claude-sonnet-5-5")
OWNER = os.getenv("ALI_OWNER_NAME", "Boss")
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
