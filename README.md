# 🚀 RuntimeQueens — Autonomous Bug Verification Agent

RuntimeQueens is an autonomous system that **verifies whether a GitHub repository actually works in a clean environment**, and explains *why* it fails when it does.

Unlike code suggestion tools, RuntimeQueens **executes real code**, detects real failures, and reasons about them.

---

## ❓ The Problem

Many projects:
- work on a developer’s machine
- fail in clean environments
- rely on undeclared dependencies
- assume local import paths
- pass CI but break elsewhere

Tools like Copilot can *suggest fixes*, but they **cannot verify reality**.

---

## 💡 Our Solution

RuntimeQueens performs **end-to-end autonomous verification**:

1. Accepts a GitHub repository URL
2. Clones it safely
3. Runs it in a **clean Docker environment**
4. Captures execution / test logs
5. Analyzes failures using structured reasoning
6. Explains **why** the failure happened in plain English

---

## 🧠 What Makes RuntimeQueens Different

| Feature | RuntimeQueens | Copilot / CI |
|------|---------------|-------------|
| Clean OS execution | ✅ | ❌ |
| Detect missing packaging | ✅ | ❌ |
| Explain root cause | ✅ | ❌ |
| Distinguish non-bugs | ✅ | ❌ |
| Avoid hallucinations | ✅ | ❌ |

RuntimeQueens knows **when not to act** — a critical system property.

---

## 🧪 Example Demo Repository

We tested against:

🔗 https://github.com/okken/pytest-buggy-example

**Observed failure:**
- Tests fail during collection
- Missing local module (`sample`)
- Works locally but fails in clean Docker

**RuntimeQueens diagnosis:**
> “The project assumes a local module is available, but it is not packaged or installed correctly. This causes failures in clean environments.”

---

## 🛑 What RuntimeQueens Intentionally Does NOT Do

- ❌ Does not modify repositories automatically
- ❌ Does not hallucinate fixes
- ❌ Does not guess intent

All outputs are **deterministic, reproducible, and explainable**.

---

## 🏗️ Architecture Overview

