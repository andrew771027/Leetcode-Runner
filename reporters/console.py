from typing import List

from models.test_result import TestResult
from reporters.registry import ReporterRegistry
from runner.interfaces import BaseReporter


@ReporterRegistry.register("console")
class ConsoleReporter(BaseReporter):

    def report(self, results: List[TestResult]):
        for r in results:
            status = "✅ PASS" if r.success else "❌ FAIL"
            print(f"{status} {r.name:<25} ({r.duration:.4f}s)")
