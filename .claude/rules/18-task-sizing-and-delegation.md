# Task sizing and delegation budgets

Every user request gets one intent and one complexity class before the first agent is spawned. Intent selects
the workflow; complexity controls the descendant-agent budget.

| Class | Typical work | Total descendant-agent budget | Research | Planning | Fan-out |
|---|---|---:|---|---|---|
| TRIVIAL | narrow fact, tiny edit, toy/example, deterministic local change | 4 | forbidden | forbidden | one path only |
| SMALL | bounded local/multi-file change, straightforward small feature with known stack | 6 | forbidden by default; one narrow `micro-reader` only for a named blocking repository fact | forbidden for implementation work | one path at a time |
| MODERATE | cross-cutting change, meaningful ambiguity/integration, non-trivial feature | 12 | allowed when material to the result | allowed when it changes the implementation direction | independent work only |
| COMPLEX | large, risky, multi-system, or materially uncertain work | 24 | allowed and bounded | allowed and bounded | independent work only |

The budget counts every descendant agent call for the current user task, including stage leads, specialists,
and `micro-reader`. Direct tool use inside a stage lead does not consume the descendant-agent budget.

## Mandatory orchestration control block

Every `Agent` handoff must include:

```text
ORCHESTRATION CONTROL
class: TRIVIAL | SMALL | MODERATE | COMPLEX
budget_before: <integer>
budget_after: <integer>
purpose: <one sentence>
research: forbidden | exception-only | allowed
```

`budget_after` must equal `budget_before - 1`. These two fields are a compact handoff ledger, not the shared
concurrency counter. In parallel Agent calls, multiple siblings may legitimately carry the same `budget_before`
snapshot; the deterministic runtime guard atomically counts accepted Agent calls for the current `prompt_id` and is
the source of truth for the hard limit. Never increase, reset, replenish, or omit the task class/budget. If the
guard reports exhaustion, do not spawn another agent.

## Proportionality gates

TRIVIAL tasks do not use `research-lead`, `planning-lead`, a playbook, or parallel workers. For a code change,
use one direct implementation path and focused verification only when it materially establishes the requested result.

SMALL implementation tasks do not use `research-lead` or `planning-lead` by default. A single `micro-reader` is
allowed only when a named repository fact blocks implementation. External research is not justified merely for
completeness.

MODERATE and COMPLEX tasks may use research, planning, playbooks, and specialist fan-out, but each additional
agent must add context isolation, independent work, or a fresh verification perspective.

Research is opt-in, not a ritual. The descendant-agent budget never resets between stages or retries. A research
call must name the concrete uncertainty it resolves and the downstream decision that depends on it. The runtime
guard keys the budget to Claude Code's `prompt_id`, so a genuinely new user prompt gets a fresh budget while retries
and descendant stages within the same prompt do not.

Planning is also proportional. Straightforward work with an obvious implementation path should skip a planning
stage even when it is technically possible.

Parallel Agent calls are allowed when the workstreams are independent and have no shared-write or ordering
dependency. Same-file edits stay in one context.

## Failure and stopping behavior

A failure does not grant a new budget. Use the remaining budget to correct the concrete failure and verify it.

Reaching the requested outcome ends orchestration immediately. Do not spend unused budget merely because it exists.

## Intent-specific gates

`CHANGE` uses the implementation workflow. `DIAGNOSE` and `AUDIT` are report-only and must not enter
implementation merely because a defect is discovered. `QUESTION` stays on the narrowest answer path.

For audits/diagnosis, high-impact candidate findings should receive a false-positive or independent verification
pass when budget permits.
