from src.llm.model import PromptInput
import yaml

def load_summary_prompts(path: str = "prompts/summary.yaml") -> tuple[PromptInput, PromptInput, PromptInput]:
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    analysis = data.get("analysis")
    formatter = data.get("formatter")
    serializer = data.get("serializer")

    if not analysis or not formatter:
        raise ValueError("Invalid prompt in structure YAML")

    return (
        PromptInput(system=analysis["system"], user=analysis["user"]),
        PromptInput(system=formatter["system"], user=formatter["user"]),
        PromptInput(system=serializer["system"], user=serializer["user"]),
    )

