#!/usr/bin/env python3
"""Static contract checker for the project-scoped Claude Code package.

The checker is intentionally additive: the kit owns and verifies its required artifacts,
but a host repository may keep additional .claude agents, skills, rules, playbooks, and MCP config.
"""
from pathlib import Path
import json
import re
import sys

try:
    import yaml
except ImportError:
    print("FAIL")
    print(" - missing dependency: PyYAML; install with `python -m pip install -r .claude/evals/requirements.txt`")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
AGENTS = ROOT / "agents"
SKILLS = ROOT / "skills"
RULES = ROOT / "rules"
PLAYBOOKS = ROOT / "playbooks"
HOOK = ROOT / "hooks" / "agent_guard.py"
STOP_HOOK = ROOT / "hooks" / "stop_guard.py"
errors: list[str] = []

EXPECTED_AGENTS = {
    "orchestrator": "claude-sonnet-5-5",
    "research-lead": "claude-sonnet-5-5",
    "planning-lead": "claude-sonnet-5-5",
    "implementation-lead": "claude-sonnet-5-5",
    "testing-lead": "claude-sonnet-5-5",
    "audit-lead": "claude-sonnet-5-5",
    "micro-reader": "claude-haiku-5-5",
    "research-worker": "claude-haiku-5-5",
    "plan-worker": "claude-haiku-5-5",
    "implementation-worker": "claude-sonnet-5-5",
    "test-runner": "claude-haiku-5-5",
    "audit-worker": "claude-haiku-5-5",
}
EXPECTED_SKILLS = {
    "cost-control",
    "context-engineering",
    "handoff-protocol",
    "implementation-protocol",
    "mcp-evaluation",
    "planning-protocol",
    "prompt-engineering",
    "research-protocol",
    "skill-authoring",
    "verification-protocol",
    "audit-protocol",
}
EXPECTED_PLAYBOOKS = {"feature-development.md", "bug-fix.md", "refactor-review.md", "audit-review.md", "README.md"}
PATH_SCOPED_RULES = {"140-testing.md", "170-ui-ux.md", "180-api.md", "190-data.md", "230-generated-code.md"}
TASK_BUDGETS = {"TRIVIAL": 4, "SMALL": 6, "MODERATE": 12, "COMPLEX": 24}
TASK_BUDGET_RULE = RULES / "18-task-sizing-and-delegation.md"

def fail(message: str) -> None:
    errors.append(message)

def load_frontmatter(path: Path, required: bool = True):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        if required:
            fail(f"{path.relative_to(PROJECT)}: missing frontmatter")
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path.relative_to(PROJECT)}: unterminated frontmatter")
        return {}, text
    try:
        data = yaml.safe_load(text[4:end]) or {}
    except Exception as exc:
        fail(f"{path.relative_to(PROJECT)}: invalid YAML: {exc}")
        return {}, text
    return data, text

# Required kit structure. Extra host-project files are permitted.
required = [ROOT / "CLAUDE.md", ROOT / "MANIFEST.txt", ROOT / "VERSION", ROOT / "settings.json",
            ROOT / "evals" / "requirements.txt", AGENTS, SKILLS, RULES, PLAYBOOKS, TASK_BUDGET_RULE,
            ROOT / "docs" / "UPGRADE-1.4.1.md", ROOT / "docs" / "UPGRADE-1.4.2.md", HOOK, STOP_HOOK]
for path in required:
    if not path.exists():
        fail(f"missing: {path.relative_to(PROJECT)}")

if HOOK.exists() and not HOOK.is_file():
    fail(".claude/hooks/agent_guard.py must be a file")
if HOOK.exists() and not (HOOK.stat().st_mode & 0o111):
    fail(".claude/hooks/agent_guard.py must be executable")
if STOP_HOOK.exists() and not STOP_HOOK.is_file():
    fail(".claude/hooks/stop_guard.py must be a file")
if STOP_HOOK.exists() and not (STOP_HOOK.stat().st_mode & 0o111):
    fail(".claude/hooks/stop_guard.py must be executable")


def hook_ref(hook: dict) -> str:
    """Command plus exec-form args, so checks work for both shell-string and exec-form hooks."""
    return hook.get("command", "") + " " + " ".join(str(a) for a in hook.get("args", []))

