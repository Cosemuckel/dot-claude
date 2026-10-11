# Verification

Implementation is not proof. Verification must use actual artifact state and actual check results.

A testing PASS requires evidence. If checks were skipped, could not run, or do not establish the requested
outcome, report INCONCLUSIVE rather than PASS.

Testing is independent from implementation. When implementation is wrong, testing reports the concrete
failure; implementation receives the failure and changes the code; testing verifies again.

Never turn an assumption, visual impression, or successful tool invocation into a claim of correctness.
