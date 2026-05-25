from abc import ABC, abstractmethod
from typing import List
from models.test_result import TestResult

class Reporter(ABC):
    
    @abstractmethod
    def report(self, results: List[TestResult]) -> None:
        pass