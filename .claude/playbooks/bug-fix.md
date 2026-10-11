# Bug fix playbook

Use for MODERATE or COMPLEX bug/regression work. TRIVIAL/SMALL fixes should use the narrowest direct path when the
failure and remedy are already clear.

1. Establish or reproduce the failure with evidence.
2. Trace the relevant implementation and identify root cause. Use a research sidecar only when the investigation
   is context-heavy or independent.
3. Choose the smallest sound fix; use planning when the repair has meaningful design ambiguity.
4. Implement the fix directly when practical.
5. Add or update regression coverage when appropriate.
6. Independently verify the relevant behavior.
7. Report the observed cause, change, and verification result.

Do not patch symptoms before understanding the failure. Do not weaken tests to make the failure disappear. If the
issue cannot be reproduced, report what evidence is missing instead of inventing a fix.
