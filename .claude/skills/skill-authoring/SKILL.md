---
name: skill-authoring
description: >-
  Author or revise a Claude Code skill and evaluate its trigger precision, context footprint, and
  behavioral effect.
disable-model-invocation: true
---

# Skill authoring

Treat a skill as an engineered artifact.

1. Define one clear task and one clear trigger condition.
2. Keep the description concise and put the key use case first.
3. Put the actual procedure in `SKILL.md`, not in the description.
4. Use references/examples/scripts for material that does not belong in the always-listed skill body.
5. Avoid generic advice already known to Claude.
6. Create positive and negative trigger cases.
7. Test the skill behavior with realistic tasks.
8. Revise based on observed failure modes.

A good skill changes behavior reliably without requiring a giant prompt.
