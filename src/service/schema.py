from dataclasses import dataclass

@dataclass
class SummaryArgs:
    """
    Data container for parameters used in the summarization process.

    Attributes
    ----------
    path : str
        Path to the input resource (e.g., a file or URL) containing the content to summarize.
    count : int
        Desired number of summary points, sentences, or sections.
    language : str
        Target language in which the summary should be generated.
    """
    path: str
    count: int
    language: str