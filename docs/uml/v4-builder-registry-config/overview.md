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
RunnerConfig
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

## Requirements

### Functional Requirements

本版本需要支援：

1. 使用者可以透過 CLI 指定 config。
2. 系統可以透過 `ConfigLoader` 載入設定。
3. 系統可以將設定轉換成 `RunnerConfig`。
4. `RunnerBuilder` 可以根據 `RunnerConfig` 組裝 Runner。
5. 系統可以透過 `BackendRegistry` 選擇 Backend。
6. 系統可以透過 `ReporterRegistry` 選擇 Reporter。
7. Runner 可以使用被注入的 Discovery、Executor、Backend、Aggregator、Reporter。
8. 系統可以支援 `SubprocessBackend`。
9. 系統可以支援簡化版 `DockerBackend`。
10. 系統可以支援 `ConsoleReporter` 與 `AnalyticsReporter`。

### Non-functional Requirements

本版本開始重視：

1. **Configurability**

   * 使用者可以透過設定控制執行模式。

2. **Extensibility**

   * 新增 Backend 不應該修改 Runner。
   * 新增 Reporter 不應該修改 Runner。

3. **Low Coupling**

   * Runner 不應該知道具體 Backend 與 Reporter 的建立細節。

4. **Dependency Injection**

   * Runner 依賴被組裝好的抽象元件，而不是自己 new 出所有東西。

5. **Framework Thinking**

   * 系統不只是「執行測試」，而是提供一個可以組裝測試流程的框架。

---

## Architecture

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

新增核心元件：

* ConfigLoader
* RunnerConfig
* RunnerBuilder
* BackendRegistry
* ReporterRegistry
* Backend Interface
* Reporter Interface
* DockerBackend

整體架構如下：

```text
User
 ↓
CLI
 ↓
ConfigLoader
 ↓
RunnerConfig
 ↓
RunnerBuilder
 ↓
BackendRegistry / ReporterRegistry
 ↓
Runner
 ↓
TestDiscovery
 ↓
ParallelExecutor
 ↓
Backend Interface
 ↓
SubprocessBackend / DockerBackend
 ↓
ExecutionResult
 ↓
ResultAggregator
 ↓
Reporter Interface
 ↓
ConsoleReporter / AnalyticsReporter
```

---

## Component Responsibilities

### CLI

CLI 負責：

```text
- Parse command
- 接收 config path
- 呼叫 ConfigLoader
- 呼叫 RunnerBuilder
- 觸發 Runner 執行
```

CLI 不負責：

```text
- 建立 Backend
- 建立 Reporter
- 決定使用哪個執行模式
- 組裝整個 Runner
```

---

### ConfigLoader

ConfigLoader 負責：

```text
- 讀取 config file
- 解析設定內容
- 建立 RunnerConfig
```

它把外部設定轉成系統內部可理解的 model。

---

### RunnerConfig

RunnerConfig 負責描述 Runner 的組裝需求。

例如：

```text
backend: subprocess
reporters:
  - console
  - analytics
parallelism: 4
test_directory: tests/
timeout: 60
docker_image: python:3.12
```

RunnerConfig 的意義是：

```text
把執行策略從 code 移到 configuration。
```

---

### RunnerBuilder

RunnerBuilder 負責根據 `RunnerConfig` 建立 Runner。

它會處理：

```text
- 建立 TestDiscovery
- 建立 ParallelExecutor
- 從 BackendRegistry 取得 Backend
- 從 ReporterRegistry 取得 Reporters
- 建立 ResultAggregator
- 將這些元件注入 Runner
```

RunnerBuilder 的存在讓 Runner 不需要知道自己是如何被組裝出來的。

---

### BackendRegistry

BackendRegistry 負責管理 Backend。

例如：

```text
subprocess -> SubprocessBackend
docker     -> DockerBackend
```

它讓系統可以透過名稱取得對應 Backend。

新增 Backend 時，只需要註冊：

```text
remote -> RemoteBackend
```

而不需要修改 Runner。

---

### ReporterRegistry

ReporterRegistry 負責管理 Reporter。

例如：

```text
console   -> ConsoleReporter
analytics -> AnalyticsReporter
```

新增 Reporter 時，只需要註冊：

```text
html -> HtmlReporter
json -> JsonReporter
```

而不需要修改 Runner。

---

### Backend Interface

Backend Interface 定義所有 Backend 必須遵守的行為。

例如：

```text
execute(request: ExecutionRequest) -> ExecutionResult
```

Runner 和 ParallelExecutor 依賴的是 interface，而不是具體 Backend。

這讓系統可以支援：

```text
SubprocessBackend
DockerBackend
RemoteBackend
```

---

### Reporter Interface

Reporter Interface 定義所有 Reporter 必須遵守的行為。

例如：

```text
report(summary: Summary) -> None
```

或：

```text
report(results: List[ExecutionResult], summary: Summary) -> None
```

