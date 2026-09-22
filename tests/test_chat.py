from ai_agents.chat import create_chat_model


def test_create_chat_model_uses_ollama_configuration() -> None:
    model = create_chat_model(
        model_name="llama3.2",
        base_url="http://ollama.test:11434",
    )

    assert model.model == "llama3.2"
    assert model.base_url == "http://ollama.test:11434"
