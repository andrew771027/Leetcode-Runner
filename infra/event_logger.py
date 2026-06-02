import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class EventLogger:

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)

    def emit(self, event_type: str, payload: Dict[str, Any], filename: str = "event.jsonl") -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        path = self.output_dir / filename

        event: dict = {
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload,
        }

        with open(path, "a") as f:
            f.write(json.dumps(event) + "\n")