Runner 不需要知道 Reporter 是 console、analytics、html 還是 json。

---

### Runner

Runner 在 v4 的責任更單純。

Runner 負責：

```text
- 使用 TestDiscovery 找測試
- 建立 ExecutionRequests
- 使用 ParallelExecutor 執行 requests
- 使用 ResultAggregator 彙整 results
- 呼叫 Reporters 顯示結果
```

Runner 不負責：

```text
- 建立 Backend
- 建立 Reporter
- 讀取 Config
- 管理 Registry
- 決定實際使用哪個 Backend class
```

---

## Design Decisions

### 1. 為什麼將物件建立責任移出 Runner？

在 v3，Runner 可能會直接知道：

```text
TestDiscovery
ParallelExecutor
PytestBackend
ResultAggregator
AnalyticsReporter
```

這代表 Runner 同時負責：

```text
- orchestration
- object creation
- dependency selection
```

這會讓 Runner 越來越胖。

v4 將 object creation 移到 `RunnerBuilder`，讓 Runner 專注在 orchestration。

---

### 2. 為什麼需要 RunnerBuilder？

如果沒有 Builder，CLI 可能需要自己建立所有元件：

```text
CLI creates ConfigLoader
CLI creates Backend
CLI creates Reporter
CLI creates Executor
CLI creates Runner
```

這會讓 CLI 太了解內部架構。

因此 v4 使用 RunnerBuilder：

```text
RunnerConfig -> RunnerBuilder -> Runner
```

讓建立流程集中在一個地方。

---

### 3. 為什麼需要 Registry？

如果沒有 Registry，選擇 Backend 可能會寫成：

```python
if backend_name == "subprocess":
    backend = SubprocessBackend()
elif backend_name == "docker":
    backend = DockerBackend()
```

短期可行，但未來 Backend 增加時，會不斷修改選擇邏輯。

Registry 讓系統變成：

```text
backend = backend_registry.get("docker")
```

新增 Backend 時，只需要註冊，不需要修改 Runner 或 Builder 的核心流程。

---

### 4. 為什麼需要 Backend Interface？

v3 的 Backend 還偏向具體實作。

v4 引入 Backend Interface，讓 Runner 和 Executor 不再依賴具體類別。

這是重要的架構轉變：

```text
依賴具體實作
 ↓
依賴抽象介面
```

也就是：

```text
ParallelExecutor -> Backend Interface
                 -> SubprocessBackend
                 -> DockerBackend
```

---

### 5. 為什麼需要 Config？

在 v3，很多設定可能被寫死在程式中，例如：

```text
backend = PytestBackend()
parallelism = 4
reporter = AnalyticsReporter()
```

v4 將這些變成 config：

```text
backend: docker
parallelism: 4
reporters:
  - console
  - analytics
```

這讓使用者不需要修改 code，就能改變執行模式。

---

### 6. 為什麼加入 DockerBackend？

DockerBackend 代表環境隔離的開始。

SubprocessBackend 依賴本機環境：

```text
local python
local pytest
local dependencies
```

DockerBackend 則可以把測試放在容器中執行：

```text
docker image
isolated environment
repeatable execution
```

這讓 Runner 更接近真實 Test Infrastructure。

---

## Trade-offs

### 優點

1. **Runner 更單純**

   * Runner 專注在 orchestration。
   * 不再負責建立具體元件。

2. **Backend 可替換**

   * 可以用 subprocess。
   * 可以用 docker。
   * 未來可以用 remote worker。

3. **Reporter 可擴充**

   * 可以輸出 console。
   * 可以輸出 analytics。
   * 未來可以輸出 html、json、allure。

4. **Config-driven**

   * 使用者可以透過設定切換執行模式。
   * 減少 hard-coded behavior。

5. **更接近 Framework**

   * 系統不再只是固定工具。
   * 開始支援可組裝、可替換、可擴充。

### 缺點

1. **架構複雜度明顯上升**

   * Builder、Registry、Interface 對小系統來說偏重。

2. **初學者理解成本提高**

   * 需要理解 abstraction、dependency injection、registry、config。

3. **Over-engineering 風險**

   * 如果需求永遠只有本機 pytest，v4 的設計可能太重。

4. **Debug 路徑變長**

   * 錯誤可能發生在 ConfigLoader、Builder、Registry、Backend、Reporter 多個階段。

5. **Config validation 成為新問題**

   * config 寫錯時，需要清楚錯誤訊息。
   * 否則使用者會很難知道是哪裡設定錯。

---

## Current Limitations

目前仍然：

1. Registry 還是 local in-memory registry。
2. Config 尚未支援複雜 schema validation。
3. DockerBackend 還是簡化版本。
4. 沒有 API Server。
5. 沒有 Scheduler。
6. 沒有 Persistent Storage。
7. 沒有 Web UI。
8. 沒有 Remote Worker。
9. 沒有 Queue。
10. 沒有 Job State Management。
11. 沒有完整權限控管。
12. 沒有分散式執行。
13. 沒有長期 test history。

