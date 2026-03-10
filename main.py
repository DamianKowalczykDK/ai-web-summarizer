from src.settings import config
from src.llm.model import LLMModelParams, PromptInput, PromptOutput
from src.llm.prompts import load_summary_prompts
from src.scrapper.html_text_extractor import fetch_page_text
from src.service.file_writer import FormaterWriterService
from src.service.summary_service import SummaryService
from src.service.schema import SummaryArgs
import argparse


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description="Analyze a web page using AI")
        parser.add_argument("--url", required=True, help="URL of the page to analyze", type=str)
        parser.add_argument("--count",required=True, help="Number of quiz questions to generate", type=int)
        parser.add_argument("--language", required=True, help="Language to use", type=str)
        parser.add_argument("--format", choices=["json", "csv", "yaml", "html"], required=True, help="Format to use", type=str)
        parser.add_argument("--prompt-path", required=False, default="prompts/summary.yaml", help="Prompt to use", type=str)

        args = parser.parse_args()

        openai_client = config.openai_client

        # To use the Ollama client, uncomment the following line:
        # ollama_client = config.ollama_client


        summary_generator_service = SummaryService[LLMModelParams, PromptInput, PromptOutput](
            analysis_llm=openai_client,
            generation_llm=openai_client,
            serializer_llm=openai_client,
            prompt_factory=lambda d: PromptInput(**d),
            prompt_loader=load_summary_prompts
        )
        summary_args = SummaryArgs(args.url, args.count, args.language)

        filename = f"summary_output.{args.format.lower()}"
        format_writer_service = FormaterWriterService[PromptOutput]()
        _ = summary_generator_service(
            summary_args,
            args.prompt_path,
            args.format,
            input_loader=fetch_page_text,
            on_complete=lambda o: print(format_writer_service.save(o, "txt",filename))
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()