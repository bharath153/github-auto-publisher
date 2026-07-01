"""Configuration management for GitHub Auto-Publisher."""
import json
import os
from pathlib import Path


class Config:
    """Manages app configuration and API credentials."""

    CONFIG_FILE = Path.home() / ".github_auto_publisher" / "config.json"

    DEFAULTS = {
        "github_token": "",
        "llm_provider": "openai",  # openai, claude, kimi, ollama
        "openai_api_key": "",
        "claude_api_key": "",
        "kimi_api_key": "",
        "ollama_url": "http://localhost:11434",
        "ollama_model": "codellama",
        "default_visibility": "public",
        "auto_generate_readme": True,
        "auto_generate_contributing": False,
        "auto_generate_license": False,
    }

    def __init__(self):
        self._config = {}
        self.load()

    def load(self):
        """Load configuration from file."""
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, "r") as f:
                self._config = json.load(f)
        else:
            self._config = self.DEFAULTS.copy()
            self.save()

    def save(self):
        """Save configuration to file."""
        self.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self._config, f, indent=2)

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value
        self.save()
