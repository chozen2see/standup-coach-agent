"""
Environment configuration helpers for Standup Coach Agent.

The project can run without any LLM credentials. When a local .env file exists,
these helpers load the values into environment variables so optional LLM
features can use them later.
"""

import os
from pathlib import Path


BASE_DIR = Path(__file__).parent
ENV_FILE = BASE_DIR / ".env"


def load_environment(env_file=ENV_FILE):
    """Load simple KEY=value pairs from a .env file if one exists."""
    if not env_file.exists():
        return

    with open(env_file, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()

            if not clean_line or clean_line.startswith("#"):
                continue

            if "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def get_llm_config():
    """Return optional LLM settings from environment variables."""
    return {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    }
