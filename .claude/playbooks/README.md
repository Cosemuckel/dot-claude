# Playbooks

Playbooks define useful checkpoints for recurring multi-phase tasks. They are workflow contracts, not mandatory
agent sequences.

Use a playbook when a task has several meaningful phases, meaningful uncertainty, or multiple specialist roles.
The orchestrator may omit phases that add no value.

When a playbook is selected, the caller passes the exact playbook filename to the responsible lead. The lead reads
that file before executing the workflow. Playbooks are ordinary Markdown routing contracts, not an additional runtime
agent hierarchy.

They do not replace:
- rules: persistent constraints;
- skills: reusable procedures and reference-heavy guidance;
- agents: stage owners and optional isolated sidecars;
- MCP: external capabilities;
- watchdog: process supervision.

Do not use a playbook for trivial lookups, tiny edits, simple questions, or a narrow diagnostic/audit task whose
workflow is already obvious. A selected playbook does not create another orchestration tier.
