---
name: audit-protocol
description: >-
  Use for report-only audits and diagnosis; build scoped evidence, validate findings against the code,
  separate severity from confidence, and never modify the target unless a separate change request is
  made.
user-invocable: false
---

# Audit / diagnosis protocol

Audit mode is evidence-first and report-only. Diagnosis mode is a narrower form of investigation whose goal is
to explain a concrete failure without implementing the fix. Neither mode silently becomes a change task.

## 1. Define the review boundary

Before hunting for problems, state:
- exact target scope;
- audit lens (correctness, security, reliability, architecture, performance, maintainability, compliance, or
the lenses actually requested);
- relevant threat model or runtime assumptions when they affect the conclusion;
- explicit exclusions;
- what evidence would count as sufficient coverage.

Do not silently broaden a bounded audit into a repository-wide survey.

## 2. Build context before verdicts

Understand the relevant entry points, data/control flows, trust boundaries, interfaces, dependencies, and
important invariants before classifying defects. Follow important calls across function/module boundaries
instead of judging a caller from names or local syntax alone.

Record assumptions and open questions explicitly. If an invariant or behavior cannot be established, say
`unclear` or `nothing found` rather than inferring it.

## 3. Use tools as evidence, not verdicts

Use static analysis, tests, scanners, browser checks, and documentation to guide investigation. A tool finding
is a candidate until the relevant code path and context are verified. Manual review should focus on gaps the
automated evidence cannot establish.

## 4. Every finding needs a proof packet

A real finding must have:
- ID and concise title;
- category/lens;
- severity: CRITICAL | HIGH | MEDIUM | LOW | INFO;
- confidence: HIGH | MEDIUM | LOW;
- exact location (file + line/function when available);
- concrete evidence;
- why the behavior violates the stated requirement/invariant or creates the stated risk;
- impact and reachable preconditions;
- reproduction or verification method when practical;
- recommended remediation, without applying it in audit mode;
- references when external standards or documentation materially support the claim.

Severity describes impact; confidence describes how well the evidence establishes the claim. Never use
confidence as a substitute for severity.

## 5. False-positive gate

Before reporting a finding, actively try to disprove it:
- Is the allegedly dangerous path reachable?
- Is there a protection elsewhere in the call chain?
- Does a contract, configuration, deployment assumption, or caller constraint invalidate the concern?
- Is the issue merely a style preference or speculative future problem?

If the premise fails, do not report it as a finding. If the issue is real but low-impact hardening, keep it
distinct from a vulnerability.

Do not assign severity until the finding survives this gate.

## 6. Deduplicate by root cause

Group multiple manifestations of one underlying defect. Avoid producing the same root cause repeatedly for
several call sites unless the differences materially change impact or remediation.

## 7. Report coverage and uncertainty

End the audit with:
- reviewed scope and lenses;
- findings by severity;
- important clean areas checked;
- coverage gaps;
- unresolved questions/assumptions;
- the next action the user can take.

A clean report means `no findings established in the reviewed scope`, not `the system is proven safe`.

## 8. Stop conditions

Stop when the requested scope has reasonable evidence coverage and the remaining work would only duplicate
established evidence, inspect out-of-scope material, or search for increasingly speculative issues.

For diagnosis, stop once the root cause is established to the requested confidence or the available evidence
is genuinely insufficient. Return the missing evidence rather than continuing indefinitely.
