# Code quality and style defaults

These are general engineering defaults. Existing project conventions and explicit user requirements take
precedence.

## Readability

Prefer clear, explicit code over clever or compressed code.

Prefer straightforward control flow over deeply nested logic.

Keep functions and modules focused.

Use names that communicate intent.

## Abstraction

Prefer local, simple solutions when the problem is local.

Do not introduce abstractions merely to avoid a small amount of duplication.

Abstract when there is a demonstrated repeated concept, a stable interface, or a real reduction in complexity.

## Types and contracts

Use the strongest practical type guarantees supported by the language and project.

Prefer explicit contracts at module and API boundaries.

Do not weaken types merely to make an implementation easier.

## Comments

Comments explain why, constraints, or non-obvious behavior.

Do not write comments that merely narrate obvious code.

Remove stale comments when changing the behavior they describe.

## Imports and formatting

Follow the project's existing formatter, linter, import ordering, and module conventions.

Do not invent a formatting style when the repository already has one.

## Existing patterns

When the repository already has a pattern for the problem, follow that pattern unless there is concrete
evidence it should change.
