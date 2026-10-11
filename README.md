# dot-claude

Claude Code behaviour set (CLAUDE.md, rules, agents, skills, playbooks, evals, hooks, docs, watchdog notes, settings), version 1.4.2 per `.claude/VERSION`.

- `.claude/` is the frozen baseline. It matches the live set loaded by Claude sessions. Do not edit it.
- `claude/` is the working copy where improvements are made. It started as a byte-exact copy of `.claude/`.

The two folders are not synced automatically; changes from `claude/` must be carried over to the live set manually.

Not included: user-level state (`~/.claude` memory, projects, sessions, history, caches, credentials) and local overrides (`settings.local.json`).
