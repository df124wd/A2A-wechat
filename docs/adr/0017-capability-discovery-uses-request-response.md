# Capability discovery uses request and response

Runtime capability discovery should be represented with structured `request` and `response` message content rather than adding dedicated core intents. This keeps the v0 intent vocabulary stable while still allowing agents to query and answer what participants can handle.
