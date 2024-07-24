# orchestralAI/__init__.py
from .client.main import OrchestralClient

"""Placeholder for orchestralAI package."""

def orchestralAI(api_key: str) -> OrchestralClient:
    client = OrchestralClient(api_key)
    return client