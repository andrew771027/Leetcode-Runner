# 📘 LeetCode Runner — v1 → v3 Architecture Evolution

---

## 🎯 專案目標

建立一個可擴展的 LeetCode 測試框架：

- CLI 控制測試執行
- 支援 pytest / benchmark / coverage
- 支援多種 execution backend（local / docker / CI）

---

# 🥚 v1 — Basic Script Version

## 架構

```
CLI (argparse)
   ↓
subprocess
   ↓
pytest
```

## CLI (argparse)

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--problem")
args = parser.parse_args()

print(f"Run problem: {args.problem}")
```

## 執行 pytest

```python
import subprocess

subprocess.run(["python", "-m", "pytest"])
```

## 問題

- CLI boilerplate 太多
- execution tightly coupled
- environment inconsistency (PATH issue)

---

# 🧱 v2 — Layered Architecture

## 架構

```
CLI (Typer)
   ↓
Runner Core (Orchestrator)
   ↓
Test / Benchmark / Coverage
   ↓
Execution Layer
```

## CLI (Typer)

```python
import typer

app = typer.Typer()

@app.command()
def run(problem: str):
    print(f"Running {problem}")

if __name__ == "__main__":
    app()
```

## Runner Core

```python
class Runner:
    def run_tests(self):
        print("Running tests...")
```

## 問題

- Execution layer still coupled
- cannot swap docker / remote execution

---

# 🚀 v3 — Strategy Pattern Architecture

## 架構

```
CLI
 ↓
Orchestrator (pure logic)
 ↓
Execution Backend (pluggable)
 ↓
pytest / tools
```

---

## Orchestrator

```python
class Orchestrator:
    def __init__(self, backend):
        self.backend = backend

    def run_tests(self):
        return self.backend.run("python -m pytest")
```

---

## Backend Interface

```python
from abc import ABC, abstractmethod

class ExecutionBackend(ABC):
    @abstractmethod
    def run(self, command: str):
        pass
```

---

## Subprocess Backend

```python
import subprocess

class SubprocessBackend(ExecutionBackend):
    def run(self, command: str):
        return subprocess.run(command, shell=True)
```

---

## Docker Backend

```python
import subprocess

class DockerBackend(ExecutionBackend):
    def run(self, command: str):
        cmd = f"docker run my-image {command}"
        return subprocess.run(cmd, shell=True)
```

---

## CLI Example

```python
import typer

app = typer.Typer()

@app.command()
def test(use_docker: bool = False):

    backend = DockerBackend() if use_docker else SubprocessBackend()

    orchestrator = Orchestrator(backend)
    orchestrator.run_tests()

if __name__ == "__main__":
    app()
```

---

# 📊 Summary

| Version | Architecture | Key Idea |
|--------|-------------|---------|
| v1 | Script | simple automation |
| v2 | Layered | separation of concerns |
| v3 | Strategy Pattern | pluggable backend |

---

# 🎯 Core Idea

LeetCode Runner =

> A pluggable execution framework for test orchestration
