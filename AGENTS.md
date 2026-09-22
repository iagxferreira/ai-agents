# AGENTS.md

## Project

This project uses Python, `uv`, LangChain, and a locally running Ollama
service. Keep the initial agent implementation small and easy to run offline.

## Development

- Use `uv` for dependency changes and command execution.
- Keep runtime configuration in environment variables rather than committing
  machine-specific settings or credentials.
- Add or update tests before changing application behavior.
- Run `uv run pytest` before considering a change complete.
- Do not require a live Ollama server for unit tests.

## Commits

- Make each commit atomic: one coherent change per commit.
- Use semantic commit messages such as `feat: add Ollama chat model` or
  `docs: document local setup`.
- Do not commit `.env` files, credentials, model weights, or `.venv`.
