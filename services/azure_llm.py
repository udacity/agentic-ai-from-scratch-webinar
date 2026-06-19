"""Small Azure OpenAI service shared by every webinar demo."""

import os
from pathlib import Path

from azure.identity import InteractiveBrowserCredential
from azure.keyvault.secrets import SecretClient
from openai import OpenAI


class AzureLLMClient:
    """Load Azure OpenAI settings from Key Vault and call the model."""

    def __init__(self, vault_url=None):
        self._load_env_file()
        self.vault_url = vault_url or os.getenv("WEBINAR_KEY_VAULT_URL")
        if not self.vault_url:
            raise ValueError(
                "Set WEBINAR_KEY_VAULT_URL to https://<vault-name>.vault.azure.net/"
            )

        # Open an explicit browser sign-in for this local webinar demo.
        credential = InteractiveBrowserCredential()
        vault = SecretClient(vault_url=self.vault_url, credential=credential)
        endpoint = vault.get_secret("aoai-endpoint").value.rstrip("/")
        api_key = vault.get_secret("aoai-key").value
        self.deployment = vault.get_secret("aoai-deployment").value

        self.client = OpenAI(
            api_key=api_key,
            base_url=f"{endpoint}/openai/v1/",
        )

    @staticmethod
    def _load_env_file():
        """Load simple KEY=VALUE settings from the project-level .env file."""
        env_path = Path(__file__).resolve().parents[1] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")

            # Respect a real exported value, but replace a missing or empty one.
            if not os.environ.get(key):
                os.environ[key] = value

    def chat(self, messages, temperature=0.2, max_tokens=700):
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
