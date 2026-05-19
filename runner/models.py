from dataclasses import dataclass


@dataclass
class TestResult:
    name: str
    category: str
    problem: str
    success: bool
    return_code: int
    duration: float | None = None
