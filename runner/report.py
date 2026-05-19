import json
from typing import List

from runner.models import TestResult


class Reporter:

    @staticmethod
    def print(results: List[TestResult]):
        print("\n=== RESULT ===")
        for r in results:
            status = "✅ PASS" if r.success else "❌ FAIL"
            print(f"{status} {r.category} {r.problem} ({r.duration})")

    @staticmethod
    def to_json(results: List[TestResult], path:str="report.json"):
        data = [r.__dict__ for r in results]

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n📄 JSON report saved to {path}")
