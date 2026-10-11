# Refactor / review playbook

Use for MODERATE or COMPLEX refactoring, cleanup, or structural review.

1. Establish current behavior and constraints.
2. Identify the specific complexity or defect the change should improve.
3. Choose the smallest safe refactor that addresses it; use planning only when the direction is materially ambiguous.
4. Preserve behavior unless a change is explicitly required.
5. Implement coupled work in one context; delegate only isolated non-overlapping units.
6. Verify with focused tests plus repository checks required by the change.
7. Review the final diff for unrelated churn.

Do not expand a local refactor into a repository-wide rewrite without explicit scope.