claude_text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8") if (ROOT / "CLAUDE.md").exists() else ""
claude_lines = claude_text.splitlines()
if len(claude_lines) >= 200:
    fail(f"CLAUDE.md is {len(claude_lines)} lines; must stay under 200")

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else ""
if version != "1.4.2":
    fail(f"expected package version 1.4.2, got {version!r}")

# Settings and hook shape.
try:
    settings = json.loads((ROOT / "settings.json").read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"settings.json is invalid JSON: {exc}")
    settings = {}

if settings.get("agent") != "orchestrator":
    fail("settings.json must select orchestrator as the default main-thread agent")
if settings.get("model") != "claude-sonnet-5-5":
    fail("settings.json must pin the main session to claude-sonnet-5-5")

env = settings.get("env", {})
if env.get("CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH") != "2":
    fail("spawn depth must be 2")
if env.get("CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS") != "8":
    fail("concurrent subagent limit must be 8")
if env.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") != "0":
    fail("agent teams must be explicitly disabled")
if "ENABLE_TOOL_SEARCH" in env:
    fail("ENABLE_TOOL_SEARCH must not be overridden; runtime defaults are authoritative")
if env.get("MAX_MCP_OUTPUT_TOKENS") != "12000":
    fail("MAX_MCP_OUTPUT_TOKENS must be 12000")

expected_denies = {"Agent(Explore)", "Agent(Plan)", "Agent(general-purpose)"}
actual_denies = set(settings.get("permissions", {}).get("deny", []))
if not expected_denies.issubset(actual_denies):
    fail("built-in generic agents are not fully denied")

hooks = settings.get("hooks", {})
for group_name in ("PreToolUse", "SubagentStop", "Stop", "SessionEnd"):
    if group_name not in hooks:
        fail(f"missing {group_name} hook group")

prompt_hook_count = 0
for group_name, entries in hooks.items():
    if not isinstance(entries, list):
        fail(f"{group_name} hooks must be a list")
        continue
    for entry in entries:
        if not isinstance(entry, dict):
            fail(f"{group_name}: hook entry must be a mapping")
            continue
        if group_name not in ("Stop", "SessionEnd") and not entry.get("matcher"):
            fail(f"{group_name}: matcher is required")
        for hook in entry.get("hooks", []):
            if not isinstance(hook, dict) or hook.get("type") not in {"prompt", "command"}:
                fail(f"{group_name}: hook type must be prompt or command")
                continue
            if hook.get("type") == "prompt":
                prompt_hook_count += 1
                if hook.get("model") != "claude-haiku-5-5":
                    fail(f"{group_name}: semantic watchdog model must be claude-haiku-5-5")
                if not isinstance(hook.get("timeout"), int) or not 1 <= hook["timeout"] <= 15:
                    fail(f"{group_name}: watchdog timeout must be an integer from 1 to 15 seconds")
                if "$ARGUMENTS" not in hook.get("prompt", ""):
                    fail(f"{group_name}: watchdog prompt must inspect $ARGUMENTS")
            if hook.get("type") == "command" and not hook.get("command"):
                fail(f"{group_name}: command hook must declare command")

agent_entry = next((e for e in hooks.get("PreToolUse", []) if e.get("matcher") == "Agent"), None)
if not agent_entry:
    fail("PreToolUse Agent hook is missing")
else:
    agent_hooks = agent_entry.get("hooks", [])
    if not any(h.get("type") == "command" and "agent_guard.py" in hook_ref(h) for h in agent_hooks):
        fail("PreToolUse Agent must include the deterministic agent_guard.py command hook")
    agent_guard_hooks = [h for h in agent_hooks if h.get("type") == "command" and "agent_guard.py" in hook_ref(h)]
    if agent_guard_hooks and not all(h.get("onFailure") == "block" for h in agent_guard_hooks):
        fail("PreToolUse Agent guard command hook must keep onFailure=block")
    semantic = [h for h in agent_hooks if h.get("type") == "prompt"]
    if len(semantic) != 1:
        fail("PreToolUse Agent must retain exactly one semantic prompt watchdog")
    elif semantic[0].get("continueOnBlock") is not True:
        fail("PreToolUse Agent semantic watchdog must use continueOnBlock=true")

bash_entry = next((e for e in hooks.get("PreToolUse", []) if e.get("matcher") == "Bash"), None)
if not bash_entry:
    fail("PreToolUse Bash semantic watchdog is missing")
