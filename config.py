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


def get_github_config():
    """Return optional GitHub Issues settings from environment variables."""
    return {
        "token": os.getenv("GITHUB_TOKEN", ""),
        "repo_owner": os.getenv("GITHUB_REPO_OWNER", ""),
        "repo_name": os.getenv("GITHUB_REPO_NAME", ""),
        "create_issues": os.getenv("GITHUB_CREATE_ISSUES", "false").lower()
        == "true",
    }


def get_standup_input_mode():
    """Return the input mode for standup responses."""
    return os.getenv("STANDUP_INPUT_MODE", "structured").strip().lower()
