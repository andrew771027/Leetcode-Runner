# Version 1 - Simple LeetCode Runner

## Goal

建立一個最小可運作（Minimum Viable Product）的 LeetCode Runner。

此版本的目標不是追求完整的架構，而是先建立一條最基本、可驗證的執行流程：

```text
CLI
    ↓
TestRunner
    ↓
PytestBackend
    ↓
pytest
```

使用者可以透過 CLI 指定測試檔案，Runner 會呼叫 pytest 執行測試，最後將測試結果輸出至終端機。

---

## Requirements

### Functional Requirements

本版本需要支援：

1. 使用者可以透過 CLI 指定一個測試檔案。
2. 系統可以呼叫 pytest 執行該測試檔案。
3. 系統可以取得 pytest 的執行結果。
4. 系統可以將執行結果轉換成 `ExecutionResult`。
5. 系統可以在終端機輸出測試是否成功。

### Non-functional Requirements

本版本暫時只重視：

1. **簡單性**：架構要容易理解。
2. **可執行性**：先讓整條流程真的跑起來。
3. **可觀察性基礎**：至少要知道測試成功或失敗。
4. **可演進性**：雖然現在很簡單，但不要讓未來完全無法擴充。

本版本尚未重視：

1. Scalability
2. Parallel Execution
3. Distributed Execution
4. Plugin System
5. Historical Analytics
6. Web Dashboard

---

## Architecture

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

整體架構如下：

```text
User
 ↓
CLI
 ↓
TestRunner
 ↓
PytestBackend
 ↓
pytest subprocess
 ↓
ExecutionResult
```

---

## Design Decisions

### 1. 為什麼需要 TestRunner？

雖然 v1 的流程很簡單，CLI 其實可以直接呼叫 pytest。

但是如果 CLI 直接呼叫 pytest，未來會變成：

```text
CLI 同時負責：
- 解析參數
- 決定執行流程
- 呼叫 pytest
- 處理結果
- 印出報告
```

這會讓 CLI 太胖，也會讓系統很難演進。

因此 v1 就先加入 `TestRunner`，讓 CLI 只負責使用者入口，真正的測試流程由 Runner 協調。

---

### 2. 為什麼需要 PytestBackend？

v1 雖然只支援 pytest，但仍然把執行測試的細節放到 `PytestBackend`。

原因是：

```text
Runner 不應該知道 pytest 是怎麼被呼叫的。
Runner 只需要知道：我把測試交給 Backend，Backend 回傳結果。
```

這讓未來可以演進成：

```text
SubprocessBackend
DockerBackend
RemoteBackend
```

而不需要大幅修改 Runner。

---

### 3. 為什麼需要 ExecutionResult？

如果直接回傳 subprocess 的 return code，例如：

```python
0
1
```

短期很簡單，但語意不清楚。

因此 v1 使用 `ExecutionResult` 封裝結果，例如：

```text
success: bool
exit_code: int
stdout: str
stderr: str
duration: float
```

這樣未來要加入報告、統計、儲存、分析時，會比較容易擴充。

---

## Trade-offs

### 優點

1. **架構簡單**

   * 適合 MVP。
   * 容易實作。
   * 容易用 UML 表達。

2. **責任開始分離**

   * CLI 負責輸入。
   * TestRunner 負責流程協調。
   * Backend 負責執行測試。
   * ExecutionResult 負責承載結果。

3. **保留未來演進空間**

   * 未來可以替換 Backend。
   * 未來可以加入 Reporter。
   * 未來可以加入 Docker、Parallel、Analytics。

### 缺點

1. **多了一點抽象**

   * 對 v1 來說，`TestRunner` 和 `PytestBackend` 可能看起來有點多餘。
   * 如果只跑一個 pytest，直接 subprocess 也能完成。

2. **還不是完整架構**

   * Backend 尚未抽成 interface。
   * Reporter 尚未獨立。
   * CLI 與 Runner 仍可能有部分耦合。

3. **擴充能力有限**

   * 目前只能跑單一測試檔。
   * 無法批次執行。
   * 無法平行執行。
   * 無法保存歷史結果。

---

## Current Limitations

目前架構仍存在一些限制：

