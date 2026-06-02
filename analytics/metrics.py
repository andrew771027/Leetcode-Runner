from typing import Any, Dict, List

from models.test_result import TestResult


class Metrics:

    def summary(self, results: List[TestResult]) -> Dict[str, Any]:
        total = len(results)

        passed = sum(1 for r in results if r.success)

        durations = [r.duration for r in results if r.duration is not None]

        average_duration = sum(durations) / len(results) if durations else 0

        slowest = max(results, key=lambda r: r.duration or 0, default=None)

        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "average_duration": average_duration,
            "slowest": slowest.name if slowest else None,
        }

    def detect_regression(
        self,
        previous: List[TestResult],
        current: List[TestResult],
        threshold: float = 2.0,
    ) -> List[Dict]:

        previous_map = {r.name: r for r in previous}
        regressions = []

        for cur in current:
            prev = previous_map.get(cur.name)

            if not prev:
                continue

            if prev.duration and cur.duration and cur.duration > prev.duration * threshold:
                regressions.append(
                    {
                        "category": cur.category,
                        "name": cur.name,
                        "previous duration": prev.duration,
                        "current duration": cur.duration,
                        "ratio": cur.duration / prev.duration,
                    }
                )

        return regressions
