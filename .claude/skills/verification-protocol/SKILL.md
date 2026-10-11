---
name: verification-protocol
description: >-
  Use when independently validating an implementation, regression, test suite, build, lint, typecheck,
  browser behavior, or other concrete success criterion.
user-invocable: false
---

# Verification protocol

Verify the actual artifact, not the implementation agent's claim.

Select the smallest set of checks that establishes the user's requested outcome. Run independent checks in
parallel when they do not share state or ordering dependencies.

For long or noisy checks, use a test-runner sidecar when the parent only needs the verdict and evidence.

For browser work, use Playwright when real browser state or interaction must be observed. Keep browser exploration
inside the testing context.

Report exactly one status: PASS, FAIL, or INCONCLUSIVE.

PASS requires actual evidence. FAIL requires concrete failure evidence. INCONCLUSIVE means the available checks do
not establish correctness.

Do not silently fix source code during verification.
