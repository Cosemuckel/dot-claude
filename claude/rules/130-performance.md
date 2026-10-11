# Performance

Correctness and maintainability come before speculative optimization.

## Defaults

Do not optimize without evidence of a meaningful cost.

Avoid obvious accidental quadratic or worse behavior when a straightforward alternative exists.

Do not introduce caching, concurrency, batching, memoization, or background processing merely because they
could be faster.

Before making a performance claim, identify what was measured or what concrete evidence supports it.

Prefer simple optimizations with clear correctness and invalidation behavior.

Do not perform unrelated performance cleanup outside the task scope.
