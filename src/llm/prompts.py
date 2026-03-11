from src.llm.model import PromptInput
import yaml

def load_summary_prompts(path: str) -> tuple[PromptInput, PromptInput, PromptInput]:
    """
    Load summary prompts from a YAML configuration file.

    The YAML file is expected to contain three prompt definitions:
    `analysis`, `formatter`, and `serializer`. Each prompt must
    include `system` and `user` fields.

    Parameters
    ----------
    path : str
        Path to the YAML file containing prompt definitions.

    Returns
    -------
    tuple[PromptInput, PromptInput, PromptInput]
        A tuple containing three PromptInput objects in the following order:
        (analysis_prompt, formatter_prompt, serializer_prompt).

    Raises
    ------
    ValueError
        If required prompt sections are missing in the YAML structure.
    """
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