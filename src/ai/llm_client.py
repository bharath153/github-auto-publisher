"""Unified LLM client supporting multiple providers."""
import httpx
from typing import Optional, List, Dict, Any
from enum import Enum


class LLMProvider(Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    KIMI = "kimi"
    OLLAMA = "ollama"


class LLMClient:
    """Client for interacting with various LLM APIs."""

    def __init__(self, provider: LLMProvider, api_key: str, **kwargs):
        self.provider = provider
        self.api_key = api_key
        self.base_url = kwargs.get("base_url", "")
        self.model = kwargs.get("model", self._default_model())
        self.client = httpx.Client(timeout=120.0)

    def _default_model(self) -> str:
        defaults = {
            LLMProvider.OPENAI: "gpt-4o",
            LLMProvider.CLAUDE: "claude-3-5-sonnet-20241022",
            LLMProvider.KIMI: "kimi-latest",
            LLMProvider.OLLAMA: "codellama",
        }
        return defaults.get(self.provider, "gpt-4o")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using the configured LLM."""
        if self.provider == LLMProvider.OPENAI:
            return self._call_openai(prompt, system_prompt)
        elif self.provider == LLMProvider.CLAUDE:
            return self._call_claude(prompt, system_prompt)
        elif self.provider == LLMProvider.KIMI:
            return self._call_kimi(prompt, system_prompt)
        elif self.provider == LLMProvider.OLLAMA:
            return self._call_ollama(prompt, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _call_openai(self, prompt: str, system_prompt: Optional[str]) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 4000,
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _call_claude(self, prompt: str, system_prompt: Optional[str]) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        body = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            body["system"] = system_prompt

        response = self.client.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]

    def _call_kimi(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Kimi API (Moonshot AI) - adjust endpoint as needed."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _call_ollama(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Local Ollama instance - free, private, no API key needed."""
        body = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3},
        }
        if system_prompt:
            body["system"] = system_prompt

        response = self.client.post(
            f"{self.base_url}/api/generate",
            json=body
        )
        response.raise_for_status()
        return response.json()["response"]

    def close(self):
        self.client.close()
