#!/usr/bin/env python3
"""Deterministic, fail-open Stop-hook heuristic for the Claude Orchestration Kit.

Replaces the former model-based Stop prompt hook. That hook ran on every turn end,
including turns that ended only to wait for background subagents, and kept blocking
them in a loop.

Design constraints:
- Fail open: any parse error or internal exception exits 0 without blocking. This hook
  never exits 2.
- Heuristic only: it blocks one narrow contradiction, a final message that claims
  completion while also reporting an unresolved FAIL/INCONCLUSIVE status.
- One-shot: when `stop_hook_active` is true a previous block was already issued, so
  the hook allows the stop instead of looping.
- The transcript (`transcript_path`) is deliberately not read; only the
  `last_assistant_message` field of the hook payload is inspected.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any

WAITING_RE = re.compile(
    r"\b(still (waiting|running|in progress)|waiting (for|on)|awaiting|in the background"
    r"|background (task|agent|subagent)s?|will (be notified|notify|report back))\b",
    re.IGNORECASE,
)
COMPLETION_RE = re.compile(
    r"\b(all (checks|tests) pass(ed)?|(is|are|was) (now )?(complete|completed|done|fixed|verified)"
    r"|successfully (implemented|completed|fixed))\b",
    re.IGNORECASE,
)
UNRESOLVED_RE = re.compile(r"\b(FAIL|FAILED|INCONCLUSIVE)\b")

BLOCK_REASON = (
    "Final message claims completion but also reports an unresolved FAIL/INCONCLUSIVE status. "
    "Report the failure as unresolved, or obtain verification evidence through testing-lead, then finish."
)


def evaluate_stop(payload: dict[str, Any]) -> tuple[bool, str]:
    """Return (allow, reason). `reason` is non-empty only when the stop is blocked."""
    if payload.get("stop_hook_active") is True:
        return True, ""

    message = payload.get("last_assistant_message")
    if not isinstance(message, str) or not message.strip():
        return True, ""

    if WAITING_RE.search(message):
        return True, ""

    if COMPLETION_RE.search(message) and UNRESOLVED_RE.search(message):
        return False, BLOCK_REASON

    return True, ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(f"stop guard could not parse hook input; allowing stop: {type(exc).__name__}", file=sys.stderr)
        return 0

    try:
        if not isinstance(payload, dict) or payload.get("hook_event_name") != "Stop":
            return 0
        allow, reason = evaluate_stop(payload)
        if not allow:
            print(json.dumps({"decision": "block", "reason": reason}))
    except Exception as exc:
        print(f"stop guard failed open: {type(exc).__name__}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
