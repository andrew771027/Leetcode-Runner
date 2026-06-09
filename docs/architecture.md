# Leetcode Runner Architecture

## Overview

Leetcode Runner is **not simply a pytest wrapper**.

Its goal is to become a lightweight **Test Execution Platform**, responsible for:

- Test discovery
- Test execution
- Workflow orchestration
- Middleware processing
- Event publishing
- Metrics collection
- Artifact generation
- Reporting

Instead of embedding all responsibilities inside `Runner`, responsibilities are separated into independent components following SOLID and Clean Architecture principles.

---

# High-level Architecture

```text
                CLI
                 │
                 ▼
           RunnerConfig
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
WorkflowBuilder      EventBusBuilder
      │                     │
      ▼                     ▼
WorkflowPipeline       EventBus
      │                     │
      ▼                     ▼
 Discover              Subscribers
 Execute                   │
 Artifact                  │
 History                   │
 Metrics                   │
 Report                    │
      │                    │
      └──────────┬─────────┘
                 ▼
               Runner
                 │
                 ▼
            ExecutionContext
```

---

# Layer Structure

```
CLI
        │
        ▼
Runner
        │
        ▼
Workflow Pipeline
        │
        ▼
Stage
        │
        ▼
Backend
        │
        ▼
Middleware
        │
        ▼
Execution
```

---

# Project Structure

```
runner/

workflow/

events/

backends/

middleware/

reporters/

factories/

services/

contracts/

models/
```

Each folder owns a single responsibility.

---

# Workflow

Workflow defines **what should happen**.

Example:

```
Discover
    ↓
Execute
    ↓
Artifact
    ↓
History
    ↓
Metrics
    ↓
Report
```

Workflow is configurable through `RunnerConfig`.

---

# Middleware

Middleware defines **how execution should happen**.

Example:

```
Retry
    ↓
Benchmark
    ↓
Timeout
    ↓
Backend
```

Each middleware is independent and composable.

---

# Backend

Backend executes actual tests.

Current implementations:

```
ExecutionBackend

    ▲

    ├── SubprocessBackend

    └── DockerBackend
```

Future:

- KubernetesBackend
- RemoteBackend
- SSHBackend

---

# Event Bus

Execution emits events instead of directly writing files.

```
ExecuteStage

        │

        ▼

    EventBus

        │

 ┌──────┼────────┐

 ▼      ▼        ▼

File   Metrics   Future
Logger Collector Slack
```

Publisher does not know who consumes the event.

---

# Reporter

Reporter is responsible for presentation only.

Examples:

- ConsoleReporter
- JsonReporter
- HtmlReporter
- FileReporter

---

# Stores

Stores are persistence components.

Examples:

```
ArtifactStore

↓

report.json
```

```
HistoryStore

↓

history.jsonl
```

Future:

- SQLiteStore
- PostgreSQLStore
- S3Store

---

# Builder Pattern

Builder assembles complex objects.

Examples:

```
RunnerBuilder

↓

Backend
```

```
WorkflowBuilder

↓

WorkflowPipeline
```

```
EventBusBuilder

↓

EventBus
```

---

# Registry Pattern

Registry enables plugin discovery.

Examples:

```
BackendRegistry

ReporterRegistry

MiddlewareRegistry

StageRegistry

SubscriberRegistry
```

New plugins can be added without modifying existing logic.

---

# Execution Flow

```
CLI

↓

Runner

↓

WorkflowPipeline

↓

Discover

↓

Execute

↓

Middleware

↓

Backend

↓

TestResult

↓

Artifact

↓

History

↓

Metrics

↓

Report
```

---

# Design Principles

- Single Responsibility Principle
- Open/Closed Principle
- Dependency Injection
- Builder Pattern
- Registry Pattern
- Workflow Pattern
- Event-Driven Architecture
- Plugin Architecture

---

# Current Status (v4.9)

Implemented:

- Workflow Pipeline
- Middleware Pipeline
- Backend abstraction
- Builder
- Registry
- Event Bus
- Subscribers
- Metrics
- Artifact
- History
- Reporter

Planned (v5.x):

- YAML configuration
- DAG workflow
- Remote execution
- Distributed execution
- Web UI
- Scheduler