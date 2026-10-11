# Audit / investigation playbook

Use for MODERATE or COMPLEX report-only audits. Small, focused audits should stay on the narrowest direct
`audit-lead` path.

1. Define the exact scope, audit lenses, assumptions, and exclusions.
2. Establish relevant context: entry points, flows, trust boundaries, dependencies, invariants, and
surrounding implementation.
3. Run targeted evidence gathering; use automated tools as signals, not verdicts.
4. Build candidate findings with exact evidence and locations.
5. Apply a false-positive gate to important findings; for high-impact claims, use an independent verification
pass when budget permits.
6. Deduplicate by root cause and separate confirmed findings from open questions.
7. Produce the audit report with severity, confidence, evidence, coverage, gaps, and remediation
recommendations.
8. Stop. Do not modify the target or start implementation as part of the audit.

Diagnosis uses the same playbook when the user's goal is to explain a concrete failure rather than to survey
the system for broader findings. In that case, prioritize root cause and confidence over a wide finding
taxonomy.
