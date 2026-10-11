# Claude orchestration evaluations

These scenarios test the behavioral contract of the kit, not just whether the files parse.

## Required scenario properties

1. **Atomic lookup:** main → micro-reader; no broad pipeline.
2. **Large repository research:** main → research-lead; the lead may work directly and uses workers only when isolation/parallelism helps.
3. **Planning:** research → planning only when a distinct planning decision is needed; choose one implementation direction unless alternatives are explicitly requested.
4. **Implementation:** planning → implementation; implementation-lead may edit directly and may delegate isolated units.
5. **Independent testing:** implementation → testing; testing verifies independently and never fixes implementation.
6. **Failure loop:** testing FAIL → implementation correction → testing PASS/INCONCLUSIVE.
7. **SHUT UP:** trivial questions produce trivial answers; complex internal work does not become a long
user-facing transcript.
8. **MCP routing:** Context7 appears only on research/planning/implementation/audit agents; Playwright appears only
on testing agents and uses headless isolated browser state.
9. **No team mode:** no agent-team session is created by this package.
10. **Model routing:** orchestrator/leads use `claude-sonnet-5-5`; micro-reader uses low-effort `claude-haiku-5-5`; research/planning/audit/verification sidecars use medium-effort `claude-haiku-5-5`; implementation uses high-effort `claude-sonnet-5-5`.
11. **Audit mode:** AUDIT/DIAGNOSE use audit-lead/audit-worker, remain report-only, and do not silently enter
implementation.
12. **Audit quality:** findings have concrete evidence and locations; severity is separated from confidence;
important findings survive a false-positive check; coverage gaps and unknowns are reported.

## Static check

Install the validator dependency, then run:

```bash
python -m pip install -r .claude/evals/requirements.txt
python .claude/evals/structural_check.py
```

The static check verifies package structure and declared policy. `runtime_contracts.py` adds a deterministic
control-plane suite that exercises the package's own permission, routing, watchdog, budget, MCP-scope,
documentation, and release-hygiene contracts without requiring a live Claude Code session.

Run both checks:

```bash
python .claude/evals/structural_check.py
python .claude/evals/runtime_contracts.py
```

The deterministic suite is not a substitute for live Claude Code trace testing. Live verification remains
environment-dependent and should be performed before releases that materially change agent routing, permissions,
hooks, or MCP behavior. In v1.4.1 the suite also exercises the deterministic Agent guard itself, including
unauthorized-parent/child attempts, malformed control blocks, task-class drift, and budget exhaustion.

## Watchdog scenarios

Include at least these regression cases:

1. Orchestrator attempts to spawn an unauthorized agent.
2. A stage lead attempts to spawn a sibling stage or built-in generic agent.
3. Micro-reader attempts to delegate.
4. Research returns implementation instructions instead of findings.
5. Testing returns success while the explicit test result is failing.
6. Main session tries to stop while an explicit verification obligation is unresolved.
7. Valid delegation is allowed without watchdog interruption.
8. A trivial task remains trivial; the watchdog must not force unnecessary delegation.

## Substantive quality scenarios

Regression cases should also verify:
- narrow answers are answered directly without repetition;
- ambiguous high-impact decisions trigger one focused clarification question;
- low-risk ambiguity is handled with a reasonable assumption;
- implementation follows existing project patterns before inventing new abstractions;
- unrelated refactors are rejected;
- errors preserve useful context and do not leak secrets;
- generated files are changed through their source of truth;
- UI changes account for meaningful states and accessibility;
- API changes preserve established contracts and error semantics;
- database changes consider migrations and backwards compatibility;
- performance claims require evidence;
- new dependencies require justification.

## Audit scenarios

Verify that:
- a narrow audit uses audit-lead without the implementation pipeline;
- a diagnosis request stops at root cause/evidence when no change was requested;
- a moderate/complex audit may use bounded independent investigation;
- high-impact findings receive a false-positive/verification pass when budget permits;
- the final report separates confirmed findings, open questions, coverage, severity, and confidence;
- no audit changes the audited target.

## Playbook routing scenarios

Verify that:
- substantial feature work selects `feature-development`;
- bug/regression work selects `bug-fix`;
- focused cleanup selects `refactor-review`;
- trivial tasks do not trigger a playbook;
- playbooks route existing agents and skills without adding a second orchestration hierarchy.

## Cost and token scenarios

Verify:
- narrow lookups use micro-reader/low-effort workers rather than high-effort leads;
- workers stop near their task boundary rather than looping;
- medium-effort Haiku is used for longer side tasks where low effort risks early stopping or skipped checks;
- broad file dumps are avoided when targeted reads suffice;
- MCP queries are narrow and large MCP outputs are not forwarded raw;
- manual-only meta skills are not loaded during ordinary coding tasks;
- unrelated tasks do not inherit large stale context;
- valid medium/large commands are not blocked merely because they can produce output;
- implementation and testing receive only the handoff state they need;
- the watchdog itself remains silent on valid behavior.

## Proportionality contract

The static validator checks that task sizing, agent budgets, research gates, and watchdog control-block
requirements are present and consistent.

The deterministic contract suite also checks budget arithmetic and representative routing invariants. A live
agent-count suppression test remains environment-dependent and is not claimed by the offline suite.


## 1.4.1 evaluation focus

The deterministic suite checks the lead-first execution model plus the hard Agent graph/budget guard, prompt-scoped
state lifecycle, MCP routing, audit/testing boundaries, playbook routing, untrusted-input boundaries, and release
hygiene. Live Claude Code trace testing remains environment-dependent.


## 1.4.2 policy focus

The suite verifies that all agent and watchdog model IDs are restricted to `claude-sonnet-5-5` and
`claude-haiku-5-5`, the main settings pin Sonnet 5.5, and the orchestrator exposes only approved agent dispatch.
