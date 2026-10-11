---
name: handoff-protocol
description: >-
  Use when an agent must delegate work or return a result to another stage; produce the smallest
  useful handoff packet.
user-invocable: false
---

# Handoff protocol

Include the task intent (`CHANGE`, `DIAGNOSE`, `AUDIT`, or `QUESTION`) when it affects allowed work.

Before returning, remove everything the caller did not ask for. Keep only facts, decisions, evidence,
constraints, blockers, or verification needed by the next stage.

Never paste raw logs, file dumps, search transcripts, rejected hypotheses, or broad recommendations.

Use `.claude/rules/20-handoff-protocol.md` for stage formats and `.claude/rules/25-task-contract.md` for task-contract fields.

## Prior failures and blockers

Preserve important negative information:

- approaches already tried;
- why they failed;
- tests that still fail;
- unresolved blockers;
- evidence that rules out a path.

The purpose is to prevent downstream agents from repeating work.

A handoff is a state packet, not a transcript.
