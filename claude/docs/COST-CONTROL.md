# Cost control

Cost control is primarily context control. Research is opt-in, not a ritual.

| Class | Agent budget |
|---|---:|
| TRIVIAL | 4 |
| SMALL | 6 |
| MODERATE | 12 |
| COMPLEX | 24 |

The budget counts descendant-agent calls for one user prompt. The deterministic runtime guard persists the count across
stages and retries and resets only when a new user prompt starts a new task.

## Model allocation

`claude-haiku-5-5` is the default sidecar model. Use low effort for genuinely narrow lookups and medium effort for
longer research/planning/audit/verification work. Exact model economics are provider/runtime properties.

Current package policy:
- micro-reader: `claude-haiku-5-5` / low;
- research-worker: `claude-haiku-5-5` / medium;
- plan-worker: `claude-haiku-5-5` / medium;
- test-runner: `claude-haiku-5-5` / medium;
- audit-worker: `claude-haiku-5-5` / medium;
- orchestrator and stage leads: `claude-sonnet-5-5` / medium by default;
- implementation lead and implementation worker: `claude-sonnet-5-5` / high.

## Spend context where it pays

Subagents are worth the overhead when they keep large intermediate outputs out of the parent context, enable
independent parallel work, or provide a fresh verification perspective.

Do not create subagents for short sequential work that the current lead can complete directly.

Use `/rewind` to recover from a bad branch of reasoning without carrying its downstream tool noise.
Use `/compact` for a long but still-relevant task.
Use `/clear` for unrelated work.

Keep MCP output scoped and avoid broad Bash dumps.

## Effort calibration

The pinned model IDs support explicit `effort` values. Keep effort explicit in agent definitions so the intended
workload tier remains reviewable. Do not substitute a different model ID when behavior or availability changes.

Re-check these choices against live repository evaluations when changing the task mix.
