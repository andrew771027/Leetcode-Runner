from abc import ABC, abstractmethod

from events.event import Event


class EventSubscriber(ABC):

    @abstractmethod
    def handle(self, event: Event):
        pass
