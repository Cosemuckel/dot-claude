# Observability

For behavior that matters operationally, make failures diagnosable.

Prefer the project's established logging, metrics, tracing, and request/correlation identifiers.

Include useful context without exposing secrets or sensitive data.

Use structured logs when the project supports them.

Do not add noisy logging merely to make an implementation feel observable.

When changing critical workflows, consider how an operator would diagnose:
- success;
- failure;
- latency;
- retries;
- partial failure;
- unexpected state.
