from pathlib import Path


class Discovery:
    def __init__(self, bath_path: str):
        self.bath_path = Path(bath_path)

    def all_tests(self) -> list:
        return [(p.parent.name, p) for p in self.bath_path.rglob("test_*.py")]
