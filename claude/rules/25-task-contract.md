# Task contract

Every non-trivial delegated task should have a bounded contract.

Use the fields that are relevant; do not fill fields with invented detail.

## Objective

What exact result is required?

## Context

What facts or prior work does the worker need?

## Scope

Which files, components, systems, or behaviors are in scope?

## Constraints

What must remain unchanged? What tools, technologies, or boundaries matter?

## Starting state

What is known to be true before the work begins?

## Target state

What should be true after successful completion?

## Allowed actions

What may the worker do?

## Forbidden actions

What must the worker not do?

## Done when

What observable condition establishes completion?

## Stop conditions

When should the worker stop rather than continue exploring?

## Handoff

Return only the information required by the caller. Include important failed approaches or unresolved blockers
so downstream agents do not repeat them.

Prefer positive action instructions ("inspect X", "return Y") and use prohibitions only where a hard boundary
is needed.