---

## Evolution from Version 3

### Version 3

v3 的核心是：

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
如何從單一測試執行，進化成批次測試協調？
```

---

### Version 4

v4 的核心是：

```text
Config
 ↓
Builder
 ↓
Registry
 ↓
Runner with injected components
```

v4 解決的是：

```text
如何讓 Runner 的元件可以被替換、註冊與組裝？
```

---

### 主要演進

v3 到 v4 的最大變化是：

```text
從 hard-coded pipeline
變成 configurable framework
```

也就是：

```text
Runner 知道具體元件
 ↓
Runner 依賴被注入的抽象元件
```

這代表架構從「工具」更接近「框架」。

---

## System Design Notes

### 1. Dependency Injection

v4 開始正式引入 Dependency Injection 的概念。

Runner 不再自己建立：

```text
Backend
Reporter
Executor
Aggregator
```

而是由外部組裝好後注入。

這讓 Runner 可以專注在：

```text
如何協調流程
```

而不是：

```text
如何建立每個物件
```

---

### 2. Open / Closed Principle

v4 的設計開始接近 Open / Closed Principle：

```text
Open for extension
Closed for modification
```

也就是：

```text
新增 Backend，可以透過 Registry 註冊。
新增 Reporter，可以透過 Registry 註冊。
Runner 本身不需要修改。
```

這是 Framework 設計很重要的基礎。

---

### 3. Config-driven Architecture

v4 將執行策略從 code 移到 config。

在 v3：

```text
程式碼決定使用哪個 backend。
```

在 v4：

```text
config 決定使用哪個 backend。
```

這讓系統更適合不同使用情境：

```text
local development -> subprocess backend
clean environment -> docker backend
CI pipeline -> docker backend + json reporter
developer console -> subprocess backend + console reporter
```

---

### 4. Plugin-like Architecture

Registry 讓系統開始接近 plugin architecture。

雖然 v4 的 Registry 還是 local in-memory，但概念已經出現：

```text
name -> implementation
```

例如：

```text
docker -> DockerBackend
console -> ConsoleReporter
analytics -> AnalyticsReporter
```

未來可以進一步演進成：

```text
external plugins
entry points
dynamic loading
remote executors
```

---

### 5. Framework Boundary

v4 的 LeetCode Runner 不再只是「一支 CLI 工具」。

它開始形成 framework boundary：

```text
Framework 提供：
- Runner lifecycle
- Backend interface
- Reporter interface
- Config model
- Registry mechanism
- Builder assembly

User / developer 提供：
- Backend implementation
- Reporter implementation
- Config choice
```

這是從 application thinking 走向 framework thinking 的轉變。

---

### 6. Complexity Management

v4 的核心其實不是新增功能，而是管理複雜度。

v3 的複雜度來自：

```text
多測試
平行執行
彙整
分析
```

v4 的複雜度來自：

```text
多種 backend
多種 reporter
多種 config
多種組裝方式
```

因此 v4 需要 Builder / Registry / Interface 來管理這些變化。

---

### 7. System Boundary Expansion

v4 的系統邊界比 v3 更大。

v3 的外部依賴主要是：

```text
pytest
local filesystem
subprocess
```

v4 開始加入：

```text
docker
config file
registry mechanism
```

這代表系統開始處理：

```text
execution environment
configuration source
component selection
```

---

### 8. Failure Model

v4 的 failure model 比 v3 更複雜。

除了測試失敗，現在還要處理：

```text
Config file not found
Invalid config format
Unknown backend name
Unknown reporter name
Docker image not found
Docker execution failed
Backend initialization failed
Reporter initialization failed
```

這代表錯誤不再只發生在 test execution，而會發生在 system assembly 階段。

因此 v4 應該開始區分：

```text
Configuration Error
Assembly Error
Execution Error
Test Failure
Reporting Error
```

---

## Next Version

Version 5 預計加入：

* API Server
* Job Scheduler
* Persistent Storage
* Web UI
* Async Execution
* Remote Worker
* Test History

Version 5 的目標是從 Test Runner Framework 進一步變成 Test Platform。

v5 的核心演進方向會是：

```text
Local framework
 ↓
Networked test platform
```

也就是從：

```text
CLI-triggered execution
```

演進成：

```text
API-triggered async job execution
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

v4 的重點不是增加更多測試功能，而是讓既有功能可以被組裝、替換與擴充。

這一版學到的 System Design 核心是：

```text
從 hard-coded pipeline
演進成 configurable framework。
```

也就是從：

```text
Runner knows concrete components
```

演進成：

```text
Runner depends on injected abstractions
```

這代表 LeetCode Runner 開始從 Test Runner Tool，進化成 Test Runner Framework。
