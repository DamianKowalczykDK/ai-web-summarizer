from dotenv import load_dotenv
from openai import OpenAI
from src.llm.client import OpenAiClient, OllamaClient
from src.llm.model import LLMModelParams
import httpx
import os

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))

    OLLAMA_URL = os.getenv("OLLAMA_URL", "")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "")
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", 0.7))

    @property
    def openai_client(self) -> OpenAiClient:
        return OpenAiClient(
            client=OpenAI(api_key=self.OPENAI_API_KEY),
            model_params=LLMModelParams(model=self.OPENAI_MODEL, temperature=self.OPENAI_TEMPERATURE),
        )

    @property
    def ollama_client(self) -> OllamaClient:
        return OllamaClient(
            http_client=httpx.Client(),
            base_url=self.OLLAMA_URL,
            model_params=LLMModelParams(model=self.OLLAMA_MODEL, temperature=self.OLLAMA_TEMPERATURE)
        )

config = Config()