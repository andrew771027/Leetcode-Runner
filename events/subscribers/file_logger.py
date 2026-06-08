import json
from pathlib import Path

from contracts.subscriber import EventSubscriber
from events.event import Event


class FileLoggerSubscriber(EventSubscriber):
    def __init__(self, path="output/event.jsonl"):
        self.path = Path(path)

    def handle(self, event: Event):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.path, "a") as f:
            f.write(json.dumps({"event_type": event.type, "payload": event.payload}))
            f.write("\n")
