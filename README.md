
# AI Agents

A Python project for building local AI agents with Ollama and LangChain.

## Requirements

- Python 3.12+
- `uv`
- Ollama running at `http://localhost:11434`

Install the model already available on this machine:

```bash
ollama run qwen2.5-coder:3b
```

`llmfit` reports that this machine can run larger tool-use models with reduced
speed because the GTX 1050 Ti has 4 GB of VRAM. For higher-quality agent work,
consider trying an 8B Qwen3/DeepSeek-R1 variant after validating its memory use.

## Setup

```bash
uv sync
```

The default model is `qwen2.5-coder:3b`. Override it, or the Ollama endpoint,
with a `.env` file or environment variables. Start from `.env.example`:

```bash
cp .env.example .env
```

The supported variables are:

- `OLLAMA_MODEL`
- `OLLAMA_BASE_URL`

You can also override them directly in the shell:

```bash
OLLAMA_MODEL=qwen3:8b uv run ai-agents
OLLAMA_BASE_URL=http://localhost:11434 uv run ai-agents
```

Start the interactive chat:

```bash
uv run ai-agents
```

The agent can calculate using `add`, `multiply`, `divide`, `subtract`, and
`calculate`. Use `calculate` for compound expressions so standard operator
precedence is preserved. When the model requests one of these tools, the chat loop prints
the tool call, executes it, prints the result, and sends that result back to
the model. It supports both native LangChain tool calls and JSON tool calls
from models that do not emit native tool-call metadata.

Run tests:

```bash
uv run pytest
```
