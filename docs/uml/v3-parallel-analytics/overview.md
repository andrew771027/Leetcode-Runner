# Version 3 - Discovery, Parallel Execution and Analytics

## Goal

Version 3 的目標是讓 LeetCode Runner 從「一次執行一個測試」進化成「可以發現、執行、彙整多個測試」。

相較於 Version 2：

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

Version 3 改為：

```text
CLI
 ↓
Runner
 ↓
TestDiscovery
 ↓
Multiple ExecutionRequests
 ↓
ParallelExecutor
 ↓
Backend
 ↓
Multiple ExecutionResults
 ↓
ResultAggregator / AnalyticsReporter
```

此版本開始具備 Test Infrastructure 的雛形：

* 自動發現測試
* 建立多個 ExecutionRequest
* 平行執行測試
* 彙整測試結果
* 產生簡單統計資訊

---

## Requirements

### Functional Requirements

本版本需要支援：

1. 使用者可以透過 CLI 指定測試目錄。
2. 系統可以自動發現目錄中的測試檔案。
3. 系統可以將多個測試檔案轉換成多個 `ExecutionRequest`。
4. 系統可以平行執行多個測試。
5. 系統可以收集多個 `ExecutionResult`。
6. 系統可以彙整測試結果。
7. 系統可以產生基本 summary。
8. 系統可以顯示簡單 analytics，例如總數、成功數、失敗數、平均執行時間、最慢測試。

### Non-functional Requirements

本版本開始重視：

1. **Scalability**

   * 從單一測試擴展到多個測試。
   * 開始處理批次任務。

2. **Throughput**

   * 透過平行執行縮短總測試時間。

3. **Observability**

   * 不只知道一個測試成功或失敗，而是知道整批測試的狀態。

4. **Separation of Concerns**

   * Discovery 負責找測試。
   * Executor 負責執行。
   * Aggregator 負責彙整。
   * AnalyticsReporter 負責分析與顯示。

5. **Extensibility**

   * 為未來 Docker Backend、Registry、Config、Reporter 預留空間。

---

## Architecture

本版本包含：

* CLI
* Runner
* TestDiscovery
* ExecutionRequest
* ParallelExecutor
* PytestBackend
* ExecutionResult
* ResultAggregator
* AnalyticsReporter

新增核心元件：

* TestDiscovery
* ParallelExecutor
* ResultAggregator
* AnalyticsReporter

整體架構如下：

```text
User
 ↓
CLI
 ↓
Runner
 ↓
TestDiscovery
 ↓
List[TestFile]
 ↓
List[ExecutionRequest]
 ↓
ParallelExecutor
 ↓
PytestBackend
 ↓
List[ExecutionResult]
 ↓
ResultAggregator
 ↓
Summary
 ↓
AnalyticsReporter
 ↓
Console Output
```

---

## Component Responsibilities

### CLI

CLI 負責：

```text
- Parse command
- 接收 test directory
- 呼叫 Runner
- 顯示最終結果
```

CLI 不負責：

```text
- 掃描測試檔案
- 建立所有 execution requests
- 平行執行
- 彙整結果
- 計算 analytics
```

---

### Runner

Runner 在 v3 成為真正的 orchestrator。

Runner 負責：

```text
- 呼叫 TestDiscovery
- 將 discovered tests 轉成 ExecutionRequests
- 呼叫 ParallelExecutor
- 收集 ExecutionResults
- 呼叫 ResultAggregator
- 呼叫 AnalyticsReporter
```

Runner 不負責：

```text
- 實際執行 pytest
- 直接操作 subprocess
- 直接計算底層測試細節
```

---

### TestDiscovery

TestDiscovery 負責：

```text
- 掃描測試目錄
- 找出符合規則的測試檔案
- 回傳 test file list
```

例如：

```text
tests/test_two_sum.py
tests/test_valid_parentheses.py
tests/test_merge_two_lists.py
```

它解決的問題是：

```text
使用者不需要一個一個指定測試檔。
```

---

### ExecutionRequest

在 v3 中，`ExecutionRequest` 從單一 request model 變成批次執行的基本單位。

```text
one test file -> one ExecutionRequest
```

也就是：

```text
List[TestFile] -> List[ExecutionRequest]
```

這讓後面的 ParallelExecutor 可以用一致的方式處理每個測試任務。

---

### ParallelExecutor

ParallelExecutor 負責：

```text
- 接收多個 ExecutionRequest
- 將 request 分派給 Backend
- 平行執行測試
- 收集多個 ExecutionResult
```

它是 v3 的核心基礎設施元件。

在 v2：

```text
one request -> one result
```

在 v3：

```text
many requests -> many results
```

