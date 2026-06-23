# Envelope requires receiver or capability

The v0 envelope should allow `receiver` to be omitted for capability routing, but every routable message must provide either an explicit `receiver` or a requested `capability`. This supports both direct participant addressing and capability-based delegation without allowing messages that cannot be routed.
