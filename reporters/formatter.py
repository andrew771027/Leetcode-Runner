import json
from typing import List

from models.test_result import TestResult


class ResultFormatter:

    @staticmethod
    def console(results: List[TestResult]) -> str:
        lines = []

        for r in results:
            status = "✅ PASS" if r.success else "❌ FAIL"
            lines.append(f"{status} {r.name:<25} ({r.duration:.4f}s)")

        return "\n".join(lines)

    @staticmethod
    def ranking(results: List[TestResult]) -> str:
        lines = []

        for i, r in enumerate(results):
            status = "✅ PASS" if r.success else "❌ FAIL"
            lines.append(f"{i}. {r.name:<25} {status} {r.duration:.3f}s")
        return "\n".join(lines)

    @staticmethod
    def json(results: List[TestResult]) -> str:
        return json.dumps([r.__dict__ for r in results], indent=2)
