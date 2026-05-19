import json
from datetime import datetime

from runner.models import TestResult


class Storage:

    def append(self, result: TestResult, file="history.jsonl"):
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": result.name,
            "success": result.success,
            "duration": result.duration,
        }

        with open(file, "a") as f:
            f.write(json.dumps(data) + "\n")
