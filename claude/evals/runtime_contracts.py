#!/usr/bin/env python3
"""Deterministic control-plane checks for the Claude orchestration package.

This suite validates the package declarations and directly exercises the deterministic
Agent guard with representative allowed/blocked calls. It does not claim to be a live
Claude Code integration test; live trace verification remains environment-dependent.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    print("FAIL")
    print(" - missing dependency: PyYAML; install with `python -m pip install -r .claude/evals/requirements.txt`")
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
AGENTS = ROOT / "agents"
RULES = ROOT / "rules"
errors: list[str] = []

def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(PROJECT)}: missing frontmatter")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        errors.append(f"{path.relative_to(PROJECT)}: unterminated frontmatter")
        return {}
    try:
        data = yaml.safe_load(text[4:end]) or {}
    except Exception as exc:
        errors.append(f"{path.relative_to(PROJECT)}: invalid YAML: {exc}")
        return {}
    return data if isinstance(data, dict) else {}

def agent(name: str) -> dict:
    return load_frontmatter(AGENTS / f"{name}.md")

def tools_for(name: str) -> set[str]:
    raw = str(agent(name).get("tools", ""))
    return {part.strip() for part in raw.split(",") if part.strip()}

def disallowed_for(name: str) -> set[str]:
    value = agent(name).get("disallowedTools", []) or []
    if isinstance(value, list):
        return {str(x).strip() for x in value if str(x).strip()}
    if isinstance(value, str):
        return {x.strip() for x in value.split(",") if x.strip()}
    return {str(value).strip()}

def load_hook(name: str):
    path = ROOT / "hooks" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_guard():
    return load_hook("agent_guard")

def hook_ref(hook: dict) -> str:
    return hook.get("command", "") + " " + " ".join(str(a) for a in hook.get("args", []))

def control(task_class: str, before: int, purpose: str = "bounded verification") -> str:
    after = before - 1
    return ("ORCHESTRATION CONTROL\n"
            f"class: {task_class}\n"
            f"budget_before: {before}\n"
            f"budget_after: {after}\n"
            f"purpose: {purpose}\n"
            "research: forbidden")

def payload(parent: str, child: str | None = None, task_class: str = "MODERATE", before: int = 12) -> dict:
    tool_input = {}
    if child is not None:
        tool_input["subagent_type"] = child
        tool_input["prompt"] = control(task_class, before)
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "session_id": "runtime-test",
        "prompt_id": "prompt-runtime-test",
        "agent_type": parent,
        "tool_input": tool_input,
    }

def check_declared_graph() -> None:
    expected = {
        "orchestrator": {"research-lead", "planning-lead", "implementation-lead", "testing-lead", "audit-lead", "micro-reader"},
        "research-lead": {"research-worker", "micro-reader"},
        "planning-lead": {"plan-worker", "micro-reader"},
        "implementation-lead": {"implementation-worker", "micro-reader"},
        "testing-lead": {"test-runner", "micro-reader"},
        "audit-lead": {"audit-worker", "micro-reader"},
    }
    for owner, want in expected.items():
        raw = str(agent(owner).get("tools", ""))
        actual = set()
        for match in re.findall(r"Agent\(([^)]+)\)", raw):
            actual.update(x.strip() for x in match.split(","))
        if actual != want:
            errors.append(f"{owner}: declared graph drifted; expected {sorted(want)}, got {sorted(actual)}")

def check_capability_boundaries() -> None:
    settings = json.loads((ROOT / "settings.json").read_text(encoding="utf-8"))
    if settings.get("model") != "claude-sonnet-5-5":
        errors.append("main session model is not pinned to claude-sonnet-5-5")
    allowed = {"claude-sonnet-5-5", "claude-haiku-5-5"}
    for path in sorted(AGENTS.glob("*.md")):
        data = load_frontmatter(path)
        if data.get("model") not in allowed:
            errors.append(f"{data.get('name', path.stem)} uses an unapproved model: {data.get('model')!r}")
    if str(agent("orchestrator").get("tools", "")) != "Agent(research-lead, planning-lead, implementation-lead, testing-lead, audit-lead, micro-reader)":
        errors.append("orchestrator is not restricted to approved Agent dispatch only")
    orch_text = (AGENTS / "orchestrator.md").read_text(encoding="utf-8").lower()
    if "sole permitted tool" not in orch_text or "repository files or inspect project contents" not in orch_text:
        errors.append("orchestrator agent-only boundary is not explicit")
    if tools_for("micro-reader") != {"Read", "Grep", "Glob"}:
        errors.append("micro-reader capability drifted")
    for name in ["research-worker", "plan-worker", "implementation-worker", "test-runner", "audit-worker", "micro-reader"]:
        if "Agent" not in disallowed_for(name):
            errors.append(f"{name} must disallow Agent")
    if "Bash" in tools_for("audit-worker") or {"Edit", "Write"} & tools_for("audit-worker"):
        errors.append("audit-worker must remain capability-level read-only")
    for name in ["testing-lead", "test-runner"]:
        if not {"Edit", "Write"}.issubset(disallowed_for(name)):
            errors.append(f"{name} must disallow Edit and Write")

def check_watchdogs(settings: dict) -> None:
    hooks = settings.get("hooks", {})
    prompt_count = 0
    for group, entries in hooks.items():
        for entry in entries:
            for hook in entry.get("hooks", []):
                if hook.get("type") == "prompt":
                    prompt_count += 1
                    if hook.get("model") != "claude-haiku-5-5":
                        errors.append(f"{group} prompt watchdog model drifted from claude-haiku-5-5")
                    if "$ARGUMENTS" not in hook.get("prompt", ""):
                        errors.append(f"{group} prompt watchdog does not inspect $ARGUMENTS")
    if prompt_count != 3:
        errors.append(f"expected three semantic prompt watchdogs, got {prompt_count}")
    agent_entry = next((e for e in hooks.get("PreToolUse", []) if e.get("matcher") == "Agent"), None)
    if not agent_entry or not any(h.get("type") == "command" and "agent_guard.py" in hook_ref(h) for h in agent_entry.get("hooks", [])):
        errors.append("Agent PreToolUse hook lacks deterministic guard")
    session_end = hooks.get("SessionEnd", [])
    if not any(any(h.get("type") == "command" and "agent_guard.py" in hook_ref(h) for h in e.get("hooks", [])) for e in session_end):
        errors.append("SessionEnd cleanup hook is missing")
    stop_hooks = [h for e in hooks.get("Stop", []) for h in e.get("hooks", [])]
    if not any(h.get("type") == "command" and "stop_guard.py" in hook_ref(h) for h in stop_hooks):
        errors.append("Stop group lacks the deterministic stop_guard.py command hook")
    if any(h.get("type") == "prompt" for h in stop_hooks):
        errors.append("Stop group must not contain a prompt hook")


def check_stop_guard() -> None:
    stop = load_hook("stop_guard")

    def stop_payload(message, active=False, event="Stop") -> dict:
        data = {"hook_event_name": event, "stop_hook_active": active}
        if message is not None:
            data["last_assistant_message"] = message
        return data

    allow, _ = stop.evaluate_stop(stop_payload("Still waiting on research-lead running in the background. The fix is complete. Status: FAIL"))
    if not allow:
        errors.append("stop guard blocked a message that is waiting on background work")
    allow, _ = stop.evaluate_stop(stop_payload("The fix is complete. Status: FAIL", active=True))
    if not allow:
        errors.append("stop guard blocked despite stop_hook_active (must be one-shot)")
    allow, _ = stop.evaluate_stop(stop_payload("All checks passed. PASS"))
    if not allow:
        errors.append("stop guard blocked a verified completion message")
    allow, reason = stop.evaluate_stop(stop_payload("The fix is complete. Status: FAIL"))
    if allow or not reason:
        errors.append("stop guard failed to block a completion claim with unresolved FAIL")
    for message in ("", "   ", None):
        allow, _ = stop.evaluate_stop(stop_payload(message))
        if not allow:
            errors.append(f"stop guard blocked an empty or missing message ({message!r})")

    script = ROOT / "hooks" / "stop_guard.py"
    blocking = json.dumps(stop_payload("The fix is complete. Status: FAIL"))
    proc = subprocess.run([sys.executable, str(script)], input=blocking, capture_output=True, text=True, timeout=20)
    try:
        decision = json.loads(proc.stdout)
    except ValueError:
        decision = {}
    if proc.returncode != 0 or decision.get("decision") != "block" or not decision.get("reason"):
        errors.append("stop_guard.py did not emit a block decision with exit 0 for a contradictory message")
    other = json.dumps(stop_payload("The fix is complete. Status: FAIL", event="SubagentStop"))
    proc = subprocess.run([sys.executable, str(script)], input=other, capture_output=True, text=True, timeout=20)
    if proc.returncode != 0 or proc.stdout.strip():
        errors.append("stop_guard.py acted on a non-Stop event")
    proc = subprocess.run([sys.executable, str(script)], input="not json {{{", capture_output=True, text=True, timeout=20)
    if proc.returncode != 0 or proc.stdout.strip():
        errors.append("stop_guard.py must fail open (exit 0, no block) on garbage stdin")


def check_runtime_guard() -> None:
    guard = load_guard()
    # Valid parent -> child.
    ok, _, state = guard.evaluate_agent_call(payload("orchestrator", "research-lead"), None)
    if not ok or state.get("consumed") != 1:
        errors.append("guard rejected a valid orchestrator -> research-lead call")
    # Same prompt, same task class: another sibling consumes another unit.
    ok, _, state = guard.evaluate_agent_call(payload("orchestrator", "planning-lead", before=11), state)
    if not ok or state.get("consumed") != 2:
        errors.append("guard failed to account for a second valid accepted Agent call")
    # Lead cannot spawn sibling stage.
    ok, reason, _ = guard.evaluate_agent_call(payload("research-lead", "planning-lead"), None)
    if ok or "cannot spawn" not in reason:
        errors.append("guard failed to block sibling-stage spawn")
    # Leaf cannot delegate.
    ok, _, _ = guard.evaluate_agent_call(payload("micro-reader", "research-worker"), None)
    if ok:
        errors.append("guard failed to block leaf delegation")
    # Unnamed child is blocked.
    ok, _, _ = guard.evaluate_agent_call(payload("orchestrator", None), None)
    if ok:
        errors.append("guard failed to block unnamed Agent call")
    # Arithmetic malformed.
    bad = payload("orchestrator", "micro-reader", before=12)
    bad["tool_input"]["prompt"] = bad["tool_input"]["prompt"].replace("budget_after: 11", "budget_after: 12")
    ok, _, _ = guard.evaluate_agent_call(bad, None)
    if ok:
        errors.append("guard failed to reject malformed budget arithmetic")
    # Task class cannot change within one prompt.
    ok, _, state = guard.evaluate_agent_call(payload("orchestrator", "micro-reader", "SMALL", 6), None)
    if not ok:
        errors.append("guard rejected first SMALL call in class-drift test")
    else:
        ok, _, _ = guard.evaluate_agent_call(payload("orchestrator", "micro-reader", "COMPLEX", 24), state)
        if ok:
            errors.append("guard failed to reject task-class change within one prompt")
    # Exhausted budget is a hard block. Build a small-budget ledger without relying on budget_before equality.
    small_state = None
    for i in range(6):
        ok, _, small_state = guard.evaluate_agent_call(payload("orchestrator", "micro-reader", "SMALL", max(1, 6-i)), small_state)
        if not ok:
            errors.append(f"guard rejected valid SMALL call {i+1} of 6")
            break
    ok, _, _ = guard.evaluate_agent_call(payload("orchestrator", "micro-reader", "SMALL", 1), small_state)
    if ok:
        errors.append("guard failed to block the 7th SMALL Agent call")
    # prompt_id is part of state partitioning.
    p1 = payload("orchestrator", "micro-reader")
    p2 = payload("orchestrator", "micro-reader")
    p2["prompt_id"] = "prompt-runtime-test-2"
    if guard._prompt_key(p1) == guard._prompt_key(p2):
        errors.append("guard prompt state key does not change across prompt_id")


def check_budget_contract() -> None:
    budgets = {"TRIVIAL": 4, "SMALL": 6, "MODERATE": 12, "COMPLEX": 24}
    rule = (RULES / "18-task-sizing-and-delegation.md").read_text(encoding="utf-8")
    for task_class, total in budgets.items():
        if not re.search(rf"\| {task_class} \|.*\| {total} \|", rule):
            errors.append(f"budget table missing {task_class}={total}")
    for phrase in ["deterministic runtime guard", "prompt_id", "parallel Agent calls", "budget_after"]:
        if phrase not in rule:
            errors.append(f"budget rule missing {phrase}")

def check_mcp_and_docs() -> None:
    context_agents = {"research-lead", "planning-lead", "implementation-lead", "audit-lead"}
    for name in context_agents:
        servers = json.dumps(agent(name).get("mcpServers", []), sort_keys=True).lower()
        if "context7" not in servers:
            errors.append(f"{name} missing Context7")
        if "@playwright/mcp@" in servers:
            errors.append(f"{name} must not receive Playwright MCP")
    for name in ["testing-lead", "test-runner"]:
        servers = json.dumps(agent(name).get("mcpServers", []), sort_keys=True)
        if "playwright" not in servers or "@playwright/mcp@1" not in servers:
            errors.append(f"{name} missing approved Playwright MCP")
        for flag in ["--headless", "--isolated", "--idle-timeout=300000"]:
            if flag not in servers:
                errors.append(f"{name} missing Playwright flag {flag}")

def check_docs() -> None:
    docs = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "docs").glob("*.md"))
    if "1.4.2" not in docs:
        errors.append("docs do not mention 1.4.2")
    if "deterministic" not in docs.lower() or "agent_guard.py" not in docs:
        errors.append("docs do not describe deterministic Agent guard")
    if "py -3" not in (ROOT / "docs" / "INSTALL.md").read_text(encoding="utf-8"):
        errors.append("INSTALL.md does not document the `py -3` hook launcher")
    if "existing `.claude`" not in docs:
        errors.append("install docs do not describe safe handling of an existing .claude tree")
    if "Context7 appears" not in (ROOT / "evals" / "README.md").read_text(encoding="utf-8"):
        errors.append("eval README has stale Context7 routing scenario")

def main() -> int:
    try:
        settings = json.loads((ROOT / "settings.json").read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"settings.json parse failed: {exc}")
        settings = {}
    checks = [
        ("declared graph", check_declared_graph),
        ("capability boundaries", check_capability_boundaries),
        ("watchdog wiring", lambda: check_watchdogs(settings)),
        ("deterministic runtime guard", check_runtime_guard),
        ("deterministic stop guard", check_stop_guard),
        ("budget contract", check_budget_contract),
        ("MCP scope", check_mcp_and_docs),
        ("documentation", check_docs),
    ]
    for label, fn in checks:
        before = len(errors)
        try:
            fn()
        except Exception as exc:
            errors.append(f"{label}: checker raised {type(exc).__name__}: {exc}")
        print(("PASS" if len(errors) == before else "FAIL") + f"  {label}")
    if errors:
        print("\nFAIL")
        for error in errors:
            print(" -", error)
        return 1
    print("\nPASS")
    print("Deterministic control-plane contract suite: all checks passed")
    print("Live Claude Code trace behavior remains environment-dependent")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
