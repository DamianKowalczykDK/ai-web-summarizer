from typing import Callable, Any
from src.llm.client import LLMClient
from src.llm.model import PromptInput, PromptOutput
from src.service.schema import SummaryArgs


class SummaryService[M, P: PromptInput, O: PromptOutput]:
    def __init__(
            self,
            analysis_llm: LLMClient[M, P, O],
            generation_llm: LLMClient[M, P, O],
            serializer_llm: LLMClient[M, P, O],
            prompt_factory: Callable[[dict[str, Any]], P],
            prompt_loader: Callable[[str], tuple[P, P, P]]
    ) -> None:
        self.analysis_llm = analysis_llm
        self.generator_llm = generation_llm
        self.serializer_llm = serializer_llm
        self.prompt_factory = prompt_factory
        self.prompt_loader = prompt_loader



    def __call__(self,
                 args: SummaryArgs,
                 prompt_path: str,
                 data_format: str,
                 input_loader: Callable[[str], str | None],
                 on_complete: Callable[[O], None] | None= None) -> PromptOutput:
        text = input_loader(args.path)

        if not text:
            raise ValueError("Could not fetch page text.")

        analysis_prompt, formatter_prompt, serializer_prompt = self.prompt_loader(prompt_path)

        filled_analysis: P = self.prompt_factory({
            "system": analysis_prompt.system.format(count=args.count, language=args.language),
            "user": analysis_prompt.user.format(text=text)
        })

        output = self.analysis_llm.generate(filled_analysis)

        filled_formatter: P = self.prompt_factory({
            "system": formatter_prompt.system.format(language=args.language),
            "user": formatter_prompt.user.format(text=output.text)
        })

        formater_output = self.generator_llm.generate(filled_formatter)

        filled_serializer: P = self.prompt_factory({
            "system": serializer_prompt.system.format(format=data_format.upper()),
            "user": serializer_prompt.user.format(text=formater_output.text)
        })

        summary_output = self.serializer_llm.generate(filled_serializer)

        if on_complete:
            on_complete(summary_output)

        return summary_output



