from src.llm.model import LLMModelParams, PromptInput, PromptOutput
from abc import abstractmethod, ABC
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
import httpx

class LLMClient[M, P, O](ABC):
    """
    Abstract base class for LLM clients.

    This class defines a common interface for interacting with different
    Large Language Model providers. Concrete implementations should
    implement the `generate` method to send a prompt and return a response.

    Type Parameters
    ---------------
    M : Model parameter type
    P : Prompt input type
    O : Prompt output type
    """

    def __init__(self, model_params: M) -> None:
        """
        Initialize the LLM client with model parameters.

        Parameters
        ----------
        model_params : M
            Configuration parameters for the language model
            (e.g. model name, temperature).
        """
        self.model_params = model_params

    @abstractmethod
    def generate(self, prompt: P) -> O:
        """
        Generate a response from the language model based on a prompt.

        Parameters
        ----------
        prompt : P
            Input prompt containing system and user messages.

        Returns
        -------
        O
            Generated output from the language model.
        """
        pass #pragma: no cover


class OpenAiClient(LLMClient[LLMModelParams, PromptInput, PromptOutput]):
    """
    Client implementation for interacting with OpenAI chat models.

    Uses the OpenAI Python SDK to send prompts and retrieve generated
    responses from OpenAI chat completion endpoints.
    """

    def __init__(self, client: OpenAI, model_params: LLMModelParams) -> None:
        """
        Initialize the OpenAI client.

        Parameters
        ----------
        client : OpenAI
            Instance of the OpenAI SDK client.
        model_params : LLMModelParams
            Configuration parameters for the OpenAI model
            (e.g. model name, temperature).
        """
        super().__init__(model_params)
        self.client = client

    def generate(self, prompt: PromptInput) -> PromptOutput:
        """
        Send a prompt to the OpenAI model and return the generated response.

        Parameters
        ----------
        prompt : PromptInput
            Input prompt containing system and user messages.

        Returns
        -------
        PromptOutput
            Model response wrapped in a PromptOutput object.
        """
        response = self.client.chat.completions.create(
            model=self.model_params.model,
            messages=[
                ChatCompletionSystemMessageParam(
                role="system", content= prompt.system
                ),
                ChatCompletionUserMessageParam(
                role="user", content=prompt.user
                )
            ],
            temperature=self.model_params.temperature
        )
        content = response.choices[0].message.content or "No Response"
        return PromptOutput(text=content)


class OllamaClient(LLMClient[LLMModelParams, PromptInput, PromptOutput]):
    """
    Client implementation for interacting with an Ollama API endpoint.

    Sends HTTP requests to an Ollama server to generate responses
    from locally hosted language models.
    """

    def __init__(self, http_client: httpx.Client, base_url: str, model_params: LLMModelParams) -> None:
        """
        Initialize the Ollama client.

        Parameters
        ----------
        http_client : httpx.Client
            HTTP client used to communicate with the Ollama API.
        base_url : str
            Base URL of the Ollama chat endpoint.
        model_params : LLMModelParams
            Configuration parameters for the Ollama model
            (e.g. model name, temperature).
        """
        super().__init__(model_params)
        self.http_client = http_client
        self.base_url = base_url

    def generate(self, prompt: PromptInput) -> PromptOutput:
        """
        Send a prompt to the Ollama API and return the generated response.

        Parameters
        ----------
        prompt : PromptInput
            Input prompt containing system and user messages.

        Returns
        -------
        PromptOutput
            Model response wrapped in a PromptOutput object.
        """
        payload = {
            "model": self.model_params.model,
            "messages": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            "temperature": self.model_params.temperature,
            "stream": False
        }

        response = self.http_client.post(self.base_url, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data.get("message", {}).get("content", "No Response")
        return PromptOutput(text=content)