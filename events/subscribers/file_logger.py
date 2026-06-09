import json
from pathlib import Path

from contracts.subscriber import EventSubscriber
from events.event import Event
from events.registry import SubscriberRegistry


@SubscriberRegistry.register("file_logger")
class FileLoggerSubscriber(EventSubscriber):
    def __init__(self, path: str = "output/event.jsonl"):
        self.path = Path(path)

    def handle(self, event: Event):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "type": event.type,
            "payload": event.payload,
        }

        with open(self.path, "a") as f:
            f.write(json.dumps(payload) + "\n")
