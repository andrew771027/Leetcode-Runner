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
ExecutionRequest
 ↓
Runner
 ↓
Backend
 ↓
ExecutionResult
```

CLI 不再直接操作測試執行細節，而是將使用者輸入轉換成 `ExecutionRequest`，再交給 Runner 執行。

---

## Requirements

### Functional Requirements

本版本需要支援：

1. 使用者可以透過 Typer CLI 指定測試檔案。
2. CLI 可以將使用者輸入轉換成 `ExecutionRequest`。
3. Runner 可以接收 `ExecutionRequest`。
4. Runner 可以呼叫 Backend 執行測試。
5. Backend 可以透過 pytest 執行測試。
6. Backend 可以回傳 `ExecutionResult`。
7. CLI 可以根據 `ExecutionResult` 顯示執行結果。

### Non-functional Requirements

本版本開始重視：

1. **Separation of Concerns**

   * CLI 只負責輸入與輸出。
   * Runner 只負責流程協調。
   * Backend 只負責實際測試執行。

2. **Extensibility**

   * 未來可以在 `ExecutionRequest` 中加入 timeout、env、backend type、docker image 等設定。

3. **Maintainability**

   * 避免 function signature 隨著需求成長一直膨脹。

4. **Testability**

   * Runner 可以不依賴 CLI 被單獨測試。
   * CLI 可以只測參數解析與 request 建立。

---

## Architecture

本版本包含：

* CLI (Typer)
* Runner
* ExecutionRequest
* PytestBackend
* ExecutionResult

新增核心元件：

```text
ExecutionRequest
```

用來封裝一次測試執行所需的資訊。

整體架構如下：

```text
User
 ↓
Typer CLI
 ↓
ExecutionRequest
 ↓
Runner
 ↓
PytestBackend
 ↓
pytest subprocess
 ↓
ExecutionResult
 ↓
CLI Output
```

---

## Component Responsibilities

### CLI

CLI 負責：

```text
- Parse command
- Validate basic input
- Build ExecutionRequest
- Call Runner
- Display ExecutionResult
```

CLI 不負責：

```text
- 決定如何執行 pytest
- 管理 backend
- 處理測試流程
- 分析測試結果
```

---

### ExecutionRequest

`ExecutionRequest` 負責封裝一次測試執行所需的資訊。

例如：

```text
test_path
working_directory
optional configuration
```

未來可以擴充：

```text
timeout
environment variables
backend type
docker image
test category
problem name
tags
```

它的角色是：

```text
把 raw CLI arguments 轉換成系統內部可理解的 request model。
```

---

### Runner

Runner 負責：

```text
- 接收 ExecutionRequest
- 協調測試執行流程
- 呼叫 Backend
- 回傳 ExecutionResult
```

Runner 不需要知道：

```text
- CLI 是 Typer 還是 argparse
- 使用者如何輸入參數
- pytest subprocess 的細節
```

---

### PytestBackend

PytestBackend 負責：

```text
- 接收 ExecutionRequest
- 組合 pytest command
- 透過 subprocess 執行 pytest
- 收集 stdout / stderr / exit_code
- 建立 ExecutionResult
```

---

### ExecutionResult

ExecutionResult 負責封裝測試結果：

```text
success
exit_code
stdout
stderr
duration
```

未來可以擴充：

```text
test_count
passed_count
failed_count
skipped_count
error_type
metadata
```

---

## Design Decisions

### 1. 為什麼引入 ExecutionRequest？

v1 中，CLI 可能直接把 `test_path` 傳給 Runner：

```python
runner.run(test_path)
```

這在一開始很簡單，但未來如果需求增加：

```text
timeout
working_directory
backend
docker_image
env variables
tags
problem name
```

function signature 可能變成：

```python
runner.run(
    test_path,
    working_directory,
    timeout,
    backend,
    docker_image,
    env,
    tags,
    problem_name,
)
```

這會讓 Runner 的介面越來越不穩定。

因此 v2 引入 `ExecutionRequest`：

```python
runner.run(request)
```

未來新增欄位時，可以擴充 request，而不是一直修改 Runner 的 function signature。

---

### 2. 為什麼 CLI 不直接呼叫 Backend？

CLI 是使用者入口，不應該知道太多執行細節。

如果 CLI 直接呼叫 Backend，會變成：

```text
CLI -> PytestBackend
```

短期可行，但未來會出現問題：

```text
- CLI 會知道 backend 選擇邏輯
- CLI 會知道 execution flow
- CLI 會知道 retry / timeout / report / analytics
```

因此 v2 改成：

```text
CLI -> Runner -> Backend
```

Runner 成為 system core，CLI 只是 adapter。

---

### 3. 為什麼使用 Typer？

Typer 讓 CLI 更容易維護與擴充。

相較於 argparse，Typer 的優點是：

```text
- command 結構更清楚
- type hint 友善
- 適合多 command CLI
- 未來可以加入 run、discover、report、benchmark 等 command
```

這讓 CLI 可以逐步演進成：

```text
leetcode-runner run
leetcode-runner discover
leetcode-runner report
leetcode-runner benchmark
```

---

### 4. 為什麼 Backend 仍固定為 PytestBackend？

v2 的目標不是建立 plugin system，而是先把 CLI / Runner / Request 的邊界切乾淨。

所以這一版仍然固定使用：

```text
PytestBackend
```

這是刻意的取捨。

因為如果 v2 同時加入多 Backend、Registry、Plugin，系統會一次變太複雜，反而不利學習 System Design。

---

## Trade-offs

### 優點

1. **CLI 與 Runner 解耦**

   * CLI 不再直接處理測試執行流程。
   * Runner 可以被其他入口使用，例如未來的 API Server 或 Web UI。

2. **Request Model 穩定化**

   * `ExecutionRequest` 讓系統輸入變得明確。
   * 未來新增設定時，不需要一直修改 Runner 介面。

3. **系統邊界更清楚**

   * CLI 是 adapter。
   * Runner 是 core。
   * Backend 是 executor。
   * Result 是 output model。

4. **更適合演進**

   * 未來可以加入 DockerBackend。
   * 未來可以加入 Discovery。
   * 未來可以加入 Parallel Execution。
   * 未來可以加入 Analytics。

### 缺點

1. **對 v2 來說稍微多一層**

   * 如果只是執行單一 pytest，`ExecutionRequest` 看起來有點多餘。

2. **還沒有真正多 Backend**

   * 雖然設計上預留空間，但目前仍固定使用 PytestBackend。

3. **Runner 還不是 Orchestrator**

   * 目前 Runner 只處理單一 request。
   * 尚未處理多測試、批次任務、平行執行、結果彙整。

4. **缺少完整錯誤模型**

   * 目前失敗大多還是依賴 pytest exit code。
   * 還不能區分 test failure、execution error、timeout、invalid path。

---

## Current Limitations

目前仍然：

1. 一次只能執行一個測試。
2. Backend 固定為 PytestBackend。
3. 沒有 Discovery。
4. 沒有 Parallel Execution。
5. 沒有 Analytics。
6. 沒有 Report。
7. 沒有 Registry。
8. 沒有 Backend Interface。
9. 沒有 Retry。
10. 沒有 Timeout。
11. 沒有 Environment Isolation。
12. 沒有歷史結果儲存。

---

## Evolution from Version 1

### Version 1

v1 的核心是：

```text
CLI
 ↓
