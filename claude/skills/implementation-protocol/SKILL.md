---
name: implementation-protocol
description: Use when executing an approved implementation plan while keeping code changes bounded and verifiable.
user-invocable: false
---

# Implementation protocol

Execute the approved plan directly when the work is coupled or sequential.

Use a leaf worker only for a cleanly isolated implementation unit with a non-overlapping file/module boundary or
a genuinely independent side task.

Do not expand scope for unrelated cleanup. Preserve repository conventions.

Treat fresh repository evidence as authoritative over stale plan assumptions. When the plan materially conflicts
with the actual repository, surface the mismatch instead of improvising a new architecture silently.

Run focused local checks when practical, but leave final correctness to the independent testing stage.

Return files changed, behavioral/structural change, verification actually performed, and blockers/deviations only.
