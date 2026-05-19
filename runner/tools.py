from pathlib import Path


def run_pytest(path: str):
    return ["python", "-m", "pytest", path, "-v"]


def run_file(path: Path):
    return ["python", "-m", "pytest", str(path), "-v"]
