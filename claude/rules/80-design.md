# Design principles

Use these defaults when designing features or changing behavior.

## Simplicity first

Prefer the simplest design that satisfies the requirement.

Minimize moving parts, state transitions, abstractions, and dependencies.

Do not add infrastructure because it is available.

## Reuse existing patterns

Prefer established repository patterns, components, helpers, services, and abstractions.

Do not create a parallel system when an existing one can be extended cleanly.

## Explicit boundaries

Give components clear responsibilities and interfaces.

Keep domain logic separated from transport, persistence, and presentation concerns where the project
architecture calls for it.

## Failure behavior

Consider important failure states, partial failures, retries, cancellation, and recovery when they are
relevant to the feature.

Do not design only the happy path when failure is a meaningful part of the contract.

## User-visible behavior

Preserve existing behavior unless a change is required by the task.

Consider loading, empty, error, permission, disabled, and partial-data states where applicable.

## Scope discipline

Do not turn a feature into a general redesign.

A local improvement is preferable to a broad refactor when both satisfy the requirement.