---

### PytestBackend

PytestBackend 仍然負責實際執行 pytest。

不同的是，v3 中它會被 ParallelExecutor 多次呼叫：

```text
ExecutionRequest A -> PytestBackend -> ExecutionResult A
ExecutionRequest B -> PytestBackend -> ExecutionResult B
ExecutionRequest C -> PytestBackend -> ExecutionResult C
```

---

### ResultAggregator

ResultAggregator 負責將多個結果彙整成 summary。

例如：

```text
total: 10
passed: 8
failed: 2
success_rate: 80%
total_duration: 15.2s
```

它的重點是：

```text
從 individual result 轉成 batch summary。
```

---

### AnalyticsReporter

AnalyticsReporter 負責顯示統計資訊。

例如：

```text
- pass rate
- average duration
- slowest test
- failed tests
```

它和 Aggregator 的差異是：

```text
Aggregator 負責計算 summary。
AnalyticsReporter 負責呈現與解讀。
```

---

## Design Decisions

### 1. 為什麼加入 TestDiscovery？

在 v2，使用者必須指定單一測試檔：

```bash
leetcode-runner run tests/test_two_sum.py
```

這適合單一測試，但不適合一整批題目。

v3 加入 TestDiscovery 後，可以改成：

```bash
leetcode-runner run tests/
```

系統自動找出所有測試檔。

這代表 Runner 從 command executor 開始演進成 test infrastructure。

---

### 2. 為什麼加入 ParallelExecutor？

當測試數量增加時，逐一執行會變慢：

```text
test A: 2s
test B: 3s
test C: 4s

sequential total: 9s
```

如果平行執行：

```text
parallel total: about 4s
```

因此 v3 加入 ParallelExecutor，開始處理 throughput 問題。

這是 System Design 中很重要的轉變：

```text
從 correctness only
變成 correctness + performance
```

---

### 3. 為什麼 Runner 不自己做 parallel？

Runner 如果同時負責 discovery、parallel、backend、aggregation，會變得太胖。

因此把平行執行拆成 `ParallelExecutor`：

```text
Runner coordinates.
ParallelExecutor executes batch requests.
```

這樣 Runner 保持 orchestration 角色，而不是塞滿 execution details。

---

### 4. 為什麼加入 ResultAggregator？

多個測試結果如果只是印出來，使用者仍然很難理解整體狀況。

因此 v3 加入 ResultAggregator，把：

```text
List[ExecutionResult]
```

轉換成：

```text
Summary
```

這讓系統可以回答：

```text
總共跑幾個？
成功幾個？
失敗幾個？
成功率多少？
總耗時多少？
```

---

### 5. 為什麼加入 AnalyticsReporter？

ResultAggregator 解決的是「彙整」。

AnalyticsReporter 解決的是「觀察」。

它讓使用者不只看到 pass/fail，還能開始看到：

```text
哪些測試最慢？
平均執行時間是多少？
失敗率是多少？
```

這是 observability 的起點。

---

## Trade-offs

### 優點

1. **支援批次執行**

   * 不再只能跑一個測試。
   * 可以處理整個 test directory。

2. **執行效率提高**

   * ParallelExecutor 可以縮短整體測試時間。

3. **架構更接近 Test Infra**

   * Discovery、Execution、Aggregation、Analytics 開始分層。

4. **觀察能力提升**

   * 不只看到單一測試結果。
   * 可以看到整批測試的 summary。

5. **Runner 成為 Orchestrator**

   * Runner 開始負責協調完整 pipeline。

### 缺點

1. **系統複雜度提高**

   * 從 single flow 變成 batch pipeline。
   * 需要處理多個 request 和 result。

2. **Parallel Execution 會帶來新問題**

   * log 順序可能混亂。
   * 錯誤追蹤較困難。
   * 資源使用量增加。
   * 測試之間如果有共享狀態，可能互相影響。

3. **Aggregator / Reporter 邊界需要定義**

   * 哪些邏輯屬於 aggregation？
   * 哪些邏輯屬於 reporting？
   * 初期可能會混在一起。

4. **Backend 仍然固定**

   * 目前還不能切換成 DockerBackend。
   * 測試環境仍然依賴本機。

---

## Current Limitations

目前仍然：

1. Backend 固定為 PytestBackend。
2. ParallelExecutor 邏輯仍然簡單。
3. 尚未支援 Docker Backend。
4. 尚未支援 Config。
5. 尚未支援 Registry。
6. Report 仍然偏向 console output。
7. Analytics 還只是基本統計。
8. 沒有 retry。
9. 沒有 timeout。
10. 沒有 flaky test detection。
11. 沒有歷史趨勢分析。
12. 沒有環境隔離。
13. 沒有 queue-based execution。
14. 沒有 worker model。

