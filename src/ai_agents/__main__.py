from .chat import create_chat_model


def main() -> None:
    model = create_chat_model()
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

        response = model.invoke(prompt)
        print(f"Assistant: {response.content}")


if __name__ == "__main__":
    main()
