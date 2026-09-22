.PHONY: setup setup-ollama sync test run

OLLAMA_MODEL ?= qwen2.5-coder:3b

setup:
	uv sync

setup-ollama:
	ollama pull $(OLLAMA_MODEL)

sync:
	uv sync

test:
	uv run pytest

run:
	uv run ai-agents
