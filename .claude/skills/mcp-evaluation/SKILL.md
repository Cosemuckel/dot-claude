---
name: mcp-evaluation
description: >-
  Evaluate whether a proposed MCP server is justified, which agents should receive it, and whether a
  skill, subagent, native tool, or hook would be a better fit.
disable-model-invocation: true
---

# MCP evaluation

For a proposed integration, determine:
1. What capability is actually missing?
2. Can native Claude Code tools solve it?
3. Would a skill solve it procedurally?
4. Would a subagent solve the context-isolation problem?
5. Would a hook enforce it more reliably?
6. Is an existing MCP better than writing one?
7. Which specific agents actually need access?

Prefer the smallest capability surface. Scope MCP access to agents that need it. Avoid adding an MCP merely
because it is popular.
