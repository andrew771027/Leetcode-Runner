import json
from datetime import datetime


class EventLogger:
    def log(self, event: dict, file="event.jsonl"):
        event["timestamp"] = datetime.utcnow().isoformat()

        with open(file, "a") as f:
            f.write(json.dumps(event) + "\n")
