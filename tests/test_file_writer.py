from src.service.file_writer import FormatterWriterService
from src.llm.model import PromptOutput
from pathlib import Path
import pytest

@pytest.fixture
def output() -> PromptOutput:
    return PromptOutput(text="Test ...")


def test_save(tmp_path: Path, output: PromptOutput) -> None:
    writer = FormatterWriterService[PromptOutput]()
    filename = tmp_path / "output.txt"

    result_path = writer.save(output=output, data_format="txt", filename=str(filename))

    assert Path(result_path).exists()
    assert Path(result_path).read_text() == output.text

def test_save_default_filename(tmp_path: Path, output: PromptOutput, monkeypatch: pytest.MonkeyPatch) -> None:
    writer = FormatterWriterService[PromptOutput]()
    monkeypatch.chdir(tmp_path)

    result_path = writer.save(output=output, data_format="txt")
    expected_filename = tmp_path / "summary_output.txt"

    assert Path(expected_filename).exists()
    assert result_path == "summary_output.txt"

