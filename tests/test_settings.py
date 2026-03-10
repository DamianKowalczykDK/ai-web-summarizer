from src.llm.client import OpenAiClient, OllamaClient
from src.settings import Config

config = Config()
def test_openai_client_creation() -> None:
    client = config.openai_client

    assert client is not None
    assert isinstance(client, OpenAiClient)


def test_ollama_client_creation() -> None:
    client = config.ollama_client

    assert client is not None
    assert isinstance(client, OllamaClient)