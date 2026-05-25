from typing import List

from models.test_result import TestResult


class Storage:
    def __init__(self):
        self._data: List[TestResult] = []

    def append(self, result: TestResult):
        self._data.append(result)

    def all(self) -> List[TestResult]:
        return self._data
