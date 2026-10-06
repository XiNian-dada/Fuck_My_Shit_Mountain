<div align="center">

![Fuck My Shit Mountain banner](assets/banner-en.png)

# Fuck My Shit Mountain

**For when the project runs, but you can feel the mountain shifting under your feet.**  
An evidence-based, multidimensional codebase audit skill designed for AI Coding Agents (Codex / Claude Code / Copilot / Gemini).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Audit Modes](https://img.shields.io/badge/Audit%20Modes-26%2B-indigo.svg)](#all-audit-modes-26-focused-areas)
[![Supported Agents](https://img.shields.io/badge/Agents-Codex%20%7C%20Claude%20%7C%20Copilot%20%7C%20Gemini-black.svg)](#quick-start)
[![Live Demo](https://img.shields.io/badge/Demo-Online%20Report-success.svg)](https://xinian-dada.github.io/Fuck_My_Shit_Mountain/)

<p align="center">
  <a href="README.md">中文</a> · <strong>English</strong>
</p>

</div>

---

## Why This Skill?

When you ask a generic AI to *"review my code"*, you usually get one of two things: superficial formatting nitpicks, or a polite "looks great to me!"

**Fuck My Shit Mountain** is an uncompromising engineering audit framework. The name is self-deprecating, but the report is deadly serious. It instructs the agent to map the repository first, trace execution paths, and produce an **evidence-backed, prioritized audit report with concrete failure scenarios, minimal fixes, and regression test proposals**.

```text
Generic AI Code Review          Fuck My Shit Mountain
──────────────────────────────────────────────────────────────────────────
Passive, agreeable "Yes-Man"  ──▶  Strictly objective against codified engineering rubrics
Vague "Consider refactoring"  ──▶  Exact File:Line, trigger inputs, & realistic failure flow
No prioritization or grading  ──▶  7 core dimension scores (0.0-10.0) + 26+ domain checklist
Fixes create cascade failures ──▶  Minimal targeted remediation diffs + regression test specs
──────────────────────────────────────────────────────────────────────────
```

> **Note**: AI review assists humans—it does not replace production metrics, real load tests, or human domain review. Its superpower is doing the exhausting, systematic digging so you know exactly where the tectonic plates are slipping.

---

## Key Capabilities

- 🗺️ **Automated Architecture Mapping**: Inspects tech stacks, dependency manifests, and risk surfaces (AI/LLM, databases, APIs, auth) to automatically recommend relevant audit modes.
- 🔍 **Evidence-Based Findings**: Every issue requires concrete code citations, execution flow traces, impact analysis, and estimated remediation effort.
- 🚦 **Confirmed vs. Suspected Separation**: Separates confirmed bugs from architectural risks; unexplored domains are marked `Not assessed` rather than assumed clean.
- ⚡ **Incremental PR Audits**: Audit only `git diff` changes against `main` or release tags for continuous integration and PR reviews.
- 📊 **Rich Multi-Format Delivery**: Generate interactive standalone **HTML reports**, machine-readable **JSON schemas** for CI tooling, or clean **Markdown docs**.

---

## Quick Start

### 1. One-Prompt Install via AI IDE

Send this repository link to your AI IDE agent and instruct it to install the skill:

```text
Please install the fuck-my-shit-mountain/ skill from this repository into my environment:
https://github.com/XiNian-dada/Fuck_My_Shit_Mountain
```

### 2. Manual Installation

Copy the [`fuck-my-shit-mountain/`](fuck-my-shit-mountain/) directory into your agent's skill directory:

| Agent | Target Directory | How to activate |
| :--- | :--- | :--- |
| **Codex** | `~/.codex/skills/fuck-my-shit-mountain/` | Reload or open a new session |
| **Claude Code** | `~/.claude/skills/fuck-my-shit-mountain/` or `.claude/skills/...` | Type `/fuck-my-shit-mountain` or invoke via natural language |
| **GitHub Copilot** | `~/.copilot/skills/fuck-my-shit-mountain/` or `.github/skills/...` | Run `/skills reload` in Copilot Chat |
| **Gemini CLI** | `~/.gemini/skills/fuck-my-shit-mountain/` or `.gemini/skills/...` | Run `/skills reload` (trust workspace if needed) |

**Terminal Quick Command:**

```bash
git clone https://github.com/XiNian-dada/Fuck_My_Shit_Mountain.git /tmp/shit-mountain
mkdir -p ~/.codex/skills
cp -R /tmp/shit-mountain/fuck-my-shit-mountain ~/.codex/skills/
rm -rf /tmp/shit-mountain
```

---

## Audit Modes & Scenarios

You don't need to memorize internal mode identifiers. Just describe your intent in plain language:

| Your Scenario | Prompt Example | Internal Modes |
| :--- | :--- | :--- |
| **Comprehensive Health Check** | `Perform a full codebase audit` | `full` (all 26+ dimensions) |
| **Pre-Release Readiness** | `Focus on release readiness and operations` | `release`, `stability`, `observability`, `configuration` |
| **Security & Privacy Scrutiny** | `Audit auth, secrets, and dependencies` | `security`, `privacy`, `supply-chain` |
| **Concurrency & Deadlocks** | `Check race conditions, deadlocks, and shared state` | `concurrency`, `stability` |
| **PR / Diff Review** | `Audit changes made since the main branch` | `incremental` (git diff scope) |
| **AI / LLM Application Risks** | `Inspect prompt injection, tool permissions, and API costs` | `ai-safety`, `privacy`, `cost`, `observability` |
| **Suspiciously Green Tests** | `Verify whether tests provide genuine confidence` | `testing`, `testing-authenticity` |
| **Refactoring Preparation** | `Identify complexity, bad smells, and technical debt` | `maintainability`, `architecture`, `design`, `code-consistency` |

Reports default to the conversation language and conversational output. File output and history are opt-in. PR reviews compare `main...HEAD`; explicit snapshot comparisons use ranges such as `v1.2.0..HEAD`.

**Example Invocation:**

```text
Use fuck-my-shit-mountain to audit this project in full mode.
Report language: English
Output format: html
```

---

## Report Preview

### Score Dashboard Example

```text
Security        ████████░░  8.0  A   Owner checks verified; one contained session-expiry gap
Stability       ██████░░░░  6.0  B   2 unhandled panic paths in payment flow; missing circuit breaker
Performance     ██████████ 10.0  S   No observable I/O bottlenecks or unbounded memory growth
Testing         ████░░░░░░  4.0  C   Heavy reliance on shallow mocks; critical edge cases unasserted
Maintainability ███████░░░  7.0  A   Shared parsing logic creates recurring change cost
Design          █████░░░░░  5.0  B   Circular dependency between billing and user modules
Release         ██████░░░░  6.0  B   No automated rollback strategy; CI lacks cross-platform checks
────────────────────────────────────────────────────────────────────────────────────────────────────
Overall         ██████░░░░  6.6  B   Solid foundation, but critical stability and test gaps remain
```

### Live Interactive Demo Report

👉 **[View the Live Demo Audit Report](https://xinian-dada.github.io/Fuck_My_Shit_Mountain/)**  
*(Features responsive layout, dark/light theme, sticky sidebar navigation, severity filter, and remediation plan)*

---

## All Audit Modes (26+ Focused Areas)

`full` mode runs through all dimensions automatically. You can also specify any combination (e.g. `security, concurrency, stability`):

<details>
<summary><strong>Click to expand the complete list of 26+ audit dimensions</strong></summary>

| Mode ID | Audit Scope & Verification Areas |
| :--- | :--- |
| `architecture` | Cohesion, coupling, dependency directions, module boundaries, state ownership |
| `security` | Authentication, authorization bypass, injection, hardcoded secrets, vulnerability paths |
| `stability` | Panic/crash handling, resource exhaustion, retry/backoff, graceful shutdown |
| `concurrency` | Race conditions, deadlocks, atomicity violations, lock contention, shared mutable state |
| `performance` | Hot execution paths, memory allocations, I/O amplification, cache safety, build times |
| `testing` | Critical path coverage gaps, test tier distribution, brittle assertions |
| `testing-authenticity` | Over-mocking, implementation-detail assertions, fake green checkmarks |
| `maintainability` | Cyclomatic complexity, coupling density, code duplication, readability |
| `design` | SOLID principle violations, leaky abstractions, YAGNI over-engineering |
| `release` | CI/CD automation, semantic versioning, migration rollback safety |
| `configuration` | Schema validation, hazardous default values, multi-environment isolation |
| `observability` | Structured logging, distributed tracing, metrics, health probes, runbooks |
| `data-integrity` | Transaction boundaries, idempotency, schema migrations, partial write risks |
| `privacy` | PII collection boundaries, log sanitization, data retention & deletion |
| `accessibility` | Keyboard focus order, ARIA semantics, responsive breakpoints, UX state completeness |
| `supply-chain` | Lockfile hygiene, registry provenance, CI action pinning, SBOM auditing |
| `cost` | Unbounded queues/storage, third-party API spend, LLM token budget controls |
| `ai-safety` | Prompt injection defense, tool execution permissions, RAG leakage, fallback evals |
| `fallback` | Silent error suppression, empty catch blocks, defensive type guessing |
| `type-safety` | Unsound type assertions, excessive `unsafe` usage, boundary type coercion |
| `frontend-state` | Component sprawl, state duplication, uncontrolled side effects, UI/business coupling |
| `backend-api` | Endpoint contract consistency, request validation, N+1 query patterns |
| `dependency-weight` | Bloated dependencies, duplicate libraries, standard library alternatives |
| `code-consistency` | Directory structure, import patterns, naming conventions, style uniformity |
| `comment-coverage` | Public API documentation clarity, obsolete or misleading comments |
| `documentation` | README accuracy, onboarding setup guides, Architectural Decision Records (ADRs) |

</details>

---

## FAQ

<details>
<summary><strong>Q: Does this modify my code or commit to my repo?</strong></summary>
<strong>Never.</strong> The audit workflow strictly follows a read-only contract. It inspects files and writes report artifacts (HTML/JSON/MD), but never mutates source code, configuration, or lockfiles without explicit user command.
</details>

<details>
<summary><strong>Q: How does it handle large repositories without blowing the context window?</strong></summary>
The skill runs <code>project_inventory.py</code> first to build a structural inventory. It then systematically prioritizes high-risk attack surfaces (auth, payment, storage, concurrency) and supports <code>incremental</code> mode to target specific diffs.
</details>

<details>
<summary><strong>Q: Why are scores stricter than typical AI reviews?</strong></summary>
The scoring rubric enforces realistic engineering standards. A clean codebase with a single critical concurrency deadlock or missing auth check will see that reflected clearly in its score and Top Risks section.
</details>

---

## Community Listings & Star History

- Listed in [Tool.lu Library](https://tool.lu/library/4y1) and [SourcePulse #32479882](https://www.sourcepulse.org/projects/32479882).
- Community discussions and AI topics on [LinuxDo](https://linux.do/).

<p align="center">
  <a href="https://star-history.com/#XiNian-dada/Fuck_My_Shit_Mountain&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=XiNian-dada/Fuck_My_Shit_Mountain&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=XiNian-dada/Fuck_My_Shit_Mountain&type=Date" />
      <img alt="Star History Chart" src="https://star-history.dera.page/svg?repos=XiNian-dada/Fuck_My_Shit_Mountain&type=Date" />
    </picture>
  </a>
</p>

## License

Released under the [MIT License](LICENSE).