1. 一次只能執行一個測試。
2. Backend 不可替換。
3. CLI 與 Runner 的責任尚未完全分離。
4. 沒有測試發現（Discovery）。
5. 沒有平行執行能力。
6. 沒有統計分析或測試報告。
7. 沒有 retry 機制。
8. 沒有 timeout 控制。
9. 沒有歷史執行紀錄。
10. 沒有 standardized reporting format，例如 JSON、HTML、Allure。

---

## Evolution

v1 是整個 LeetCode Runner 的起點。

它的重點不是架構完整，而是先定義最小核心流程：

```text
給定一個測試檔
 ↓
執行 pytest
 ↓
取得結果
 ↓
輸出結果
```

從 System Design 的角度看，v1 解決的是：

```text
如何把「手動執行 pytest」包裝成一個可重複使用的 Runner？
```

在沒有 Runner 之前，使用者可能直接執行：

```bash
pytest tests/test_two_sum.py
```

v1 則把它變成：

```bash
leetcode-runner run tests/test_two_sum.py
```

這個轉換的意義是：

```text
從 command usage
變成 system entry point
```

也就是說，v1 不是只是在包一層 CLI，而是在建立未來 Test Platform 的第一個入口。

---

## System Design Notes

這一版可以學到幾個 System Design 基礎概念：

### 1. System Boundary

v1 的系統邊界很小：

```text
Inside System:
- CLI
- TestRunner
- PytestBackend
- ExecutionResult

Outside System:
- pytest
- test files
- operating system subprocess
```

這讓我們開始分辨：

```text
哪些東西是自己系統的一部分？
哪些東西是外部依賴？
```

---

### 2. Responsibility Separation

v1 開始練習責任切分：

```text
CLI:
負責接收使用者輸入

TestRunner:
負責協調流程

PytestBackend:
負責執行 pytest

ExecutionResult:
負責封裝結果
```

這是日後走向 Test Infra / Platform 的基礎。

---

### 3. Abstraction Boundary

雖然 v1 還沒有正式的 Backend Interface，但已經開始有抽象邊界：

```text
TestRunner 不直接依賴 subprocess。
TestRunner 依賴 PytestBackend。
```

這代表未來可以進一步演進成：

```text
TestRunner -> Backend Interface -> PytestBackend
                                  -> DockerBackend
                                  -> RemoteBackend
```

---

### 4. Failure Handling

v1 的 failure handling 還很陽春，只能透過 pytest exit code 判斷成功或失敗。

例如：

```text
exit_code = 0  -> success
exit_code != 0 -> failed
```

但這已經是 failure modeling 的第一步。

未來可以再區分：

```text
Test Failed
Execution Error
Timeout
Environment Error
Docker Error
Invalid Test Path
```

---

### 5. Observability

v1 的 observability 很有限，只能透過 terminal output 觀察結果。

目前能觀察：

```text
- 測試是否成功
- exit code
- stdout
- stderr
```

目前不能觀察：

```text
- 歷史趨勢
- flaky test
- 平均執行時間
- failure rate
- slowest tests
```

這會成為後續版本加入 Reporter、Storage、Analytics 的原因。

---

## Next Version

Version 2 預計改善：

1. 將 CLI 與 Runner 進一步解耦。
2. 使用 Typer 取代 argparse。
3. 建立更清楚的 Runner 責任分工。
4. 加入更明確的 ExecutionRequest。
5. 為未來支援多種 Backend 預留擴充能力。
6. 開始區分輸入模型與執行模型。
7. 讓 Runner 不再直接依賴 raw CLI arguments。

v2 的核心演進方向會是：

```text
CLI args
 ↓
ExecutionRequest
 ↓
Runner
 ↓
Backend
 ↓
ExecutionResult
```

---

## UML Files

本版本 UML 包含：

* `component.mmd`：系統元件組成。
* `class.mmd`：核心類別與依賴關係。
* `sequence.mmd`：一次測試執行流程。
* `activity.mmd`：完整執行流程。

---

## Summary

v1 的重點不是做出完整平台，而是建立最小可運作的 Runner。

這一版學到的 System Design 核心是：

```text
從一個 command
抽象成一個 system entry point
```

也就是從：

```bash
pytest tests/test_two_sum.py
```

演進成：

```bash
leetcode-runner run tests/test_two_sum.py
```

這個小改變代表系統開始有自己的邊界、責任分工與未來演進空間。
