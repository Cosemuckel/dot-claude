# Model and context policy

## Allowed models

This package is pinned to exactly two model IDs: `claude-sonnet-5-5` and `claude-haiku-5-5`. No other model or
tier is permitted. Do not use an alias that may silently move to a different release, and do not escalate to another
model for difficult tasks. If either pinned ID is unavailable in the installed Claude Code runtime, stop and report
the configuration blocker rather than substituting a different model.

`claude-sonnet-5-5` is used for the main orchestrator, stage leads, and implementation worker.
`claude-haiku-5-5` is used for bounded workers and the semantic watchdog hooks.

## Main-session boundary

The main chat is only a coordination channel. Its sole tool family is the allow-listed `Agent(...)` tool. It launches
approved agents, receives their results, may dispatch bounded rework, and synthesizes the final response. It must not
read/search files, run commands or tests, edit files, use web/MCP tools, or perform repository work itself. All such
activities belong in authorized agents. The declared tool allowlist and structural evaluation enforce this boundary.

## Context engineering

Keep the always-loaded contract lightweight. Put procedural details in skills, domain rules in scoped rules, and
stage-specific actions in stage agents. The main session should receive compact handoffs: conclusions, evidence,
verification status, assumptions, and blockers rather than transcripts, raw file contents, or large logs.

Retain only the information needed for routing decisions and final synthesis. Use agents when file access, research,
implementation, or verification is required; do not compensate for missing evidence with unsupported claims.
