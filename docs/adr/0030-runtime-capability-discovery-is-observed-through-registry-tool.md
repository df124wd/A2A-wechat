# Runtime capability discovery is observed through a registry tool

Research-to-Write should show runtime capability discovery before Planner Agent delegates research. In v0 this is represented as `tool_call` and `tool_result` messages between `agent.planner` and `tool.capability_registry`.

The registry tool is an observable protocol participant, not an autonomous agent. It returns matching participants for a requested capability, such as `research.web`, and the Planner remains responsible for choosing and delegating the next task step. This validates capability-based delegation without introducing a full scheduler or router yet.
