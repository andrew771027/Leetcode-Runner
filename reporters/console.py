from typing import List

from models.test_result import TestResult
from runner.interfaces import BaseReporter
from reporters.registry import ReporterRegistry


@ReporterRegistry.register("console")
class ConsoleReporter(BaseReporter):

    def report(self, results: List[TestResult]):
        for r in results:
            status = "✅ PASS" if r.success else "❌ FAIL"
            print(f"{status} {r.name:<25} ({r.duration:.4f}s)")
