from dataclasses import dataclass

@dataclass
class PromptInput:
    """
    Represents the input prompt sent to a language model.

    This structure separates the prompt into a system message
    (instructions for the model) and a user message (actual query).
    """
    system: str
    user: str


@dataclass
class PromptOutput:
    """
    Represents the response returned by a language model.

    Attributes
    ----------
    text : str
        The generated text returned by the model.
    """
    text: str


@dataclass
class LLMModelParams:
    """
    Configuration parameters used when calling a language model.

    Attributes
    ----------
    model : str
        Name or identifier of the language model to be used.
    temperature : float, default=0.7
        Sampling temperature controlling randomness of the output.
        Higher values produce more diverse results, while lower
        values make responses more deterministic.
    """
    model: str
    temperature: float = 0.7