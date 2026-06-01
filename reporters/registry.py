from reporters.console import ConsoleReporter
from reporters.json_reporter import JsonReporter
from reporters.logger import LoggerReporter
from reporters.storage import StorageReporter


class ReporterRegistry:

    _registry = {
        "console": ConsoleReporter,
        "json": JsonReporter,
        "log": LoggerReporter,
        "storage": StorageReporter,
    }

    @classmethod
    def create_many(cls, names: str):
        return [cls._registry[name]() for name in names]
