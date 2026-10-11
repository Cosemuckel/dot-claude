---
name: cost-control
description: Use when evaluating or reducing Claude Code token, context, tool, MCP, or subagent usage for a workflow.
disable-model-invocation: true
user-invocable: true
---

# Cost control

Diagnose waste before changing behavior.

Check:
1. main-context size;
2. irrelevant handoff content;
3. repeated reads/searches;
4. model and effort selection;
5. agent turn counts;
6. unnecessary fan-out;
7. MCP tool/output volume;
8. broad command output;
9. unnecessary skill loading;
10. repeated or speculative verification.

Prefer:
- a narrower query;
- a smaller worker;
- lower effort;
- a tighter max-turn budget;
- a smaller handoff;
- a path-scoped rule;
- a deterministic filter;
- a CLI/native tool instead of an MCP when equivalent.

Do not optimize by making the agent omit information that is genuinely required for correctness.
