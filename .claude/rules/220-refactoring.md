# Refactoring scope

Refactor when the existing structure directly blocks, obscures, or unnecessarily complicates the requested
change.

Prefer local, safe refactoring.

Do not turn feature work into repository-wide cleanup.

Do not rename or reorganize unrelated code merely because it could be cleaner.

Good opportunistic refactoring is:
- directly related to the changed behavior;
- low-risk;
- easy to verify;
- clearly simpler afterward.

Broad refactoring requires explicit scope.
