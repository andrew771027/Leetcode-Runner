# Version 1 - Simple LeetCode Runner

## Goal

建立一個最小可運作（Minimum Viable Product）的 LeetCode Runner。

此版本的目標不是追求完整的架構，而是建立一條最基本的執行流程：

```
CLI
    ↓
Test Runner
    ↓
Pytest Backend
    ↓
pytest
```

使用者可以透過 CLI 指定測試檔案，Runner 會呼叫 pytest 執行測試，最後將測試結果輸出至終端機。

---

# Architecture

本版本包含四個主要元件：

* CLI
* TestRunner
* PytestBackend
* ExecutionResult

其中：

* **CLI**：負責解析命令列參數。
* **TestRunner**：負責協調整個測試流程。
* **PytestBackend**：透過 `subprocess` 呼叫 pytest。
* **ExecutionResult**：封裝測試結果，避免直接回傳 primitive values。

---

# Design Decisions

本版本採用最簡單的設計：

* 一次只執行一個測試。
* Backend 固定使用 pytest。
* 使用 subprocess 執行外部程序。
* 執行完成後回傳 ExecutionResult。

目前尚未考慮：

* Parallel Execution
* Docker Backend
* Plugin System
* Registry
* Builder Pattern
* Analytics
* Report Generation

---

# Current Limitations

目前架構仍存在一些限制：

1. 一次只能執行一個測試。
2. Backend 不可替換。
3. CLI 與 Runner 的責任尚未完全分離。
4. 沒有測試發現（Discovery）。
5. 沒有平行執行能力。
6. 沒有統計分析或測試報告。

---

# Next Version

Version 2 預計改善：

* 將 CLI 與 Runner 進一步解耦。
* 使用 Typer 取代 argparse。
* 建立更清楚的 Runner 責任分工。
* 為未來支援多種 Backend（例如 Docker、Subprocess）預留擴充能力。

---

# UML Files

本版本 UML 包含：

* `component.mmd`：系統元件組成。
* `class.mmd`：核心類別與依賴關係。
* `sequence-run-one-test.mmd`：一次測試執行流程。
* `activity-run-flow.mmd`：完整執行流程。
