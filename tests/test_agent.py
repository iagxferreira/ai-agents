from ai_agents.agent import parse_json_tool_call, parse_json_tool_calls, tool_call_key


def test_parse_json_tool_call_accepts_fenced_model_response() -> None:
    response = '''```json
{"name": "add", "arguments": {"a": 2, "b": 2}}
```'''

    assert parse_json_tool_call(response) == {
        "name": "add",
        "arguments": {"a": 2, "b": 2},
    }


def test_parse_json_tool_call_returns_none_for_normal_text() -> None:
    assert parse_json_tool_call("The answer is 4.") is None


def test_parse_json_tool_calls_accepts_multiple_json_lines() -> None:
    response = (
        '{"name": "multiply", "arguments": {"a": 9, "b": 7}}\n'
        '{"name": "divide", "arguments": {"a": 63, "b": 3}}'
    )

    assert parse_json_tool_calls(response) == [
        {"name": "multiply", "arguments": {"a": 9, "b": 7}},
        {"name": "divide", "arguments": {"a": 63, "b": 3}},
    ]


def test_tool_call_key_identifies_same_tool_and_arguments() -> None:
    call = {"name": "add", "args": {"a": 2, "b": 2}}

    assert tool_call_key(call) == tool_call_key(call.copy())
