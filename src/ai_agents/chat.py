import os

from langchain_ollama import ChatOllama

DEFAULT_MODEL = "qwen2.5-coder:3b"
DEFAULT_BASE_URL = "http://localhost:11434"


def create_chat_model(
    model_name: str | None = None,
    base_url: str | None = None,
) -> ChatOllama:
    """Create the local Ollama chat model used by the agent."""
    return ChatOllama(
        model=model_name or os.getenv("OLLAMA_MODEL", DEFAULT_MODEL),
        base_url=base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL),
    )
