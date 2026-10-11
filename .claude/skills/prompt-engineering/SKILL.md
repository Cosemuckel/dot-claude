---
name: prompt-engineering
description: Use when the user explicitly asks to create, improve, diagnose, or adapt a prompt for an AI model or agent.
disable-model-invocation: true
user-invocable: true
---

# Prompt engineering

Optimize the model's decision environment, not the amount of instruction text.

Extract only what materially affects the outcome:
- objective;
- target model/system;
- context and references;
- scope;
- constraints;
- inputs;
- output contract;
- success criteria;
- examples when they disambiguate behavior.

For current Claude models with adaptive reasoning:
- Prefer clear intent and general guidance over brittle step-by-step micromanagement when the model can safely infer
  the missing execution details.
- Use explicit action language when you want tool use or implementation, and explicit conservation language when
  you want a report-only result.
- Use examples when format, taste, or edge-case behavior matters more than another paragraph of rules.
- Use XML tags when a prompt mixes instructions, context, examples, and variable inputs and the boundaries would
  otherwise be ambiguous.
- For long-running coding agents, state the done condition and require verification; do not restate every tool
  operation the model already knows how to perform.
- For long contexts, put the reference material before the query and place the actual question/decision at the end.
- Avoid duplicate instructions across CLAUDE.md, rules, skills, and agent prompts. Redundancy consumes context and
  can create instruction conflicts.

For agentic prompts, prefer:
- starting state;
- target state;
- allowed actions;
- meaningful constraints;
- done criteria;
- stop conditions;
- compact output contract.

The smallest reliable prompt is better than the longest comprehensive prompt.
