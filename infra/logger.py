import json
from datetime import datetime

from models.test_result import TestResult


class Logger:
    def log_result(self, result: TestResult, file="event.jsonl") -> None:

        event: dict = {
            "type": "test_run",
            "name": result.name,
            "success": result.success,
            "duration": result.duration,
            "timestamp": datetime.utcnow().isoformat(),
        }

        with open(file, "a") as f:
            f.write(json.dumps(event) + "\n")
