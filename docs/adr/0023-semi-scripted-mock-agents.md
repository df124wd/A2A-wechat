# Semi-scripted mock agents

The v0 mock model should drive semi-scripted behavior for the planner, research, and writer agents rather than emitting a complete trace from one global script. Each agent should have a clear fixed strategy so the generated trace remains predictable while still exercising participant boundaries, message flow, delegation, and tool invocation.
