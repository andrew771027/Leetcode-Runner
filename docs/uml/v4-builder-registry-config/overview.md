# Version 4 - Builder, Registry and Config

## Goal

Version 4 的目標是降低模組之間的耦合，讓 LeetCode Runner 從「固定流程的批次執行器」進化成「可組裝的 Test Runner Framework」。

相較於 Version 3：

```text
CLI
 ↓
Runner
 ↓
Discovery
 ↓
ParallelExecutor
 ↓
PytestBackend
 ↓
Aggregator / Analytics
```

Version 4 改為：

```text
CLI
 ↓
ConfigLoader
 ↓
RunnerBuilder
 ↓
Registry
 ↓
Runner
 ↓
Discovery / Executor / Backend / Reporter
```

此版本的核心不是增加更多功能，而是讓既有功能可以被替換、註冊與組裝。

---

# Architecture

本版本包含：

* CLI
* ConfigLoader
* RunnerConfig
* RunnerBuilder
* BackendRegistry
* ReporterRegistry
* Runner
* TestDiscovery
* ParallelExecutor
* Backend Interface
* SubprocessBackend
* DockerBackend
* ResultAggregator
* Reporter Interface
* ConsoleReporter
* AnalyticsReporter
* ExecutionRequest
* ExecutionResult
* Summary

新增：

* ConfigLoader
* RunnerConfig
* RunnerBuilder
* BackendRegistry
* ReporterRegistry
* Backend Interface
* Reporter Interface
* DockerBackend

---

# Design Decisions

本版本最大的改變是：

**將建立物件的責任從 Runner 中移出。**

在 Version 3，Runner 仍然知道很多具體元件：

* TestDiscovery
* ParallelExecutor
* PytestBackend
* ResultAggregator
* AnalyticsReporter

到了 Version 4，Runner 不再自己建立這些物件，而是透過 RunnerBuilder 組裝完成。

---

# Key Concept

Version 4 開始引入兩個重要設計：

## Builder Pattern

RunnerBuilder 負責根據 RunnerConfig 建立 Runner。

Runner 不需要知道自己是如何被組裝出來的。

## Registry Pattern

BackendRegistry 負責管理不同 Backend。

例如：

* subprocess
* docker

ReporterRegistry 負責管理不同 Reporter。

例如：

* console
* analytics

---

# Benefits

Version 4 的好處是：

1. 新增 Backend 不需要修改 Runner。
2. 新增 Reporter 不需要修改 Runner。
3. Config 可以控制執行模式。
4. Runner 的責任更單純。
5. 架構更接近 Test Infrastructure / Developer Productivity Tooling。

---

# Current Limitations

目前仍然：

1. Registry 還是 local in-memory registry。
2. Config 尚未支援複雜 schema validation。
3. DockerBackend 還是簡化版本。
4. 沒有 API Server。
5. 沒有 Scheduler。
6. 沒有 Persistent Storage。
7. 沒有 Web UI。

---

# Next Version

Version 5 預計加入：

* API Server
* Job Scheduler
* Persistent Storage
* Web UI
* Async Execution
* Remote Worker
* Test History

Version 5 的目標是從 Test Runner Framework 進一步變成 Test Platform。

---

# UML Files

* component.mmd
* class.mmd
* sequence.mmd
* activity.mmd
