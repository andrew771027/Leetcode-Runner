from typing import List
from reporters.base import Reporter
from models.test_result import TestResult

class ConsoleReporter(Reporter):

    def report(self, results: List[TestResult]):
        for r in results:
            status = "✅ PASS" if r.success else "❌ FAIL"
            print(f"{status} {r.name:<25} ({r.duration:.4f}s)")