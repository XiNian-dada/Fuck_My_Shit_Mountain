<div align="center">

![Fuck My Shit Mountain banner](assets/banner-zh.png)

# Fuck My Shit Mountain

**专治“项目能跑，但我总觉得山里埋了雷”**  
面向 AI Coding Agent（Codex / Claude Code / Copilot / Gemini）的证据级全维度代码库审计 Skill。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Audit Modes](https://img.shields.io/badge/Audit%20Modes-26%2B-indigo.svg)](#全部模式)
[![Supported Agents](https://img.shields.io/badge/Agents-Codex%20%7C%20Claude%20%7C%20Copilot%20%7C%20Gemini-black.svg)](#快速上手)
[![Live Demo](https://img.shields.io/badge/Demo-Online%20Report-success.svg)](https://xinian-dada.github.io/Fuck_My_Shit_Mountain/)

<p align="center">
  <strong>中文</strong> · <a href="README.en.md">English</a>
</p>

</div>

---

## 为什么需要它？

当你问常规 AI *“帮我 review 一下代码”* 时，往往只能得到两类回答：要么是浮于表面的格式挑刺，要么是一团和气的“写得很好没毛病”。

**Fuck My Shit Mountain** 是一套严谨的工程审计规范。名字是解构的，但报告极其严肃。它让 AI 像一位经验丰富、直言不讳的架构与安全同行，先摸清代码库全貌，再顺着代码链路挖掘潜在雷区，产出一份**带代码证据、带复现路径、带优先级与修复验证建议**的专业审计报告。

```text
常规 AI 审查                  Fuck My Shit Mountain
──────────────────────────────────────────────────────────────────────────
随性发挥，容易当“和事佬”   ──▶  绝对客观，基于工程标尺，绝不妥协奉承（No Yes-man）
空泛的“建议加注释/重构”     ──▶  具体到 File:Line、触发条件与真实故障演进场景
缺乏量化与优先级判断       ──▶  7 大核心维度评分 + 26+ 专业维度矩阵覆盖
改完容易引发连锁崩溃       ──▶  提供最小化精准修复策略与对应的回归测试建议
──────────────────────────────────────────────────────────────────────────
```

> **注意**：AI 审计并非魔法，无法完全替代深入的人工复核与生产环境实测；它的价值在于以极高效率替你完成地毯式排雷，把隐藏在山底的架构与安全隐患提早摆在台面上。

---

## 核心特性

- 🗺️ **自动化项目画像**：自动识别技术栈、依赖清单与关键风险暴露面（AI/LLM、数据库持久化、服务端接口等），自然语言智能推荐审计维度，告别生硬死板的指令。
- 🔍 **证据闭环（Evidence-Based）**：每条发现必须具备具体的代码行号、真实触发条件、影响推导与工时预估，拒绝无凭据的主观臆断。
- 🚦 **真假风险区分**：严格隔离**已确认缺陷**与**待确认风险**，未深入覆盖的区域明确标注为 `Not assessed`，绝不把“未发现”粉饰为满分。
- ⚡ **增量审计（Incremental Mode）**：支持基于 `git diff` 针对 PR 变更文件展开定向审查，快速嵌入日常代码 Review 与持续交付流。
- 📊 **专业报告呈现**：支持一键导出交互式单页 **HTML 报告**、自动化流程适用的 **JSON 数据**，以及极简的 **Markdown 文档**。

---

## 快速上手

### 1. 告诉你的 AI IDE 一键安装

将本仓库链接发送给支持 Agent 体系的 AI IDE，并指示安装：

```text
请帮我把这个仓库中的 fuck-my-shit-mountain/ skill 安装到当前环境：
https://github.com/XiNian-dada/Fuck_My_Shit_Mountain
```

### 2. 手动安装指南

将仓库内的 [`fuck-my-shit-mountain/`](fuck-my-shit-mountain/) 目录复制到对应平台的 skills 目录即可：

| 平台 | 安装路径 | 生效方式 |
| :--- | :--- | :--- |
| **Codex** | `~/.codex/skills/fuck-my-shit-mountain/` | 复制后新开对话即可生效 |
| **Claude Code** | `~/.claude/skills/fuck-my-shit-mountain/` 或 `.claude/skills/...` | 终端输入 `/fuck-my-shit-mountain` 或自然语言唤起 |
| **GitHub Copilot** | `~/.copilot/skills/fuck-my-shit-mountain/` 或 `.github/skills/...` | 复制后在对话窗口执行 `/skills reload` |
| **Gemini CLI** | `~/.gemini/skills/fuck-my-shit-mountain/` 或 `.gemini/skills/...` | 复制后执行 `/skills reload`，工作区安装前需 trust |

**终端极简安装：**

```bash
git clone https://github.com/XiNian-dada/Fuck_My_Shit_Mountain.git /tmp/shit-mountain
mkdir -p ~/.codex/skills
cp -R /tmp/shit-mountain/fuck-my-shit-mountain ~/.codex/skills/
rm -rf /tmp/shit-mountain
```

---

## 审计模式与使用指引

你无需背诵内部参数，直接用日常工程语言表达需求：

| 你的关注点 | 建议表达方式 | 内部执行模式 |
| :--- | :--- | :--- |
| **全盘摸底体检** | `请对项目进行全量审计` | `full`（覆盖全量 26+ 维度） |
| **上线前合规把关** | `偏发布与运维审查` | `release`, `stability`, `observability`, `configuration` |
| **权限与供应链安全** | `重点看权限、密钥和依赖安全` | `security`, `privacy`, `supply-chain` |
| **高并发与死锁** | `排查竞态条件、死锁与共享状态` | `concurrency`, `stability` |
| **PR 提交定向把关** | `审计当前分支自 main 分支以来的变更` | `incremental`（基于 git diff） |
| **AI / LLM 应用专项** | `排查 Prompt 注入、Tool 鉴权与 Token 账单` | `ai-safety`, `privacy`, `cost`, `observability` |
| **怀疑测试虚假通过** | `检查测试是否真实有效` | `testing`, `testing-authenticity` |
| **代码重构准备** | `排查代码异味与可维护性` | `maintainability`, `architecture`, `design`, `code-consistency` |

默认跟随当前对话语言，并在对话内输出报告；文件输出与历史记录按需启用。PR 的分叉点比较使用 `main...HEAD`，明确的快照比较使用 `v1.2.0..HEAD`。

**示例提示词：**

```text
请使用 fuck-my-shit-mountain 对当前项目进行全量审计。
报告语言：中文
输出格式：html
```

---

## 报告长什么样？

审计完成后，你将获得包含量化评分、置信度矩阵、顶层风险和分步整改计划的完整交付件。

### 核心维度评分面板示例

```text
Security        ████████░░  8.0  A   关键权限边界已验证，一处会话过期处理需要完善
Stability       ██████░░░░  6.0  B   核心支付链路存在 2 处未捕获异常，缺少重试熔断
Performance     ██████████ 10.0  S   未发现明显 I/O 阻塞或热点开销
Testing         ████░░░░░░  4.0  C   单元测试多为无效 Mock，关键业务分支缺乏断言
Maintainability ███████░░░  7.0  A   共享解析逻辑存在重复修改与遗漏风险
Design          █████░░░░░  5.0  B   业务模块存在双向依赖，分层边界模糊
Release         ██████░░░░  6.0  B   缺少自动化回滚方案，CI 未做跨环境构建校验
────────────────────────────────────────────────────────────────────────────
Overall         ██████░░░░  6.6  B   主体框架基本成型，但上线前须解决稳定性与测试短板
```

### 在线交互式 Demo 报告

👉 **[点击预览在线 Demo 页面](https://xinian-dada.github.io/Fuck_My_Shit_Mountain/)**  
*(支持深浅色自适应、侧边栏滚动监听、风险等级过滤与详细整改卡片)*

---

## 全部审计维度（26+ 专项）

`full` 模式会自动化覆盖全部细分项；日常使用时亦可自由指定组合（如 `security, concurrency, stability`）：

<details>
<summary><strong>点击展开全部 26+ 细分维度清单</strong></summary>

| 模式 ID | 审查重点与覆盖范围 |
| :--- | :--- |
| `architecture` | 模块职责划分、依赖方向、分层边界、状态所有权 |
| `security` | 身份认证、权限绕过、注入风险、密钥凭据泄漏、安全回归 |
| `stability` | 异常传播、Panic 路径、资源泄漏、重试退避、优雅停机 |
| `concurrency` | 竞态条件（Race Condition）、死锁、原子性破坏、锁粒度与共享可变状态 |
| `performance` | 热点路径、内存开销、I/O 放大、缓存穿透、启动和构建开销 |
| `testing` | 核心用例覆盖缺口、测试分层完整度、边界条件与脆弱测试 |
| `testing-authenticity` | 过度 Mock、只测实现细节、假绿测试、缺乏端到端真实路径 |
| `maintainability` | 圈复杂度、模块耦合度、冗余逻辑、命名直观性与重构阻力 |
| `design` | SOLID 原则违规、抽象泄漏、过度工程（YAGNI）、防御性脆弱 |
| `release` | CI/CD 流程完整性、语义化发版、迁移安全与回滚机制 |
| `configuration` | 配置 Schema 校验、危险默认值、多环境隔离、废弃特性开关清理 |
| `observability` | 结构化日志、全链路追踪、监控指标、健康探针、告警与运维手册 |
| `data-integrity` | 数据库事务边界、幂等性设计、Schema 迁移回滚、部分写入风险 |
| `privacy` | PII 个人隐私数据采集、日志脱敏、数据留存/遗忘合规 |
| `accessibility` | 键盘焦点管理、ARIA 语义无障碍支持、响应式视口、UX 状态完整性 |
| `supply-chain` | 锁文件完整性、依赖项来源安全、CI Action Pinning、SBOM 资产审计 |
| `cost` | 云基础设施开销、无界队列/存储膨胀、外部商业 API 与 LLM Token 账单风险 |
| `ai-safety` | Prompt Injection 防御、Agent 工具调用权限截断、RAG 向量泄露、成本拦截 |
| `fallback` | 危险静默降级、空 Catch 吞错、掩耳盗铃式的类型猜测 |
| `type-safety` | Unsafe 代码块滥用、非法类型强制断言、边界空值处理 |
| `frontend-state` | 组件颗粒度、状态散落、副作用蔓延、UI 与业务逻辑耦合 |
| `backend-api` | RESTful/GraphQL 一致性、请求入参校验、N+1 查询、数据访问层隔离 |
| `dependency-weight` | 冗余臃肿依赖、工具链重复打包、现代标准能力替代可行性 |
| `code-consistency` | 目录规范、导入规范、命名范式与团队代码风格一致性 |
| `comment-coverage` | 导出接口文档有效性、陈旧误导性注释、代码解释失真 |
| `documentation` | README 准确性、本地环境冷启动指引、架构设计决议（ADR） |

</details>

---

## 常见问题 (FAQ)

<details>
<summary><strong>Q: 它会修改我的源码或提交 Git 记录吗？</strong></summary>
<strong>绝对不会。</strong> 审计过程遵循严格的只读契约，只在项目根目录或指定路径输出审计报告与整改建议，绝不会擅自修改任何业务逻辑、配置或锁文件。
</details>

<details>
<summary><strong>Q: 大型代码库上下文装不下怎么办？</strong></summary>
系统内置了渐进式画像机制。AI 会先借助 <code>project_inventory.py</code> 建立项目地图，优先对鉴权、网关、支付、核心数据流等高风险表面展开深度排查，并可通过 <code>incremental</code> 模式聚焦增量变更。
</details>

<details>
<summary><strong>Q: 为什么对某个维度的评分比想象中严格？</strong></summary>
本项目采用“宁严勿滥”的工程标尺。哪怕整体架构规范，如果核心调用链缺少超时熔断，或存在严重并发死锁隐患，都会如实反映在相应维度的得分与 Top Risks 列表中，拒绝无原则的粉饰。
</details>

---

## 社区收录与 Star 趋势

- 本项目已被 [Tool.lu Library](https://tool.lu/library/4y1) 与 [SourcePulse #32479882](https://www.sourcepulse.org/projects/32479882) 目录收录。
- 技术交流与探讨欢迎访问 [LinuxDo 社区](https://linux.do/)。

<p align="center">
  <a href="https://star-history.com/#XiNian-dada/Fuck_My_Shit_Mountain&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=XiNian-dada/Fuck_My_Shit_Mountain&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=XiNian-dada/Fuck_My_Shit_Mountain&type=Date" />
      <img alt="Star History Chart" src="https://star-history.dera.page/svg?repos=XiNian-dada/Fuck_My_Shit_Mountain&type=Date" />
    </picture>
  </a>
</p>

## 开源协议

本项目基于 [MIT License](LICENSE) 开源。
