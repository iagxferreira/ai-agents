import json
from typing import Any


def tool_call_key(tool_call: dict[str, Any]) -> str:
    """Create a stable identity for detecting repeated tool requests."""
    return json.dumps(
        [tool_call["name"], tool_call.get("args", {})], sort_keys=True
    )


def parse_json_tool_calls(content: Any) -> list[dict[str, Any]]:
    """Parse one or more JSON tool calls emitted without native metadata."""
    if not isinstance(content, str):
        return []

    text = content.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()

    values = []
    try:
        values = [json.loads(text)]
    except json.JSONDecodeError:
        for line in text.splitlines():
            try:
                values.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return [
        value
        for value in values
        if isinstance(value, dict)
        and isinstance(value.get("name"), str)
        and isinstance(value.get("arguments"), dict)
    ]


def parse_json_tool_call(content: Any) -> dict[str, Any] | None:
    """Parse the first JSON tool call emitted without native metadata."""
    calls = parse_json_tool_calls(content)
    return calls[0] if calls else None
