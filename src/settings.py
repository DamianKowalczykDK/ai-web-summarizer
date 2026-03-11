from dotenv import load_dotenv
from openai import OpenAI
from src.llm.client import OpenAiClient, OllamaClient
from src.llm.model import LLMModelParams
import httpx
import os

load_dotenv()

class Config:
    """
    Configuration class for initializing LLM clients from environment variables.

    Loads OpenAI and Ollama API credentials, model names, and temperatures
    from environment variables and provides ready-to-use client instances.

    Environment Variables
    ---------------------
    OPENAI_API_KEY : str
        API key for OpenAI.
    OPENAI_MODEL : str
        OpenAI model name.
    OPENAI_TEMPERATURE : float
        Temperature for OpenAI model.
    OLLAMA_URL : str
        Base URL of the Ollama API.
    OLLAMA_MODEL : str
        Ollama model name.
    OLLAMA_TEMPERATURE : float
        Temperature for Ollama model.
    """

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))

    OLLAMA_URL = os.getenv("OLLAMA_URL", "")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "")
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", 0.7))

    @property
    def openai_client(self) -> OpenAiClient:
        """
        Create and return an OpenAI client instance.

        Returns
        -------
        OpenAiClient
            Configured OpenAI LLM client ready to generate prompts.
        """
        return OpenAiClient(
            client=OpenAI(api_key=self.OPENAI_API_KEY),
            model_params=LLMModelParams(model=self.OPENAI_MODEL, temperature=self.OPENAI_TEMPERATURE),
        )

    @property
    def ollama_client(self) -> OllamaClient:
        """
        Create and return an Ollama client instance.

        Returns
        -------
        OllamaClient
            Configured Ollama LLM client ready to generate prompts.
        """
        return OllamaClient(
            http_client=httpx.Client(),
            base_url=self.OLLAMA_URL,
            model_params=LLMModelParams(model=self.OLLAMA_MODEL, temperature=self.OLLAMA_TEMPERATURE)
        )


config = Config()