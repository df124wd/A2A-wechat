# Mixed ID strategy for trace readability

Runtime objects such as messages, tasks, conversations, traces, and correlations should use prefixed random IDs, while participants should use stable semantic IDs such as `agent.planner`, `agent.researcher`, `tool.search`, and `human.user`. This keeps trace records readable without sacrificing uniqueness for generated objects.
