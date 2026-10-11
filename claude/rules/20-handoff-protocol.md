# Handoff protocol

Every delegation states:
1. exact task;
2. required output;
3. relevant constraints;
4. what not to return.

Also pass the smallest useful evidence packet: exact paths/symbols/tests/sources, established facts, blockers,
and unresolved decisions.

Required handoff contents by stage:

Research → planning: relevant facts, evidence locations/sources, material constraints, unresolved uncertainty.

Planning → implementation: one chosen approach, affected files/modules, ordered steps,
invariants/compatibility constraints, verification criteria, material risks.

Implementation → testing: files changed, behavioral/structural change, verification already performed,
blockers/deviations.

Testing → orchestrator: PASS, FAIL, or INCONCLUSIVE; checks actually run; exact evidence needed to justify the
status; blockers/uncertainty.

Do not forward raw transcripts, large tool outputs, or duplicated instructions. Prefer references the recipient
can inspect directly.
