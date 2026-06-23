# A2A run CLI shape

The v0 experiment runner should expose a CLI shaped like `a2a run research-to-write --task "..."`. This separates the project command from the scenario name, leaves room for additional scenarios, and lets the runner default to an ignored local trace output while still allowing the caller to specify an output file.
