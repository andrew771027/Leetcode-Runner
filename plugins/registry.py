from backends.subprocess import SubprocessBackend
from backends.docker import DockerBackend

from reporters.console import ConsoleReporter
from reporters.json_reporter import JsonReporter

BACKENDS = {
    "subprocess": SubprocessBackend,
    "docker": DockerBackend
}

REPORTERS = {
    "console": ConsoleReporter,
    "json": JsonReporter
}