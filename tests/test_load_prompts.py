from src.llm.model import PromptInput
from src.llm.prompts import load_summary_prompts
import tempfile
import yaml
import pytest

def test_load_test_prompts_valid() -> None:
    data = {
        "analysis": {
            "system": "Analyze system",
            "user": "Analyze user",
        },
        "formatter": {
            "system": "Format system",
            "user": "Format user",
        },
        "serializer": {
            "system": "Serialize system",
            "user": "Serialize user",
        }
    }
    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        f.seek(0)
        analysis, formatter, serializer = load_summary_prompts(f.name)

    assert analysis == PromptInput(system="Analyze system", user="Analyze user")
    assert formatter == PromptInput(system="Format system", user="Format user")
    assert serializer == PromptInput(system="Serialize system", user="Serialize user")

def test_load_test_prompts_invalid() -> None:
    data = {
        "analysis": {
            "system": "Analyze system",
            "user": "Analyze user",
        },
        "formatter": {}
    }

    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        f.seek(0)

    with pytest.raises(ValueError, match="Invalid prompt in structure YAML"):
        _ = load_summary_prompts(f.name)