::: card
# 🚀 LeetCode Runner

**從 Script 到 Test Infrastructure（v1 → v3.4）**
:::

::: card
## 🎯 專案目標

打造一個可擴展、可替換 execution、可測試的 LeetCode 測試框架。

-   CLI 一鍵執行測試
-   支援 pytest / benchmark / coverage
-   支援 local / docker / CI / remote
:::

::: card
## 🧠 我的設計思考

::: highlight
pytest = test runner\
LeetCode Runner = orchestration layer
:::

一開始只是想寫 script，但後來發現：

-   我其實在做 runner 的上層
-   這是一個 framework，而不是工具
:::

::: card
## ⚠️ 核心問題：Execution Environment

    pytest ❌（依賴 PATH）
    python -m pytest ✅（依賴 interpreter）

問題：

-   subprocess 使用當前 virtualenv
-   但測試可能在另一個 repo
:::

::: card
## 🥚 v1 --- Script

    CLI (argparse)
       ↓
    subprocess
       ↓
    pytest

    import argparse
    import subprocess

    parser = argparse.ArgumentParser()
    parser.add_argument("--problem")
    args = parser.parse_args()

    subprocess.run(["python", "-m", "pytest"])

問題：

-   耦合嚴重
-   不可擴展
:::

::: card
## 🧱 v2 --- 分層架構

    CLI (Typer)
     ↓
    Runner Core
     ↓
    Execution Layer

    class Runner:
        def run_tests(self):
            print("running...")

問題：

-   execution 還是寫死
:::

::: card
## 🚀 v3 --- Strategy Pattern

    CLI
     ↓
    Orchestrator
     ↓
    Execution Backend
     ↓
    pytest

    class ExecutionBackend:
        def run(self, cmd):
            pass

    class Orchestrator:
        def __init__(self, backend):
            self.backend = backend

        def run_tests(self):
            return self.backend.run("pytest")

突破：

-   execution 可替換
-   支援 docker / CI
:::

::: card
## 🧪 v3.1 --- 工程化

    from dataclasses import dataclass

    @dataclass
    class ExecutionResult:
        return_code: int
        stdout: str
        stderr: str

提升：

-   可觀測性
-   錯誤處理
:::

::: card
## 🧠 v3.2 --- 平台化

    Execution Platform
     ├── Local
     ├── Docker
     └── CI

關鍵：

-   解決環境問題
-   支援多 execution
:::

::: card
## 🧠 v3.3 --- Multi Repo

    class ExecutionContext:
        repo_path: str
        runtime: str

解決：

-   不同 repo dependency
:::

::: card
## 🧠 v3.4 --- Test Infra

    CLI
     ↓
    Orchestrator
     ↓
    Execution Platform
     ↓
    pytest

能力：

-   execution abstraction
-   CI integration
-   環境隔離
:::

::: card
## 💬 我的心得

-   抽象比實作重要
-   execution 本質是 strategy
-   infra 問題比想像早出現
-   設計能力 \> coding
:::

::: card
## 🏁 總結

::: highlight
LeetCode Runner =\
\
A pluggable execution platform for test orchestration
:::
:::
