from src.llm.model import LLMModelParams, PromptInput, PromptOutput
from abc import abstractmethod, ABC
from openai import OpenAI
import httpx

class LLMClient[M, P, O](ABC):
    def __init__(self, model_params: M) -> None:
        self.model_params = model_params

    @abstractmethod
    def generate(self, prompt: P) -> O:
        pass #pragma: no cover


class OpenAiClient(LLMClient[LLMModelParams, PromptInput, PromptOutput]):
    def __init__(self, client: OpenAI, model_params: LLMModelParams) -> None:
        super().__init__(model_params)
        self.client = client

    def generate(self, prompt: PromptInput) -> PromptOutput:
        response = self.client.chat.completions.create(
            model=self.model_params.model,
            messages=[
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            temperature=self.model_params.temperature
        )
        content = response.choices[0].message.content or "No Response"
        return PromptOutput(text=content)

class OllamaClient(LLMClient[LLMModelParams, PromptInput, PromptOutput]):
    def __init__(self, http_client: httpx.Client, base_url: str, model_params: LLMModelParams) -> None:
        super().__init__(model_params)
        self.http_client = http_client
        self.base_url = base_url

    def generate(self, prompt: PromptInput) -> PromptOutput:
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
