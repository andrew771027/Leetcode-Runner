import json
from typing import List
from reporters.base import Reporter
from models.test_result import TestResult

class JsonReporter(Reporter):
    def report(self, results: List[TestResult]):
        print(json.dumps([r.__dict__ for r in results], indent=2))