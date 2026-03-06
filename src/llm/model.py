from dataclasses import dataclass

@dataclass
class PromptInput:
    system: str
    user: str

@dataclass
class PromptOutput:
    text: str

@dataclass
class LLMModelParams:
    model: str
    temperature: float = 0.7