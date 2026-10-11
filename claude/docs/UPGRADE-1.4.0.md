# Upgrade notes — 1.4.0

This release retunes the kit for the current Claude 5.5 generation and recent Claude Code context-engineering
practice.

## What changed

### Model policy
- `haiku` remains the alias, but is now documented as following the current Haiku line; as of 1.4.0 this is
  Claude Haiku 5.5.
- Nontrivial Haiku sidecars use `medium` effort. `micro-reader` stays at `low` for genuinely narrow lookups.
- `sonnet` remains the workhorse alias; as of 1.4.0 this is Claude Sonnet 5.5.
- Model routing was subsequently tightened in 1.4.2: only the pinned Sonnet 5.5 and Haiku 5.5 model IDs are permitted.

### Orchestration
- Stage leads now have the tools required to perform their own stage work directly.
- Leaf workers are optional sidecars for context isolation, independent parallel work, or a fresh perspective.
- Playbooks are checkpoint sets rather than mandatory step-by-step agent pipelines.
- Independent Agent calls may run in parallel when there is no shared-write or ordering dependency.

### Context engineering
- Prompts favor intent, references, done criteria, and judgment over repetitive prohibitions.
- Handoffs prefer exact paths/symbols/tests/sources over copied context.
- Added the manual `context-engineering` skill.
- Added guidance for `/rewind`, `/compact`, `/clear`, and deliberate subagent use.
- Added `docs/MODEL-AND-CONTEXT.md`.

### Verification and hardening
- Testing and audit remain separate authority boundaries.
- Audit remains capability-level read-only.
- Watchdog policy was tightened around malformed/disproportionate Agent calls but relaxed around valid technical
  strategies.
- Static and deterministic runtime evaluators now verify the lead-first capability sets.

## Release verification

The package validators pass:

- `python .claude/evals/structural_check.py`
- `python .claude/evals/runtime_contracts.py`

The runtime suite is deterministic/offline. Live Claude Code trace testing remains environment-dependent.
