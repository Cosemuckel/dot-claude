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

## Evidence standard

Structural claims should cite exact file/line/function evidence when available. Follow important call chains
and cross-boundary dependencies instead of inferring behavior from names. Unknowns remain unknowns.

## Finding quality

Separate severity from confidence. Severity describes impact if the finding is real; confidence describes how
strongly the evidence establishes the claim. High severity requires a concrete impact mechanism and relevant
reachability/preconditions.

Every substantive finding should include a location, evidence, impact, verification/reproduction method when
practical, and a specific remediation recommendation.

Before reporting, perform a false-positive check: look for protections, reachability constraints, contracts,
configuration, deployment assumptions, or other code that invalidates the candidate.

Deduplicate multiple manifestations of the same root cause. Prefer a smaller set of strong findings over a
large list of speculative ones.

## Coverage

A report must state what was reviewed and what was not. “No findings” means none were established in the
reviewed scope; it is not proof that the system is defect-free.
