# Watchdog

The watchdog is a conservative control plane implemented with Claude Code hooks. It has a deterministic command layer
for hard orchestration constraints and a Haiku prompt layer for semantic review.

It observes `PreToolUse` on `Agent` and `Bash`, `SubagentStop`, `Stop`, and `SessionEnd` for guard-state cleanup.

The command layer enforces capability graph, named-child, task-class, and descendant-budget constraints. `Stop` is
also deterministic (`hooks/stop_guard.py`): it allows stopping when the final message shows work waiting on
background agents, blocks only a completion claim paired with an unresolved `FAIL`/`INCONCLUSIVE` status, is one-shot
via `stop_hook_active`, and fails open on any error. The prompt layer covers `PreToolUse` on `Agent` and `Bash`
(proportionality, obvious context-dump waste) and `SubagentStop` (stage-role discipline, verification/completion claims).

The watchdog does not choose technical solutions and does not require a particular valid implementation strategy.

## Agent policy

The allowed graph is:

`orchestrator → {research-lead, planning-lead, implementation-lead, testing-lead, audit-lead, micro-reader}`

Each stage lead may use its own stage tools directly and may optionally spawn:
- research-lead → research-worker, micro-reader
- planning-lead → plan-worker, micro-reader
- implementation-lead → implementation-worker, micro-reader
- testing-lead → test-runner, micro-reader
- audit-lead → audit-worker, micro-reader

Leaf workers cannot delegate.

## Proportionality

TRIVIAL and SMALL work should not trigger unnecessary research/planning or worker fan-out. MODERATE and COMPLEX work
may use multiple contexts when they add isolation, independent parallelism, or fresh verification.

Every Agent call carries the ORCHESTRATION CONTROL block. The deterministic guard atomically counts accepted Agent
calls under Claude Code's `prompt_id`, so the hard total survives sequential retries and parallel fan-out.
`budget_before`/`budget_after` remain compact handoff metadata; they are not a shared mutable counter.

The watchdog should intervene only on clear violations. Do not block legitimate technical choices because the
watchdog would have designed a different solution.
