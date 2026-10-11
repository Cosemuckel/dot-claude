---
name: context-engineering
description: Use when a Claude Code session, CLAUDE.md, rules, skills, handoffs, or agent graph is becoming noisy, expensive, or overconstrained.
disable-model-invocation: true
user-invocable: true
---

# Context engineering

Treat context as a working resource, not a permanent transcript.

## Diagnose the shape of the context

Identify which material is actually load-bearing:
- current user objective;
- repository facts and exact references;
- active constraints and contracts;
- unresolved decisions;
- verification evidence.

Remove stale debugging, repeated explanations, raw logs, and duplicated policy.

## Choose the right context reset

Use `/rewind` when a direction failed but earlier evidence remains useful.

Use `/compact` when the same task must continue but the session has accumulated stale or noisy context.

Use `/clear` for a genuinely new task and restart from a concise brief.

Use a subagent when the next activity will produce a lot of intermediate output that the parent only needs as a
conclusion.

## Tune the instruction stack

Keep `CLAUDE.md` lightweight. Put project-specific gotchas and durable invariants in rules. Put procedures and
reference-heavy workflows in skills. Put isolated side work in subagents. Put deterministic enforcement in hooks.

Prefer one authoritative instruction over several near-duplicates.

When a model repeatedly succeeds without a guardrail, remove the guardrail from the prompt and keep only a
capability-level or deterministic boundary that still matters.

When a model repeatedly fails because the desired behavior is under-specified, add one concrete success criterion,
example, or reference rather than a large new rule set.

## Handoffs

Pass conclusions, exact references, open questions, and verification evidence. Do not pass raw transcripts.
