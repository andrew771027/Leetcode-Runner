import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from models.test_result import TestResult


class ArtifactStore:

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)

    def save_report(self, results: List[TestResult], filename: str = "report.json"):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        path = self.output_dir / filename

        with open(path, "w") as f:
            json.dump([asdict(r) for r in results], f, indent=2)
