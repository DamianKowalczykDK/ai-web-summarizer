from unittest.mock import MagicMock
from src.llm.model import LLMModelParams, PromptInput, PromptOutput
from src.llm.client import OpenAiClient, OllamaClient
import httpx
import pytest

@pytest.mark.parametrize(
    "response, expected_output",
    [
        ("Test", PromptOutput(text="Test")),
        ("Test", PromptOutput(text="No Response"))
    ]
)
def test_openai_client_generate(response: str | None, expected_output: str) -> None:
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test"))]
    mock_client.chat.completions.create.return_value = mock_response

    params = LLMModelParams("gpt-4o")
    client = OpenAiClient(client=mock_client, model_params=params)

    prompt = PromptInput(system="You are... ", user="Say Test")

    result = client.generate(prompt)

    assert result == PromptOutput(text="Test")

@pytest.mark.parametrize(
    "response, expected_output",
    [
        ({"message": {"content": "Test"}}, PromptOutput(text="Test")),
        ({"message": {}}, PromptOutput(text="No Response"))
    ]
)
def test_ollama_client_generate(response: dict[str, str], expected_output: str) -> None:
    http_client = MagicMock(spec=httpx.Client)
    mock_response = MagicMock()
    mock_response.json.return_value = {"message": {"content": "Test"}}
    mock_response.raise_for_status.return_value = None
    http_client.post.return_value = mock_response


    params = LLMModelParams("gpt-4o")
    client = OllamaClient(http_client=http_client, base_url="https://test", model_params=params)

    prompt = PromptInput(system="You are... ", user="Say Test")
    result = client.generate(prompt)

    assert result == PromptOutput(text="Test")