---

## Evolution from Version 2

### Version 2

v2 的核心是：

```text
one request -> one result
```

架構重點是：

```text
CLI input
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
如何把 CLI input 和 Runner 解耦？
```

---

### Version 3

v3 的核心是：

```text
many requests -> many results -> summary / analytics
```

架構重點是：

```text
Discovery
 ↓
Multiple ExecutionRequests
 ↓
Parallel Execution
 ↓
Multiple ExecutionResults
 ↓
Aggregation
 ↓
Analytics
```

v3 解決的是：

```text
如何讓 Runner 處理一批測試，而不是只處理一個測試？
```

---

### 主要演進

v2 到 v3 的最大變化是：

```text
從 single execution
變成 batch orchestration
```

也就是：

```text
單一任務執行器
 ↓
批次測試協調器
```

這是從 tool 走向 infrastructure 的重要分界點。

---

## System Design Notes

### 1. Batch Processing

v3 開始引入 batch processing 概念。

在 v2：

```text
Input: one ExecutionRequest
Output: one ExecutionResult
```

在 v3：

```text
Input: List[ExecutionRequest]
Output: List[ExecutionResult]
Output Summary: AggregatedResult
```

這讓系統開始需要思考：

```text
如何建立多個任務？
如何分派多個任務？
如何收集多個結果？
如何彙整整批結果？
```

---

### 2. Orchestration Pipeline

v3 的 Runner 不再只是簡單呼叫 Backend，而是協調一條 pipeline：

```text
Discover
 ↓
Build Requests
 ↓
Execute in Parallel
 ↓
Collect Results
 ↓
Aggregate
 ↓
Report
```

這就是 orchestration 的雛形。

Runner 的角色變成：

```text
不是自己做所有事，
而是安排誰在什麼階段做什麼事。
```

---

### 3. Scalability

v3 開始處理 scale 的第一個問題：

```text
測試數量變多時怎麼辦？
```

v1 / v2 都只處理一個測試，所以 scale 不明顯。

v3 開始處理：

```text
10 個測試
100 個測試
1000 個測試
```

雖然目前只是 local parallel，但它已經引入 scalable thinking。

---

### 4. Throughput vs Complexity

ParallelExecutor 提高 throughput，但也帶來 complexity。

得到的是：

```text
更快的總執行時間
```

付出的代價是：

```text
更複雜的錯誤處理
更複雜的 log 管理
更高的資源使用
可能的 shared state 問題
```

這是典型的 System Design trade-off。

---

### 5. Observability

v3 開始從單一結果走向整體觀察。

v2 只能回答：

```text
這個測試有沒有過？
```

v3 可以回答：

```text
總共跑幾個？
過幾個？
失敗幾個？
成功率多少？
哪個最慢？
平均耗時多少？
```

這是 Test Infrastructure 很重要的一步。

---

### 6. Data Flow

v3 的資料流開始變清楚：

```text
Test files
 ↓
ExecutionRequests
 ↓
ExecutionResults
 ↓
Summary
 ↓
Analytics Output
```

這代表系統不只是執行 command，而是開始有資料管線。

---

### 7. Failure Model

v3 的 failure model 比 v2 更複雜。

需要開始思考：

```text
如果某一個測試失敗，要不要中斷全部？
如果某一個測試 timeout，要不要繼續其他測試？
如果 discovery 找不到測試，是錯誤還是空結果？
如果 parallel worker 壞掉，怎麼處理？
```

v3 可以先採用簡單策略：

```text
單一測試失敗不停止整批執行。
所有結果都收集完，再統一產生 summary。
```

這樣比較適合 test runner。

---

## Next Version

Version 4 預計加入：

* BackendRegistry
* ReporterRegistry
* RunnerBuilder
* ConfigLoader
* DockerBackend
* 更清楚的組裝流程

Version 4 的目標是降低耦合，讓 Backend、Reporter、Config 可以被替換與擴充。

v4 的核心演進方向會是：

```text
Hard-coded components
 ↓
Config-driven / Registry-driven components
```

也就是從：

```text
Runner 手動組裝所有東西
```

演進成：

```text
RunnerBuilder 根據 config 組裝 Runner
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

v3 的重點是讓 LeetCode Runner 從單一測試執行器，演進成批次測試協調器。

這一版學到的 System Design 核心是：

```text
從 single execution
演進成 batch orchestration。
```

也就是從：

```text
one request -> one result
```

演進成：

```text
many requests -> many results -> summary / analytics
```

這代表 LeetCode Runner 開始具備 Test Infrastructure 的雛形。
