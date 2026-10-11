# Upgrade notes — 1.4.2

## Model policy

- Pinned the project main session and Sonnet-tier agents to `claude-sonnet-5-5`.
- Pinned Haiku-tier agents and all semantic watchdog hooks to `claude-haiku-5-5`.
- Removed alias-based model selection and all fallback/escalation paths to other model tiers. If a pinned ID is not
  available, the setup must report a blocker rather than silently substitute another model.

## Main-session boundary

- Made the orchestrator a strict control plane: its only tool family is allow-listed `Agent(...)` dispatch.
- Prohibited direct file reads/searches, shell commands, web/MCP access, edits, and testing in the main session.
- Reworked the structural and runtime contract checks to reject unapproved model IDs and verify the agent-only boundary.
- Made rules `140-testing.md` and `230-generated-code.md` path-scoped; deduplicated rule `26-investigation-and-audit.md` against the audit-protocol skill and the handoff-protocol skill against rules 20 and 25.

## Stop hook and Windows launcher

- Root cause of the Stop loop: the Haiku prompt hook ran at every turn end, including turns that ended only to wait for
  background subagents, and kept returning a block, so the session never settled while those subagents ran.
- Replaced the Stop prompt hook with the deterministic command hook `hooks/stop_guard.py`. It reads only the hook
  payload (`last_assistant_message`, `stop_hook_active`), never the transcript. It allows waiting messages and
  `stop_hook_active`, blocks only a completion claim combined with an unresolved `FAIL`/`INCONCLUSIVE`, and fails open
  (always exit 0). Semantic prompt hooks are now three: Agent, Bash, SubagentStop.
- Hook commands now use the Windows launcher in exec form: `"command": "py"`, `"args": ["-3", ".../hook.py"]`, replacing
  `python3`, which can resolve to the Microsoft Store stub. On macOS/Linux change these entries to `python3` or
  `python`. See `INSTALL.md`.
