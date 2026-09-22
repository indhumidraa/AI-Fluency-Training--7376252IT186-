import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# .env is located in P1
ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE)

PROVIDER = os.getenv("PROVIDER", "").lower()
MODEL = os.getenv("MODEL")

if PROVIDER == "groq":
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
else:
    raise ValueError(f"Unsupported provider: {PROVIDER}")