# Audit and diagnosis methodology

This package treats auditing as a distinct evidence-producing activity, not as an unfinished implementation
pipeline. The design is informed by established code-review and security-review guidance: Google emphasizes
design, functionality, complexity, tests, and maintainability; GitLab recommends concrete scope, actionable
findings, small review surfaces, and domain-aware coverage; OWASP recommends combining automated scanning with
manual investigation and explicitly documenting findings, impact, reproduction, and remediation; Trail of Bits
emphasizes context building, explicit invariants/assumptions, exact evidence, threat-model-aware verification,
and false-positive filtering.

Reference material:
- Google Engineering Practices — Code Review: https://google.github.io/eng-practices/review/
- GitLab Code Review Guidelines: https://docs.gitlab.com/development/code_review/
- OWASP Secure Code Review Cheat Sheet:
https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
- Trail of Bits audit-context-building:
https://github.com/trailofbits/skills/tree/main/plugins/audit-context-building
- Trail of Bits false-positive verification: https://github.com/trailofbits/skills/tree/main/plugins/fp-check

## Practical rules adopted here

**Scope before depth.** An audit names its target and review lens before investigators fan out. A bounded
audit is not silently expanded into a repository-wide survey.

**Context before verdicts.** Investigators establish entry points, flows, boundaries, dependencies, and
invariants before classifying a suspected problem. Claims should point to concrete evidence rather than names
or surface patterns.

**Tools are signals.** Scanners and tests can find candidates and coverage gaps, but they do not replace
code-path verification.

**Every real finding is a proof packet.** The report identifies where the issue is, what evidence establishes
it, why it matters, what preconditions are required, and how it can be reproduced or otherwise verified.

**Severity and confidence are separate.** Severity describes impact; confidence describes evidentiary
strength. A high-confidence low-impact issue is not a high-severity issue, and a high-severity hypothesis with
weak evidence should remain unresolved rather than being overstated.

**Try to disprove the finding.** Before reporting a candidate, check reachability, protections elsewhere in
the flow, configuration, contracts, and threat-model assumptions. This is an explicit false-positive gate.

**Do not turn preferences into defects.** Style opinions and speculative future improvements belong in
recommendations or notes, not substantive findings.

**Deduplicate by cause.** Multiple symptoms of one root cause should normally be one finding with multiple
affected locations.

**Report coverage and gaps.** A useful audit says what was examined, what was not, and what remains unclear.
“No findings” is scoped to the reviewed evidence; it is not a proof of absence.

**Stop at evidence sufficiency.** Once the requested scope is covered and remaining work would mainly generate
duplicate or speculative findings, stop. Audit quality is not proportional to the number of pages inspected or
findings produced.
