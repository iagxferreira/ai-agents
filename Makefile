.PHONY: sync test run

sync:
	uv sync

test:
	uv run pytest

run:
	uv run ai-agents
