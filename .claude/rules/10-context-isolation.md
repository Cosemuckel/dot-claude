# Context isolation

Treat context as a constrained resource. Do not move raw files, logs, search transcripts, dependency trees, or
broad exploratory notes between agents.

For a narrow repository question, use the narrowest specialist that can answer it. The default is
`micro-reader` for one fact, one value, one file relationship, one short call path, or one tightly scoped
comparison.

A worker should read as much as necessary inside its own context, but return only the requested result and
minimum evidence.

A stage lead may coordinate multiple focused workers. If independent subtasks exist, parallelize them when
useful. Never create additional layers merely for ceremony.

The main session should receive compact handoff packets, not the evidence corpus behind them.
