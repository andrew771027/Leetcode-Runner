import json
from typing import List

from models.test_result import TestResult
from reporters.registry import ReporterRegistry
from runner.interfaces import BaseReporter


@ReporterRegistry.register("json")
class JsonReporter(BaseReporter):
    def report(self, results: List[TestResult]):
        payload = [
            {
                "name": r.name,
                "success": r.success,
                "duration": r.duration,
            }
            for r in results
        ]

        print(json.dumps(payload, indent=2))
