# Investigation and audit mode

`AUDIT` and `DIAGNOSE` are first-class report-only task intents. They are not incomplete implementation tasks.

## Audit

An audit answers: “What is wrong, risky, inconsistent, or unproven in this scoped system?” It should:
1. establish scope, relevant lenses, assumptions, and exclusions;
2. build enough context to understand relevant entry points, flows, boundaries, and invariants;
3. gather evidence;
4. try to disprove candidate findings;
5. report only findings that survive the evidence gate;
6. state coverage gaps and unresolved questions;
7. stop without modifying the target.

## Capability boundary

Audit and diagnosis are report-only even when the investigation discovers a defect. `audit-lead` and
`audit-worker` must not edit or write the target, and `audit-worker` is intentionally denied shell execution
and delegation capabilities. Do not modify the target. Do not treat prompt instructions as a substitute for
tool-level restrictions.

If evidence gathering requires execution of a mutating or otherwise privileged command, stop and report the
missing capability instead of using an indirect workaround. A separate testing or implementation task is
required when execution is genuinely necessary.

Do not confuse a scanner alert, code smell, naming preference, or speculative future concern with a confirmed
finding.

## Diagnosis

Diagnosis answers: “Why is this behavior failing or occurring?” It should identify root cause, evidence,
confidence, affected scope, and any important missing evidence. It may recommend a fix, but it does not
implement the fix unless the user separately requests a change.

## Evidence and reporting

Structural claims cite exact file/line/function evidence; unknowns remain unknowns. Separate severity from
confidence. Run a false-positive check before reporting, and deduplicate findings by root cause. State coverage
gaps: "no findings" means none were established in the reviewed scope.

See the audit-protocol skill for the proof packet and procedure.
