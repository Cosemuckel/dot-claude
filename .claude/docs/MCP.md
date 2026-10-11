# MCP configuration

This package intentionally uses MCP without adding Claude Code plugins.

## Enabled: Context7

Context7 is declared inline in `research-lead`, `planning-lead`, `implementation-lead`, and `audit-lead`:

`https://mcp.context7.com/mcp`

Use it only for current/version-specific library and framework documentation. The package does not add Context7 to
project `.mcp.json`, so it does not enter the main orchestrator's configured tool surface. A host project may already
have its own `.mcp.json`; review that file separately when strict MCP isolation is required.

## Enabled: Playwright

Playwright is declared inline in `testing-lead` and `test-runner`:

`npx -y @playwright/mcp@1 --headless --isolated --idle-timeout=300000`

Use it only when real browser/UI state must be observed or verified. The package runs Playwright headless and
isolated so browser profile state is not persisted to disk between sessions. Keep browser exploration and output inside
the testing context. Browser interactions can still mutate remote application state, so use test fixtures/environments
with appropriate isolation.

Playwright MCP requires Node.js 20+. The package intentionally follows the `@playwright/mcp@1` major line
rather than `latest`; upgrade the pin deliberately when adopting a new major version.

## Optional: Serena

Serena is intentionally not enabled by default.

If semantic code navigation/refactoring is needed and native repository navigation is insufficient, opt in at
project scope using a reviewed, explicitly pinned Serena release appropriate for the installed Claude
Code/Serena versions.

This package does not embed a floating Git dependency.

After installation, verify with separate commands: `/agents` and `/mcp`. `/mcp` may show a server only when its owning
subagent is active/connected.

Do not add Serena merely because it is available. Evaluate whether it provides a material advantage over
native search/LSP for the project.

## Tool-search policy

MCP-capable agents explicitly include `ToolSearch` so deferred MCP definitions can be discovered on demand.

The package does not override the runtime tool-search environment; provider/runtime defaults remain
authoritative. Inline agent MCP definitions additionally keep the servers out of the main orchestrator's tool
surface.
