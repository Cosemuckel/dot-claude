# Playbook routing

The orchestrator selects a playbook when a recurring workflow has several meaningful phases. The playbook is a
routing aid and checkpoint set, not a mandatory sequence. When selected, the responsible stage lead must read the
playbook file before executing the workflow.

Use:
- `feature-development` for substantial new functionality;
- `bug-fix` for incorrect behavior or regressions;
- `refactor-review` for focused restructuring/cleanup;
- `audit-review` for systematic report-only audits/investigations.

Do not invoke a playbook for:
- TRIVIAL tasks;
- ordinary SMALL implementation work;
- a narrow question;
- a narrow diagnosis/audit whose workflow is already obvious.

A playbook may omit research or planning when the task is already well understood. Do not create worker calls only
to make every checkpoint appear in the transcript.

Audit playbooks are report-only. They never grant permission to edit the target.
