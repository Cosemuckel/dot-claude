# Upgrade notes — 1.4.1

This release hardens the orchestration control plane without changing the lead-first architecture.

## Runtime enforcement

- The default project session agent is `orchestrator`.
- `.claude/hooks/agent_guard.py` is a deterministic `PreToolUse` command hook for `Agent` calls.
- The guard uses Claude Code's `agent_type` and `prompt_id` hook fields to enforce the declared parent→child graph,
  require a named subagent, keep the task class stable within one user prompt, and enforce the total descendant-agent
  budget atomically across sequential and parallel calls.
- `SessionEnd` cleans the temporary guard state.
- The Haiku Agent/Bash/Stop/SubagentStop hooks remain semantic watchdogs rather than pretending to be the hard gate.

## Testing and MCP hardening

- Test agents remain unable to call Edit/Write. Their documentation now distinguishes "no implementation-source/test
  edits" from absolute shell immutability because Bash can still create generated/build artifacts.
- Playwright MCP is invoked with `--headless --isolated --idle-timeout=300000` for deterministic CI-oriented browser
  sessions with non-persistent browser state.
- Context7 routing documentation is consistent with the actual audit-lead configuration.

## Evaluation and installation

- The validators now treat the kit as an additive `.claude` layer: project-specific agents, skills, rules, playbooks,
  and existing `.mcp.json` are allowed rather than being rejected merely for existing. Those host additions are not
  automatically added to the kit's hardened Agent graph; graph changes require a deliberate guard/evaluator update.
- Required kit files are still checked, but the evaluator no longer claims an exact closed-world inventory.
- Installation documentation warns against blindly overwriting an existing `.claude` tree and recommends backup/merge.

## Model policy

- In 1.4.1 the model aliases were runtime-mapped; version 1.4.2 supersedes that policy by pinning exactly `claude-sonnet-5-5` and `claude-haiku-5-5`.
