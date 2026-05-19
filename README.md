# LeetCode Runner — v1 → v3 Architecture Evolution

## 🎯 專案目標
建立一個可擴展的 LeetCode 測試框架，支援：
- 自動執行測試（pytest）
- Benchmark / Coverage
- 多種執行環境（local / docker / CI）

---

# 🥚 v1 — 初始版本（Basic CLI + subprocess）

## 🧩 架構
CLI (argparse)
    ↓
subprocess
    ↓
pytest

## ⚠️ 問題
- CLI 可讀性差
- Execution Environment 問題
- 架構耦合

---

# 🧱 v2 — 分層架構（Layered Architecture）

## 🧩 架構設計
CLI → Runner Core → Modules → Execution Layer

## 🎯 改進
- 分層設計（SoC）
- 使用 Typer
- 模組化功能

## ⚠️ 問題
- Execution Layer 仍耦合
- 無法支援 Docker / Remote / CI

---

# 🚀 v3 — 抽象化架構（Strategy Pattern）

## 🧩 架構設計
CLI → Orchestrator → Execution Backend → Tools

## 🧠 核心設計
- Orchestrator = 純邏輯
- Execution Backend = 可替換

## 🔌 Backend 類型
- SubprocessBackend
- DockerBackend
- RemoteBackend
- CIBackend

## 🎯 設計價值
- 解耦
- 可擴展
- 可測試
- Strategy Pattern

---

# 📊 三版本比較

| 面向 | v1 | v2 | v3 |
|------|----|----|----|
| 架構 | 無 | 分層 | 抽象 |
| 擴展性 | ❌ | ⚠️ | ✅ |
| 可測試 | ❌ | ⚠️ | ✅ |

---

# 🧭 下一步（v3.1）
- Backend 強化（timeout / retry）
- logging / error handling
- plugin system
