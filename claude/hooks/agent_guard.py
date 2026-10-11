#!/usr/bin/env python3
"""Deterministic Agent-tool policy gate for the Claude Orchestration Kit.

The hook enforces the hard runtime parts of the orchestration contract that are
not safely left to prompt judgment: parent -> child graph, named child
requirement, task-class consistency, and the non-resetting descendant-agent
budget for the current user prompt.

Semantic proportionality remains in the prompt watchdog in settings.json.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

TASK_BUDGETS = {
    "TRIVIAL": 4,
    "SMALL": 6,
    "MODERATE": 12,
    "COMPLEX": 24,
}

ALLOWED_CHILDREN = {
    "orchestrator": {
        "research-lead",
        "planning-lead",
        "implementation-lead",
        "testing-lead",
        "audit-lead",
        "micro-reader",
    },
    "research-lead": {"research-worker", "micro-reader"},
    "planning-lead": {"plan-worker", "micro-reader"},
    "implementation-lead": {"implementation-worker", "micro-reader"},
    "testing-lead": {"test-runner", "micro-reader"},
    "audit-lead": {"audit-worker", "micro-reader"},
}

CONTROL_MARKER = "ORCHESTRATION CONTROL"


def parse_control(text: str) -> tuple[dict[str, Any] | None, str | None]:
    """Parse the mandatory orchestration control block from a handoff prompt."""
    if CONTROL_MARKER not in text:
        return None, "Every Agent handoff must include an ORCHESTRATION CONTROL block."

    block = text.split(CONTROL_MARKER, 1)[1]
    block = block.split("\n\n", 1)[0]
    import re

    patterns = {
        "class": r"(?mi)^class:\s*(TRIVIAL|SMALL|MODERATE|COMPLEX)\s*$",
        "budget_before": r"(?mi)^budget_before:\s*(\d+)\s*$",
        "budget_after": r"(?mi)^budget_after:\s*(\d+)\s*$",
        "purpose": r"(?mi)^purpose:\s*(\S.*)$",
        "research": r"(?mi)^research:\s*(forbidden|exception-only|allowed)\s*$",
    }
    values: dict[str, Any] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, block)
        if not match:
            return None, f"ORCHESTRATION CONTROL is missing or malformed: {key}."
        values[key] = match.group(1).strip()

    values["budget_before"] = int(values["budget_before"])
    values["budget_after"] = int(values["budget_after"])
    return values, None


def _child_type(tool_input: dict[str, Any]) -> str | None:
    value = tool_input.get("subagent_type")
    if isinstance(value, str) and value.strip():
        return value.strip()
    # Defensive compatibility for a future tool-schema rename.
    value = tool_input.get("agent_type")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def evaluate_agent_call(
    payload: dict[str, Any], state: dict[str, Any] | None
) -> tuple[bool, str, dict[str, Any] | None]:
    """Evaluate a proposed Agent call and return the updated ledger on success."""
    if payload.get("hook_event_name") != "PreToolUse" or payload.get("tool_name") != "Agent":
        return True, "not an Agent PreToolUse event", state

    parent = payload.get("agent_type")
    if not isinstance(parent, str) or not parent:
        return False, "The main session must run as the `orchestrator` agent before it can delegate.", state

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return False, "Agent tool input is missing or malformed; delegation is blocked.", state

    child = _child_type(tool_input)
    if child is None:
        return False, "Name the target subagent with `subagent_type`; unnamed delegation is blocked.", state

    allowed = ALLOWED_CHILDREN.get(parent, set())
    if child not in allowed:
        allowed_text = ", ".join(sorted(allowed)) if allowed else "none"
        return False, f"`{parent}` cannot spawn `{child}`. Allowed child types: {allowed_text}.", state

    prompt = tool_input.get("prompt")
    if not isinstance(prompt, str):
        prompt = tool_input.get("description")
    if not isinstance(prompt, str):
        return False, "Agent handoff text is missing; include the ORCHESTRATION CONTROL block in the prompt.", state

    control, error = parse_control(prompt)
    if error:
        return False, error, state

    task_class = control["class"]
    total = TASK_BUDGETS[task_class]
    before = control["budget_before"]
    after = control["budget_after"]
    if before < 1 or before > total:
        return False, f"`budget_before` must be between 1 and {total} for {task_class}.", state
    if after != before - 1:
        return False, "`budget_after` must equal `budget_before - 1`.", state

    current = dict(state or {})
    current_class = current.get("class")
    if current_class is not None and current_class != task_class:
        return False, (
            f"Task class cannot change within one user prompt: ledger is {current_class}, "
            f"request says {task_class}."
        ), state

    consumed = int(current.get("consumed", 0))
    if consumed >= total:
        return False, f"The {task_class} descendant-agent budget is exhausted ({total} calls).", state

    current["class"] = task_class
    current["budget_total"] = total
    current["consumed"] = consumed + 1
    return True, "allowed", current


def _session_dir(payload: dict[str, Any]) -> Path:
    session_id = str(payload.get("session_id") or "session")
    cwd = str(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    token = hashlib.sha256(f"{cwd}\0{session_id}".encode("utf-8")).hexdigest()[:24]
    return Path(tempfile.gettempdir()) / "claude-orchestration-kit" / token


def _prompt_key(payload: dict[str, Any]) -> str:
    prompt_id = payload.get("prompt_id")
    if not isinstance(prompt_id, str) or not prompt_id:
        raise ValueError("Claude Code did not provide prompt_id; refusing to guess task-boundary state")
    return hashlib.sha256(prompt_id.encode("utf-8")).hexdigest()[:24]


class _FileLock:
    """Tiny cross-platform lock based on exclusive lock-file creation."""

    def __init__(self, path: Path, timeout: float = 4.0):
        self.path = path
        self.timeout = timeout
        self.acquired = False

    def __enter__(self):
        deadline = time.monotonic() + self.timeout
        self.path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="ascii") as handle:
                    handle.write(f"{os.getpid()} {time.time()}\n")
                self.acquired = True
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > 30:
                        self.path.unlink(missing_ok=True)
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() >= deadline:
                    raise TimeoutError("orchestration guard state lock timed out")
                time.sleep(0.03)

    def __exit__(self, exc_type, exc, tb):
        if self.acquired:
            self.path.unlink(missing_ok=True)


def _state_path(payload: dict[str, Any]) -> tuple[Path, Path]:
    directory = _session_dir(payload)
    key = _prompt_key(payload)
    return directory / f"{key}.json", directory / ".lock"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    temp.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")
    os.replace(temp, path)


def _cleanup_session(payload: dict[str, Any]) -> None:
    directory = _session_dir(payload)
    if not directory.exists():
        return
    for child in directory.glob("*.json"):
        child.unlink(missing_ok=True)
    (directory / ".lock").unlink(missing_ok=True)
    try:
        directory.rmdir()
        directory.parent.rmdir()
    except OSError:
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(f"orchestration guard could not parse hook input: {exc}", file=sys.stderr)
        return 2

    if payload.get("hook_event_name") == "SessionEnd":
        _cleanup_session(payload)
        return 0

    if payload.get("hook_event_name") != "PreToolUse" or payload.get("tool_name") != "Agent":
        return 0

    state_path, lock_path = _state_path(payload)
    try:
        with _FileLock(lock_path):
            state = _read_json(state_path)
            ok, reason, updated = evaluate_agent_call(payload, state)
            if ok and updated is not None:
                _write_json_atomic(state_path, updated)
    except TimeoutError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"orchestration guard failed closed: {exc}", file=sys.stderr)
        return 2

    if not ok:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
