# Feature development playbook

Use for MODERATE or COMPLEX feature work. The playbook is a set of useful checkpoints, not a mandatory
agent sequence. Omit any checkpoint that adds no value.

1. Establish existing behavior, architecture, constraints, and relevant project patterns; use research when the
   needed context is genuinely uncertain or large.
2. Decide the implementation direction; use planning when the change has meaningful design ambiguity or cross-cutting
   dependencies.
3. Implement the approved direction. Implementation-lead may execute directly or delegate isolated non-overlapping
   units.
4. Independently verify the requested behavior.
5. Repeat implementation → verification only for concrete verification failures.
6. Stop once the requested behavior is implemented and verification is sufficient.

Skills and MCP are loaded only where relevant. Handoffs contain compact conclusions and references, not transcripts.