else:
    bash_prompts = [h for h in bash_entry.get("hooks", []) if h.get("type") == "prompt"]
    if len(bash_prompts) != 1:
        fail("PreToolUse Bash must retain exactly one semantic prompt watchdog")
    elif bash_prompts[0].get("continueOnBlock") is not True:
        fail("PreToolUse Bash semantic watchdog must use continueOnBlock=true")

session_end = hooks.get("SessionEnd", [])
if not any(any(h.get("type") == "command" and "agent_guard.py" in hook_ref(h) for h in e.get("hooks", [])) for e in session_end):
    fail("SessionEnd must invoke agent_guard.py to clean per-session state")

stop_hooks = [h for e in hooks.get("Stop", []) if isinstance(e, dict) for h in e.get("hooks", []) if isinstance(h, dict)]
if not any(h.get("type") == "command" and "stop_guard.py" in hook_ref(h) for h in stop_hooks):
    fail("Stop must include the deterministic stop_guard.py command hook")
if any(h.get("type") == "prompt" for h in stop_hooks):
    fail("Stop must not use a prompt hook; the Stop review is deterministic")

# Windows launcher: every command hook runs through `py -3` (exec form or inline).
for group_name, entries in hooks.items():
    for entry in entries if isinstance(entries, list) else []:
        for hook in entry.get("hooks", []) if isinstance(entry, dict) else []:
            if not isinstance(hook, dict) or hook.get("type") != "command":
                continue
            args = hook.get("args", [])
            exec_form = hook.get("command") == "py" and isinstance(args, list) and args[:1] == ["-3"]
            inline_form = str(hook.get("command", "")).startswith("py -3")
            if not (exec_form or inline_form):
                fail(f"{group_name}: command hook must use the `py -3` launcher")

if prompt_hook_count != 3:
    fail(f"expected 3 semantic watchdog prompt hooks, found {prompt_hook_count}")

# Agent integrity. Required inventory is a subset; extra project agents are allowed.
agent_defs: dict[str, dict] = {}
for path in sorted(AGENTS.glob("*.md")):
    data, _ = load_frontmatter(path)
    if not isinstance(data, dict):
        fail(f"{path.name}: frontmatter is not a mapping")
        continue
    name = data.get("name")
    if not name:
        fail(f"{path.name}: missing name")
        continue
    if name in agent_defs:
        fail(f"duplicate agent name: {name}")
    agent_defs[name] = data
    if data.get("description") is None:
        fail(f"{name}: missing description")
    if name in EXPECTED_AGENTS and data.get("model") != EXPECTED_AGENTS[name]:
        fail(f"{name}: expected model {EXPECTED_AGENTS[name]!r}, got {data.get('model')!r}")
    if name in EXPECTED_AGENTS:
        if not data.get("effort"):
            fail(f"{name}: missing effort")
        if not isinstance(data.get("maxTurns"), int) or data["maxTurns"] <= 0:
            fail(f"{name}: maxTurns must be a positive integer")

missing_agents = set(EXPECTED_AGENTS) - set(agent_defs)
if missing_agents:
    fail(f"missing required agents: {sorted(missing_agents)}")

def declared_tools(name: str) -> str:
    return str(agent_defs.get(name, {}).get("tools", ""))

