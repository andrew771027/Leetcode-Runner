import yaml

from runner.config import RunnerConfig


class ConfigLoader:

    @staticmethod
    def load(path: str) -> RunnerConfig:
        with open(path, "r") as f:
            raw = yaml.safe_load(f)

        return RunnerConfig(
            base_path=raw["base_path"],
            backend=raw.get("backend", "subprocess"),
            workers=raw.get("workers", 4),
            output_dir=raw.get("output_dir", "output"),
            middleware=raw.get("middleware", ["retry", "benchmark"]),
            workflow=raw.get(
                "workflow", ["discover", "execute", "artifact", "history", "metrics", "report"]
            ),
            reporters=raw.get("reporters", ["console"]),
            event_subscribers=raw.get("events", {}),
        )
