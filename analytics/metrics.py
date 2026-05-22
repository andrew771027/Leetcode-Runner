from typing import List

from models.test_result import TestResult


class Metrics:

    def rank(self, results: List[TestResult]):
        return sorted(results, key=lambda r: (not r.success, r.duration))

    def short_summary(self, results: List[TestResult]):
        total = len(results)
        passed = sum(1 for r in results if r.success)

        return {"total": total, "passed": passed, "failed": total - passed}

    def precise_summary(self, results: List[TestResult]):
        total = len(results)

        passed = sum(1 for r in results if r.success)

        avg_time = sum(r.duration for r in results) / total

        slowest = max(results, key=lambda r: r.duration)

        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total,
            "avg_time": avg_time,
            "slowest": {"name": slowest.name, "duration": slowest.duration},
        }
