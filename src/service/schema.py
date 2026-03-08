from dataclasses import dataclass

@dataclass
class SummaryArgs:
    path: str
    count: int
    language: str
    format: str