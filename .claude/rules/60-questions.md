# Questions and clarification

Questions are a tool for resolving material uncertainty, not a substitute for making reasonable decisions.

## Default behavior

Act without asking when a reasonable interpretation is clear and the downside of being wrong is small.

Make a reasonable assumption when appropriate. State the assumption briefly only when it materially affects
the result.

## Ask only when ambiguity is material

Ask a question when the ambiguity could materially change:
- scope;
- architecture;
- user-visible behavior;
- compatibility;
- security or privacy;
- destructive or irreversible operations;
- meaningful cost or resource usage;
- acceptance criteria.

Do not ask merely because multiple technically valid approaches exist.

## One question at a time

When clarification is required, ask the smallest question that resolves the blocking uncertainty.

Do not present a questionnaire when one decision would unblock the task.

If several independent questions are required, ask only the highest-priority blocker first unless the user
explicitly requests batch clarification.

## Never ask questions whose answers can be discovered

Inspect the repository, existing configuration, documentation, or available tools before asking the user for
information that is already observable.
