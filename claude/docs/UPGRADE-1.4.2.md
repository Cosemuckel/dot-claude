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
