import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List

from models.test_result import TestResult


class HistoryStore:

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)

    def append(self, results: List[TestResult], filename: str = "history.jsonl"):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        path = self.output_dir / filename

        with open(path, "a") as f:
            record = {
                "timestamp": datetime.utcnow().isoformat(),
                "result": [asdict(r) for r in results],
            }

            f.write(json.dumps(record) + "\n")

    def load_latest(self, filename: str = "history.jsonl") -> List[TestResult]:
        path = self.output_dir / filename

        if not path.exists():
            return []

        lines = path.read_text().splitlines()
        if not lines:
            return []

        latest = json.loads(lines[-1])

        return [TestResult(**item) for item in latest["results"]]
