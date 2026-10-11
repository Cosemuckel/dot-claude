# Installation

Package version: `1.4.2`

Install the package into the repository root so the project-scoped `.claude/` directory is present. Do not blindly
overwrite an existing `.claude/` tree: back it up first and merge package-owned files with project-owned settings,
agents, rules, skills, and hooks. The package does not require a project `.mcp.json`; its bundled MCP definitions are
inline in the owning agent files.

The project settings select `orchestrator` as the default agent. Start normally:

```bash
claude
```

The explicit equivalent is:

```bash
claude --agent orchestrator
```

The first run may prompt for project trust or MCP authorization. Review those prompts before proceeding.

Install the validator dependency before running the static check:

```bash
python -m pip install -r .claude/evals/requirements.txt
```

Check configuration with separate commands:

```text
/agents
/mcp
```

`/agents` should show the project agents. `/mcp` should show the MCP connections when their owning agents are
active/connected.

For Playwright MCP, Node.js 20+ is required. The package uses the `@playwright/mcp@1` major line with headless and
isolated browser profiles. Treat the dependency as an explicit release input and upgrade it deliberately after
compatibility verification.

## Model allocation

- The only allowed model IDs are `claude-sonnet-5-5` and `claude-haiku-5-5`.
- The project main session is pinned to `claude-sonnet-5-5`; every agent and semantic watchdog uses one of those two IDs.
- The main orchestrator exposes only approved `Agent(...)` dispatch. It has no file, search, shell, web, MCP, edit,
  write, or test tools. All repository work is performed by agents.
- If a pinned model ID is unavailable, report the blocker; do not fall back to an alias or another model.
- Use the prescribed launch command so the main model remains explicit: `claude --model claude-sonnet-5-5 --agent orchestrator`.

## Serena

See [`docs/MCP.md`](MCP.md). It is optional and not enabled by this package.

## Safety note

The package intentionally does not grant broad permissions or bypass permission checks. Your repository and
organization settings remain authoritative.

## Watchdog

The package enables a project-scoped orchestration watchdog through `.claude/settings.json`.

No extra process is required. The watchdog is silent when behavior is valid and intervenes only on clear
process violations. The watchdog has a deterministic command hook for hard Agent graph/budget enforcement plus Haiku prompt hooks for semantic proportionality and completion review.

The semantic layer is model-based and intentionally conservative. The graph/budget gate is deterministic and should
be treated as the hard runtime boundary.

The package also supports report-only `AUDIT` and `DIAGNOSE` intents via `audit-lead`; these do not modify the
target or automatically enter implementation.

## Control-plane verification

Run both package checks after changing orchestration, permissions, hooks, or evaluation files:

```bash
python .claude/evals/structural_check.py
python .claude/evals/runtime_contracts.py
```

The first check validates static package structure.

The second runs deterministic control-plane contract scenarios for permissions, routing, watchdog
configuration, budget arithmetic, MCP scope, documentation consistency, and release hygiene.

The deterministic Agent guard can be regression-tested offline, but these checks do not replace live Claude Code trace
testing in the target environment.

The validator is additive: extra project agents/skills/rules/playbooks and an existing `.mcp.json` are not errors. They
are not automatically added to the hardened orchestration graph, however. To make a new agent routable from the kit's
main session, update the deterministic graph in `.claude/hooks/agent_guard.py` and its regression checks deliberately.
