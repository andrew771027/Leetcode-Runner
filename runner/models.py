from dataclasses import dataclass


@dataclass
class TestResult:
    category: str
    problem: str
    success: bool
    return_code: int
    duration: float | None = None
