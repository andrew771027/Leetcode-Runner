from events.bus import EventBus
from events.registry import SubscriberRegistry


class EventBusBuilder:

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def build(self, subscriber_config: dict[str, list[str]]) -> EventBus:
        bus = EventBus()

        for event_type, subscriber_names in subscriber_config.items():
            for name in subscriber_names:
                subscriber = self._create_subscriber(name)
                bus.subscribe(event_type, subscriber)

        return bus

    def _create_subscriber(self, name: str):
        if name == "file_logger":
            return SubscriberRegistry.create(
                name,
                path=f"{self.output_dir}/event.jsonl",
            )

        return SubscriberRegistry.create(name)
