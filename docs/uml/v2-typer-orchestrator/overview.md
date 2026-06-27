# Version 2 - Typer Runner

## Goal

Version 2 的目標是將命令列介面（CLI）與測試執行流程分離，讓 Runner 成為真正負責執行測試的核心元件。

相較於 Version 1：

```text
CLI
 ↓
subprocess
```

Version 2 改為：

```text
CLI
 ↓
Runner
 ↓
Backend
```

CLI 不再直接操作測試，而是將執行需求交給 Runner。

---

# Architecture

本版本包含：

* CLI (Typer)
* Runner
* ExecutionRequest
* PytestBackend
* ExecutionResult

新增：

ExecutionRequest

用來封裝一次測試執行所需的資訊。

Runner 不需要知道 CLI 如何取得資料，只需要接收 ExecutionRequest。

---

# Design Decisions

本版本最大的改變是：

**引入 Request Object。**

ExecutionRequest 封裝：

* test_path
* working_directory
* optional configuration

未來如果增加：

* Docker
* Timeout
* Environment Variables

Runner 不需要修改 function signature。

---

Runner 負責：

* 接收 Request
* 呼叫 Backend
* 回傳 ExecutionResult

CLI 只負責：

* Parse Command
* 建立 Request
* 顯示結果

---

# Current Limitations

目前仍然：

* 一次只能執行一個測試
* Backend 固定為 PytestBackend
* 沒有 Discovery
* 沒有 Parallel Execution
* 沒有 Analytics
* 沒有 Report

---

# Next Version

Version 3 預計加入：

* Test Discovery
* Multiple Execution Requests
* Parallel Executor
* Summary
* Benchmark
* Analytics

Runner 將開始負責協調多個測試，而不只是執行單一測試。

---

# UML Files

* component.mmd
* class.mmd
* sequence.mmd
* activity.mmd
