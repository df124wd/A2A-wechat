# Visual replay only in first version

The first version should support visual replay of traces in message order, but should not promise deterministic replay of agent or tool execution. LLM calls and external tools are not inherently stable, and deterministic replay would require recording, caching, and isolation machinery that is outside the first protocol experiment.
