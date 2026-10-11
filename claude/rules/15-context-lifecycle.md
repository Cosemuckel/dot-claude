# Context lifecycle

Context is a finite working resource.

## Keep sessions task-focused

Start a new context for a genuinely new task.

Within Claude Code:
- use `/rewind` to discard a failed direction while retaining useful evidence;
- use `/compact` when the same task must continue but stale material is accumulating;
- use `/clear` between unrelated tasks and restart from a concise brief;
- use a subagent when the next activity will generate substantial intermediate output that the parent only needs as
  a conclusion.

## Keep outputs bounded

Prefer focused commands and queries over broad dumps.

Do not print entire files, repositories, logs, traces, diffs, or documentation when a targeted query can establish
the answer.

## Context handoff

Pass conclusions, exact references, evidence, blockers, and unresolved decisions—not raw transcripts.
