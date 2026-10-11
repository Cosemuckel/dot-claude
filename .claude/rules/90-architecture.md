# Architecture and technical decisions

Use this when making implementation or architecture decisions.

## Prefer the smallest sufficient boundary

Prefer:
1. existing abstraction that already fits;
2. small local abstraction;
3. shared abstraction;
4. new subsystem;

unless evidence justifies the more expensive option.

## Avoid unnecessary distribution

Do not introduce a service, queue, cache, worker, event bus, or other distributed component without a concrete
requirement.

Distributed complexity is justified by actual scale, isolation, reliability, or operational requirements.

## Preserve interfaces

Avoid breaking public or cross-component contracts unless the task explicitly requires it.

When a contract must change, identify affected callers and verification requirements.

## Keep responsibilities coherent

Do not duplicate domain rules across multiple layers.

Keep authoritative business logic in one clear location where practical.

## Decision quality

Prefer evidence over assumptions.

Prefer reversible decisions when uncertainty is high.

Prefer existing project conventions over personal taste.

When two solutions are both valid, prefer the one with fewer moving parts and lower long-term maintenance
cost, unless the project context indicates otherwise.
