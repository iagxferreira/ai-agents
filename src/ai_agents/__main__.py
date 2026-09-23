from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from .agent import parse_json_tool_calls, tool_call_key
from .calculator import CALCULATOR_TOOLS
from .chat import create_chat_model

MAX_TOOL_ROUNDS = 5


def main() -> None:
    model = create_chat_model().bind_tools(CALCULATOR_TOOLS)
    tools_by_name = {tool.name: tool for tool in CALCULATOR_TOOLS}
    print("Local Ollama chat started. Type 'exit' or press Ctrl-D to quit.")

    while True:
        try:
            prompt = input("You: ").strip()
        except EOFError:
            print()
            break

        if prompt.lower() in {"exit", "quit"}:
            break
        if not prompt:
            continue

        messages = [
            SystemMessage(
                content=(
                    "Use a calculator tool only when needed. After receiving a " 
                    "tool result, answer the user directly and do not call more "
                    "calculator tools for the same request. Use calculate for "
                    "compound expressions so normal operator precedence is kept."
                )
            ),
            HumanMessage(content=prompt),
        ]
        seen_tool_calls = set()
        last_result = None
        answer = None
        for _ in range(MAX_TOOL_ROUNDS):
            response = model.invoke(messages)
            messages.append(response)
            tool_calls = response.tool_calls
            if not tool_calls:
                json_tool_calls = parse_json_tool_calls(response.content)
                if json_tool_calls:
                    tool_calls = [
                        {
                            "id": f"json-tool-call-{index}",
                            "name": tool_call["name"],
                            "args": tool_call["arguments"],
                        }
                        for index, tool_call in enumerate(json_tool_calls)
                    ]

            if not tool_calls:
                answer = response.content
                break

            if last_result is not None:
                answer = str(last_result)
                break

            new_tool_calls = [
                tool_call
                for tool_call in tool_calls
                if tool_call_key(tool_call) not in seen_tool_calls
            ]
            if not new_tool_calls:
                answer = str(last_result)
                break

            for tool_call in new_tool_calls:
                seen_tool_calls.add(tool_call_key(tool_call))
                tool = tools_by_name.get(tool_call["name"])
                if tool is None:
                    answer = f"Unsupported tool requested: {tool_call['name']}"
                    break
                print(f"Calling tool: {tool_call['name']}")
                result = tool.invoke(tool_call["args"])
                print(f"Result: {result}")
                last_result = result
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=tool_call["id"])
                )
            if answer is not None:
                break
        else:
            answer = str(last_result)

        print(f"Assistant: {answer}")


if __name__ == "__main__":
    main()