def list_field(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    return [str(value).strip()]

def disallowed(name: str) -> set[str]:
    return set(list_field(agent_defs.get(name, {}).get("disallowedTools")))

orch = agent_defs.get("orchestrator", {})
if orch.get("tools") != "Agent(research-lead, planning-lead, implementation-lead, testing-lead, audit-lead, micro-reader)":
    fail("orchestrator must directly allow only stage leads plus micro-reader")
if declared_tools("orchestrator") != "Agent(research-lead, planning-lead, implementation-lead, testing-lead, audit-lead, micro-reader)":
    fail("orchestrator must expose only approved Agent dispatch")
if any(tool in declared_tools("orchestrator") for tool in ["Read", "Grep", "Glob", "Edit", "Write", "Bash", "WebSearch", "WebFetch", "ToolSearch"]):
    fail("orchestrator must not have repository, shell, web, MCP, or tool-discovery tools")
allowed_models = {"claude-sonnet-5-5", "claude-haiku-5-5"}
for name, data in agent_defs.items():
    if data.get("model") not in allowed_models:
        fail(f"{name}: model {data.get('model')!r} is outside the two-model allowlist")
orch_text = (AGENTS / "orchestrator.md").read_text(encoding="utf-8")
for phrase in ["sole permitted tool", "repository files or inspect project contents", "must be executed by an authorized agent"]:
    if phrase.lower() not in orch_text.lower():
        fail(f"orchestrator instructions missing hard-boundary phrase: {phrase}")

micro = agent_defs.get("micro-reader", {})
if micro.get("tools") != "Read, Grep, Glob":
    fail("micro-reader must be Read/Grep/Glob only")
if "Agent" not in disallowed("micro-reader"):
    fail("micro-reader must explicitly disallow Agent")

for name in ["research-worker", "plan-worker", "implementation-worker", "test-runner", "audit-worker"]:
    if "Agent" not in disallowed(name):
        fail(f"{name} must be a leaf and disallow Agent")

expected_tools = {
    "research-lead": "Read, Grep, Glob, WebSearch, WebFetch, Agent(research-worker, micro-reader), ToolSearch",
    "planning-lead": "Read, Grep, Glob, Agent(plan-worker, micro-reader), ToolSearch",
    "implementation-lead": "Read, Grep, Glob, Edit, Write, Bash, Agent(implementation-worker, micro-reader), ToolSearch",
    "testing-lead": "Read, Grep, Glob, Bash, Agent(test-runner, micro-reader), ToolSearch",
    "audit-lead": "Read, Grep, Glob, WebSearch, WebFetch, Agent(audit-worker, micro-reader), ToolSearch",
}
for name, expected in expected_tools.items():
    if declared_tools(name) != expected:
        fail(f"{name}: capability set drifted; expected {expected!r}")

for name in ["testing-lead", "test-runner"]:
    if "Edit" not in disallowed(name) or "Write" not in disallowed(name):
        fail(f"{name} must disallow Edit and Write")
    if name == "test-runner" and "read-only" in agent_defs[name].get("description", "").lower():
        fail("test-runner must not claim to be read-only while retaining Bash")

for name in ["audit-lead", "testing-lead"]:
    if {"Edit", "Write"} & {x.strip() for x in declared_tools(name).split(",") if x.strip()}:
        fail(f"{name} must not expose Edit/Write")

# Explicit skill preloads for kit agents. Extras are allowed but required preloads must remain present.
known_skills = {d.name for d in SKILLS.iterdir() if d.is_dir()}
for name, data in agent_defs.items():
    for skill in data.get("skills", []) or []:
        if skill not in known_skills:
            fail(f"{name}: preloaded skill {skill!r} does not exist")

skill_names = set()
for d in sorted(SKILLS.iterdir()):
    if not d.is_dir():
        continue
    p = d / "SKILL.md"
    if not p.exists():
        fail(f"skill missing SKILL.md: {d.name}")
        continue
    skill_names.add(d.name)
    data, _ = load_frontmatter(p)
    if not isinstance(data, dict):
        fail(f"skill {d.name}: frontmatter invalid")
        continue
    if data.get("name") != d.name:
        fail(f"skill {d.name}: frontmatter name must match directory")
    if not data.get("description"):
        fail(f"skill {d.name}: missing description")
for missing in EXPECTED_SKILLS - skill_names:
    fail(f"missing required skill: {missing}")

for skill_name in ["handoff-protocol", "implementation-protocol", "planning-protocol", "research-protocol", "verification-protocol", "audit-protocol"]:
    data, _ = load_frontmatter(SKILLS / skill_name / "SKILL.md")
    if data.get("user-invocable") is not False:
        fail(f"internal protocol skill {skill_name}: user-invocable must be false")
for skill_name in ["cost-control", "mcp-evaluation", "skill-authoring", "context-engineering"]:
    data, _ = load_frontmatter(SKILLS / skill_name / "SKILL.md")
    if data.get("disable-model-invocation") is not True:
        fail(f"meta skill {skill_name}: disable-model-invocation must be true")
context_skill, _ = load_frontmatter(SKILLS / "context-engineering" / "SKILL.md")
if context_skill.get("user-invocable") is not True:
    fail("context-engineering must be user-invocable")

expected_preloads = {
    "micro-reader": {"handoff-protocol"},
    "research-lead": {"research-protocol", "handoff-protocol"},
    "planning-lead": {"planning-protocol", "handoff-protocol"},
    "implementation-lead": {"implementation-protocol", "handoff-protocol"},
    "implementation-worker": {"implementation-protocol"},
    "testing-lead": {"verification-protocol", "handoff-protocol"},
    "test-runner": {"verification-protocol"},
    "audit-lead": {"audit-protocol", "handoff-protocol"},
    "audit-worker": {"audit-protocol"},
}
for name, expected in expected_preloads.items():
    actual = set(agent_defs.get(name, {}).get("skills", []) or [])
    if not expected.issubset(actual):
        fail(f"{name}: missing required preloaded skills {sorted(expected - actual)}")

# MCP routing is agent-scoped; an existing host .mcp.json is permitted.
for name in ["research-lead", "planning-lead", "implementation-lead", "audit-lead"]:
    data = agent_defs[name]
    servers = data.get("mcpServers", []) or []
    names = [key for entry in servers if isinstance(entry, dict) for key in entry.keys()]
    if "context7" not in names:
        fail(f"{name}: missing inline Context7")
    if "ToolSearch" not in declared_tools(name):
        fail(f"{name}: missing ToolSearch for deferred MCP discovery")
    if "latest" in json.dumps(servers).lower():
        fail(f"{name}: MCP dependency must not use latest")

for name in ["testing-lead", "test-runner"]:
    data = agent_defs[name]
    servers = data.get("mcpServers", []) or []
    names = [key for entry in servers if isinstance(entry, dict) for key in entry.keys()]
    if "playwright" not in names:
        fail(f"{name}: missing inline Playwright")
    if "ToolSearch" not in declared_tools(name):
        fail(f"{name}: missing ToolSearch for deferred MCP discovery")
    serialized = json.dumps(servers)
    if "@playwright/mcp@latest" in serialized or "@playwright/mcp@1" not in serialized:
        fail(f"{name}: Playwright MCP must remain on approved @1 major line without @latest")
    command = serialized
    for flag in ["--headless", "--isolated", "--idle-timeout=300000"]:
        if flag not in command:
            fail(f"{name}: Playwright MCP must include {flag}")

# Required path-scoped rules are validated; host-project extras are allowed.
for name in PATH_SCOPED_RULES:
    path = RULES / name
    data, _ = load_frontmatter(path, required=True)
    if not isinstance(data.get("paths"), list) or not data["paths"]:
        fail(f"{name}: paths frontmatter must be a non-empty list")
    if set(data) - {"paths"}:
        fail(f"{name}: only paths frontmatter is allowed")

# Playbooks: required subset only.
actual_playbooks = {p.name for p in PLAYBOOKS.iterdir() if p.is_file()}
missing_playbooks = EXPECTED_PLAYBOOKS - actual_playbooks
for missing in sorted(missing_playbooks):
    fail(f"missing required playbook: {missing}")
playbook_rule = (RULES / "45-playbooks.md").read_text(encoding="utf-8")
for expected in ["feature-development", "bug-fix", "refactor-review"]:
    if expected not in playbook_rule:
        fail(f"playbook routing rule missing {expected}")
if "responsible stage lead" not in playbook_rule.lower() or "read the" not in playbook_rule.lower():
    fail("playbook routing rule must require the responsible stage lead to read the selected playbook")

# Task sizing / delegation contract.
task_rule_text = TASK_BUDGET_RULE.read_text(encoding="utf-8")
for task_class, budget in TASK_BUDGETS.items():
    if task_class not in task_rule_text or not re.search(rf"\| {task_class} \|.*\| {budget} \|", task_rule_text):
        fail(f"task budget rule missing {task_class}={budget}")
for required_phrase in [
    "ORCHESTRATION CONTROL", "budget_before", "budget_after", "Research is opt-in, not a ritual",
    "prompt_id", "deterministic runtime guard", "parallel Agent calls",
]:
    if required_phrase not in task_rule_text:
        fail(f"task budget rule missing required phrase: {required_phrase}")

orch_text = (AGENTS / "orchestrator.md").read_text(encoding="utf-8")
for phrase in ["TRIVIAL", "SMALL", "MODERATE", "COMPLEX", "budget_before", "budget_after", "Research is opt-in, not a ritual", "budget", "AUDIT", "DIAGNOSE"]:
    if phrase not in orch_text:
        fail(f"orchestrator missing proportionality contract phrase: {phrase}")
for name in ["research-lead", "planning-lead", "implementation-lead", "testing-lead", "audit-lead"]:
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    for phrase in ["budget_before", "budget_after", "deterministic runtime guard", "caller routes a named playbook"]:
        if phrase not in text:
            fail(f"{name}: missing propagation/playbook phrase: {phrase}")

agent_prompt = next((h for h in agent_entry.get("hooks", []) if h.get("type") == "prompt"), {}).get("prompt", "") if agent_entry else ""
for phrase in ["TRIVIAL", "SMALL", "MODERATE", "COMPLEX", "parallel calls", "purpose"]:
    if phrase.lower() not in agent_prompt.lower():
        fail(f"Agent semantic watchdog missing proportionality concept: {phrase}")

# Audit/testing and untrusted-input contracts.
audit_rule = (RULES / "26-investigation-and-audit.md").read_text(encoding="utf-8")
for phrase in ["AUDIT", "DIAGNOSE", "false-positive", "severity", "confidence", "coverage gaps", "modifying the target"]:
    if phrase.lower() not in audit_rule.lower():
        fail(f"audit rule missing required concept: {phrase}")
combined = "\n".join((ROOT / "rules" / n).read_text(encoding="utf-8") for n in ["100-reliability-security.md", "155-mcp-output.md"]) + "\n" + claude_text
for phrase in ["untrusted", "mcp responses", "cannot override", "task contracts"]:
    if phrase.lower() not in combined.lower():
        fail(f"untrusted-input boundary missing concept: {phrase}")

# Documentation consistency.
targets = list(ROOT.glob("docs/*.md")) + [ROOT / "MANIFEST.txt", ROOT / "CLAUDE.md", ROOT / "watchdog" / "README.md", ROOT / "playbooks" / "README.md", ROOT / "evals" / "README.md"]
all_docs = "\n".join(p.read_text(encoding="utf-8") for p in targets if p.exists())
for stale in [
    "Exact alias-to-model mapping remains provider/runtime-owned",
    "model/effort policy is alias-based",
    "Sonnet alias: orchestrator",
    "configured aliases support explicit",
    "Context7 only appears in research/planning/implementation stages",
    "Claude Sonnet 5.5 and Claude Haiku 5.5 respectively",
    "@playwright/mcp@latest",
    "current Serena setup command",
    "git+https://github.com/oraios/serena",
]:
    if stale in all_docs:
        fail(f"stale documentation phrase remains: {stale}")

if "1.4.2" not in (ROOT / "MANIFEST.txt").read_text(encoding="utf-8"):
    fail("MANIFEST.txt does not document 1.4.2")
if "UPGRADE-1.4.2.md" not in (ROOT / "MANIFEST.txt").read_text(encoding="utf-8"):
    fail("MANIFEST.txt does not reference UPGRADE-1.4.2.md")

# No bundled plugins and no Python caches in release tree.
if list(ROOT.rglob("plugin.json")):
    fail("plugins are not part of this package")
offenders = [p.relative_to(PROJECT).as_posix() for p in ROOT.rglob("*") if p.is_file() and (p.suffix == ".pyc" or "__pycache__" in p.parts)]
if offenders:
    fail("release contains Python cache artifacts: " + ", ".join(sorted(offenders)))

if errors:
    print("FAIL")
    for error in errors:
        print(" -", error)
    raise SystemExit(1)

print("PASS")
print(f"Package version: {version}")
print(f"CLAUDE.md lines: {len(claude_lines)}")
print(f"Required agents present: {len(EXPECTED_AGENTS)}; host extras permitted")
print(f"Required skills present: {len(EXPECTED_SKILLS)}; host extras permitted")
print(f"Rules: {len(list(RULES.glob('*.md')))} total; required path-scoped rules validated")
print(f"Required playbooks present: {len(EXPECTED_PLAYBOOKS)-1}; host extras permitted")
print("Watchdogs: deterministic Agent guard + deterministic Stop guard + 3 semantic prompt hooks + SessionEnd cleanup")
print("MCP: inline-scoped Context7 + headless/isolated @playwright/mcp@1; host .mcp.json permitted")
print("Runtime: hard Agent graph/budget guard is tested separately by runtime_contracts.py")
