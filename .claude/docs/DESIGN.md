# Design

## Model-native orchestration

This package keeps strong capability and authority boundaries while removing unnecessary process wrappers.

The main session is a routing channel. Stage leads can do their own bounded work directly. Leaf workers are optional
sidecars used for context isolation, independent parallel work, or a fresh perspective.

This aligns the package with current Claude Code guidance: subagents add value when the parent would otherwise absorb
large intermediate output, when tasks are independent, or when a clean second opinion is useful. Sequential work
that depends on the full previous context is usually better kept in one agent context.

## 1. Small persistent context

[`.claude/CLAUDE.md`](../CLAUDE.md) is the always-loaded universal contract and index. Topic-specific guidance lives
in [`.claude/rules/`](../rules/), procedures in [`.claude/skills/`](../skills/), and recurring workflows in
[`.claude/playbooks/`](../playbooks/).

Keep persistent instructions lean. Avoid duplicating model capabilities or generic coding knowledge that Claude can
infer from its tools and repository.

## 2. Main orchestration boundary

The project settings select `orchestrator` as the default main-thread agent and pin its model to
`claude-sonnet-5-5`. The orchestrator has exactly one tool family: approved `Agent(...)` dispatch. It cannot access
repository or project contents directly and cannot use shell, web, MCP, editing, or test tools. A deterministic
`PreToolUse` command hook enforces the parent→child graph because nested `Agent(...)` declarations are not themselves
an authoritative parent-specific allowlist.

The orchestrator selects stages according to task intent and complexity. It should not build a pipeline merely
because one exists.

## 3. Stage leads and leaf sidecars

Each stage lead owns the core work for its stage.

Research: direct read/search/web work; research-worker or micro-reader only when isolation/parallelism helps.

Planning: direct repository analysis and one chosen direction; plan-worker or micro-reader for focused independent
questions.

Implementation: direct editing and command execution; implementation-worker for isolated non-overlapping units.

Testing: direct verification; test-runner for isolated checks, parallel verification, or noisy output.

Audit/diagnosis: direct evidence gathering and validation; audit-worker for isolated checks or independent
counter-checks. The audit target remains read-only.

## 4. Narrow file analysis

`micro-reader` exists for one-fact lookups and tightly scoped file/code analysis. It is read-only, has no shell/web
access, and returns only the requested result.

## 5. Skills and progressive disclosure

Skills contain reusable procedures and reference-heavy guidance. Internal protocol skills are not user-invocable.
The `context-engineering` skill is a manual tool for diagnosing noisy, expensive, or overconstrained sessions.

Prefer one authoritative instruction over duplicated guidance across CLAUDE.md, rules, skills, and agent prompts.

## 6. MCP isolation

Context7 and Playwright remain inline-scoped to agents that need them. The orchestrator has no MCP access.

Serena is optional and documented only.

## 7. Model routing

The package permits exactly two pinned IDs: `claude-sonnet-5-5` and `claude-haiku-5-5`. The main orchestrator, stage
leads, and implementation worker use Sonnet 5.5. Narrow workers and semantic watchdog hooks use Haiku 5.5. No
alias-based fallback or escalation to any other model is permitted. If a pinned ID is unavailable, report a blocker.

Effort remains workload-aware: `micro-reader` uses low effort; research, planning, audit, and verification sidecars
use medium effort; implementation uses high effort; the orchestrator and other leads use medium effort by default.

## 8. Verification

Testing is a separate role and separate context. It verifies actual artifact state and actual check results.
It may parallelize independent checks but never edits the implementation.

## 9. Watchdog

The package watchdog has two layers. A deterministic `PreToolUse` command hook enforces the parent→child graph, named
subagent requirement, task-class consistency, and the per-user-prompt descendant budget. Prompt hooks provide the
semantic proportionality and completion review. The completion hooks are not independent execution of tests.

## 10. Cost and context control

The dominant optimization is reducing unnecessary context movement, not merely shrinking prompts.

Use:
- bounded handoffs;
- direct stage-lead execution;
- isolated sidecars for noisy subtasks;
- parallel independent work;
- `/rewind`, `/compact`, `/clear` deliberately;
- focused command output;
- model/effort matching to task difficulty.

## 11. Audit / diagnosis

Audit and diagnosis are report-only. They require scoped evidence, false-positive checking, severity/confidence
separation, and explicit coverage gaps.

A clean report means no findings established in the reviewed scope; it does not mean the system is proven safe.
