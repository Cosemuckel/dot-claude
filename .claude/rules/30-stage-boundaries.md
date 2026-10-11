# Stage boundaries

The main orchestrator is an agent-only control plane. It may dispatch approved agents, receive their results,
route bounded rework through agents, and synthesize the final response. It has no file, search, shell, web, MCP,
editing, or testing tools and must not access repository contents directly. All substantive work occurs in agents.

Research lead: establish evidence and constraints; do not implement. Planning lead: choose one actionable
technical approach; do not implement. Implementation lead: implement the approved plan; do not declare final
success. Testing lead: independently verify the actual result; do not silently fix implementation defects.
Audit lead: investigate and report evidence-backed findings or root causes; never modify the audited target or
silently enter implementation.

Category leads may delegate to specialists when workload is large. Specialists are leaf workers and do not
create new delegation layers.

A narrow file-analysis task belongs to a narrow worker even when a stage lead could technically perform it
itself. Stage leads may read only what is necessary to manage their stage or execute the stage-specific work. The
main orchestrator must never perform any of those direct actions.
