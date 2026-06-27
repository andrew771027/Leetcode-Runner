# Version 3 - Discovery, Parallel Execution and Analytics

## Goal

Version 3 的目標是讓 LeetCode Runner 從「一次執行一個測試」進化成「可以發現、執行、彙整多個測試」。

相較於 Version 2：

```text
CLI
 ↓
Runner
 ↓
Backend
```

Version 3 改為：

```text
CLI
 ↓
Runner
 ↓
Discovery
 ↓
ParallelExecutor
 ↓
Backend
 ↓
Aggregator / Analytics
```

此版本開始具備 Test Infrastructure 的雛形：

* 自動發現測試
* 建立多個 ExecutionRequest
* 平行執行測試
* 彙整測試結果
* 產生簡單統計資訊

---

# Architecture

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

新增：

* TestDiscovery
* ParallelExecutor
* ResultAggregator
* AnalyticsReporter

---

# Design Decisions

本版本最大的改變是：

**Runner 不再只負責執行單一測試，而是負責協調整個測試流程。**

Runner 的職責變成：

1. 呼叫 TestDiscovery 找出測試檔案。
2. 將測試檔案轉成多個 ExecutionRequest。
3. 將多個 Request 交給 ParallelExecutor。
4. 收集多個 ExecutionResult。
5. 透過 ResultAggregator 產生 summary。
6. 透過 AnalyticsReporter 顯示統計資訊。

---

# Key Concept

Version 3 開始引入「批次執行」的概念。

在 Version 2：

```text
one request → one result
```

在 Version 3：

```text
many requests → many results → summary / analytics
```

這是從 Script 走向 Test Infrastructure 的重要分界點。

---

# Current Limitations

目前仍然：

1. Backend 固定為 PytestBackend。
2. ParallelExecutor 邏輯仍然簡單。
3. 尚未支援 Docker Backend。
4. 尚未支援 Config。
5. 尚未支援 Registry。
6. Report 仍然偏向 console output。
7. Analytics 還只是基本統計。

---

# Next Version

Version 4 預計加入：

* BackendRegistry
* ReporterRegistry
* RunnerBuilder
* ConfigLoader
* DockerBackend
* 更清楚的組裝流程

Version 4 的目標是降低耦合，讓 Backend、Reporter、Config 可以被替換與擴充。

---

# UML Files

* component.mmd
* class.mmd
* sequence.mmd
* activity.mmd
