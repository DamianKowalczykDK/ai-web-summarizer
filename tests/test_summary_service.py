from typing import Callable
from unittest.mock import MagicMock
from src.llm.model import PromptInput, PromptOutput, LLMModelParams
from src.service.schema import SummaryArgs
from src.service.summary_service import SummaryService
import pytest


@pytest.fixture
def prompt_input_analysis() -> PromptInput:
    return PromptInput(system="System: {count}", user="User: {text}")

@pytest.fixture
def prompt_input_formatter() -> PromptInput:
    return PromptInput(system="System: {language}", user="User: {text}")

@pytest.fixture
def prompt_input_serializer() -> PromptInput:
    return PromptInput(system="System: {format}", user="User: {text}")

@pytest.fixture
def mock_llm_output() -> PromptOutput:
    return PromptOutput("Test output")

@pytest.fixture
def service(
        mock_llm_output: PromptOutput,
        prompt_input_analysis: PromptInput,
        prompt_input_formatter: PromptInput,
        prompt_input_serializer: PromptInput
) -> SummaryService[LLMModelParams, PromptInput, PromptOutput]:
    mock_analysis_llm = MagicMock()
    mock_analysis_llm.generate.return_value = mock_llm_output

    mock_generation_llm = MagicMock()
    mock_generation_llm.generate.return_value = mock_llm_output

    mock_serializer_llm = MagicMock()
    mock_serializer_llm.generate.return_value = mock_llm_output

    prompt_factory: Callable[[dict[str, str]], PromptInput] = lambda data: PromptInput(
        system=data["system"],
        user=data["user"],
    )
    prompt_loader: Callable[[str], tuple[PromptInput, PromptInput, PromptInput]] = lambda path: (
        prompt_input_analysis, prompt_input_formatter, prompt_input_serializer
    )

    return SummaryService(
        analysis_llm=mock_analysis_llm,
        generation_llm=mock_generation_llm,
        serializer_llm=mock_serializer_llm,
        prompt_factory=prompt_factory,
        prompt_loader=prompt_loader,

    )

def test_summary_generation_service_success(service: SummaryService, mock_llm_output: PromptOutput) -> None:
    args = SummaryArgs(path="test_url", count=5, language="English")

    loader = lambda path: "fetched text"

    result = service(
        args=args,
        prompt_path="test_path",
        data_format="json",
        input_loader=loader,
    )
    assert result == mock_llm_output

def test_summary_generation_service_not_text(service: SummaryService, mock_llm_output: PromptOutput) -> None:
    args = SummaryArgs(path="test_url", count=5, language="English")

    loader = lambda path: None

    with pytest.raises(ValueError, match="Could not fetch page text."):
        _ = service(
            args=args,
            prompt_path="test_path",
            data_format="json",
            input_loader=loader
        )

def test_summary_generation_service_on_completed(service: SummaryService, mock_llm_output: PromptOutput) -> None:
    args = SummaryArgs(path="test_url", count=5, language="English")

    loader = lambda path: "fetched text"
    mock_on_complete = MagicMock()

    result = service(
        args=args,
        prompt_path="test_path",
        data_format="json",
        input_loader=loader,
        on_complete=mock_on_complete
    )

    mock_on_complete.assert_called_once_with(mock_llm_output)
    assert result == mock_llm_output
