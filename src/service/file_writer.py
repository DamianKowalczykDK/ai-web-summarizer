from src.llm.model import PromptOutput


class FormaterWriterService[O: PromptOutput]:
    def save(self, output: O, data_format: str, filename: str | None = None) -> str:
        path = filename or f"summary_output.{data_format}"
        with open(path, "w", encoding="utf-8") as file:
            file.write(output.text)
        return path

