from ai_agents.chat import create_chat_model


def test_create_chat_model_uses_ollama_configuration() -> None:
    model = create_chat_model(
        model_name="llama3.2",
        base_url="http://ollama.test:11434",
    )

    assert model.model == "llama3.2"
    assert model.base_url == "http://ollama.test:11434"


def test_create_chat_model_loads_configuration_from_dotenv(
    monkeypatch, tmp_path
) -> None:
    (tmp_path / ".env").write_text(
        "OLLAMA_MODEL=env-model\nOLLAMA_BASE_URL=http://env.test:11434\n"
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)

    model = create_chat_model()

    assert model.model == "env-model"
    assert model.base_url == "http://env.test:11434"
