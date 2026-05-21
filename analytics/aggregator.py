from typing import List

from models.test_result import TestResult


class Aggregator:

    def rank(self, results: List[TestResult]):
        return sorted(results, key=lambda r: (not r.success, r.duration))

    def summary(self, results: List[TestResult]):
        total = len(results)
        passed = sum(1 for r in results if r.success)

        return {"total": total, "passed": passed, "failed": total - passed}