TestRunner
 ↓
PytestBackend
 ↓
pytest
```

v1 解決的是：

```text
如何把手動 pytest command 包裝成一個 Runner？
```

---

### Version 2

v2 的核心是：

```text
CLI
 ↓
ExecutionRequest
 ↓
Runner
 ↓
Backend
 ↓
ExecutionResult
```

v2 解決的是：

```text
如何把使用者輸入和測試執行流程分離？
```

---

### 主要演進

v1 到 v2 的最大變化是：

```text
從 raw input
變成 request model
```

也就是：

```text
CLI argument
 ↓
ExecutionRequest
```

這代表系統開始有自己的內部資料模型。

---

## System Design Notes

### 1. Adapter vs Core

v2 開始出現一個重要概念：

```text
CLI 是 adapter
Runner 是 core
```

CLI 只是其中一種入口。

未來系統可能有多種入口：

```text
CLI
Web API
Scheduler
GitHub Actions
Internal Dashboard
```

這些入口都可以建立 `ExecutionRequest`，再交給 Runner。

因此 Runner 不應該依賴 CLI。

---

### 2. Request Object Pattern

`ExecutionRequest` 是 v2 最重要的設計。

它讓系統輸入從分散的參數，變成一個明確的物件：

```text
Before:
runner.run(test_path, working_directory, timeout, backend)

After:
runner.run(request)
```

這個設計讓系統更容易擴充，也讓每次執行都有明確的資料邊界。

---

### 3. Stable Interface

v2 透過 `ExecutionRequest` 讓 Runner 的介面穩定：

```python
runner.run(request)
```

未來即使 request 裡面增加欄位，Runner 的 public interface 仍然可以保持不變。

這是 System Design 裡很重要的思維：

```text
讓會變的東西包在 model 裡，
讓核心介面保持穩定。
```

---

### 4. Separation of Concerns

v2 的責任分工比 v1 更清楚：

```text
CLI:
處理使用者輸入

ExecutionRequest:
描述一次執行需求

Runner:
協調執行流程

Backend:
執行測試

ExecutionResult:
描述執行結果
```

這讓每個元件可以被單獨理解、單獨測試、單獨替換。

---

### 5. Path Toward Test Platform

v2 雖然仍然只是 CLI Runner，但它已經開始往 Test Platform 方向靠近。

因為只要有 `ExecutionRequest`，未來就可以讓不同來源建立 request：

```text
CLI command
Web UI form
REST API request
Scheduled job
GitHub PR trigger
```

最後都變成：

```text
ExecutionRequest -> Runner
```

這是從工具走向平台的第一步。

---

## Next Version

Version 3 預計加入：

1. Test Discovery
2. Multiple Execution Requests
3. Parallel Executor
4. Summary
5. Benchmark
6. Analytics

Runner 將開始負責協調多個測試，而不只是執行單一測試。

v3 的核心演進方向會是：

```text
Discover tests
 ↓
Build multiple ExecutionRequests
 ↓
Run requests
 ↓
Collect ExecutionResults
 ↓
Generate Summary
```

---

## UML Files

本版本 UML 包含：

* `component.mmd`
* `class.mmd`
* `sequence.mmd`
* `activity.mmd`

---

## Summary

v2 的重點不是增加功能，而是讓架構開始有清楚的內部資料模型。

這一版學到的 System Design 核心是：

```text
把 CLI input 轉換成 ExecutionRequest，
讓 Runner 不依賴使用者入口。
```

也就是從：

```text
CLI-driven execution
```

演進成：

```text
Request-driven execution
```

這個改變讓 LeetCode Runner 未來可以支援更多入口、更多 Backend、更多執行模式。
