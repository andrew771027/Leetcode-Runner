from dataclasses import dataclass, field
from typing import Any

from models.test_result import TestResult


@dataclass
class ExecutionContext:
    files: list[tuple[str, str]] = field(default_factory=list)

    results: list[TestResult] = field(default_factory=list)

    summary: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)
