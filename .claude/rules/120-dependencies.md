# Dependencies and external libraries

Before adding a dependency:

1. Check whether the repository already provides the capability.
2. Check whether the language/runtime/framework already provides it.
3. Check whether an existing dependency already solves the problem.
4. Consider compatibility, maintenance, size, security, and lifecycle implications.
5. Add the dependency only when it materially improves the solution.

Prefer established project dependencies over adding a second library for the same problem.

Do not upgrade unrelated dependencies during a feature task.

Do not replace a working library merely because another library is fashionable or superficially cleaner.

Keep dependency changes narrowly scoped and verify their effects.
