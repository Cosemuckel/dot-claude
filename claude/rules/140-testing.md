# Testing quality

Tests should establish meaningful behavior, not merely exercise lines of code.

## Test the contract

Prefer testing observable behavior and important invariants over implementation details.

Follow the repository's existing test structure and fixtures.

## Cover meaningful failure paths

Include relevant error, validation, permission, empty, boundary, and recovery behavior when applicable.

## Preserve test integrity

Do not weaken assertions, delete tests, or modify expected outcomes merely to make a change pass.

If a test is obsolete because the intended contract changed, update the test together with the implementation
and make the behavior change explicit.

## Determinism

Prefer deterministic tests.

Do not add sleeps or timing assumptions when a proper synchronization mechanism exists.

## Test scope

Run the narrowest relevant checks first, then the broader checks required by the task or repository workflow.
