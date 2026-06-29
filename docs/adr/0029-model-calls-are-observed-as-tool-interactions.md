# Model calls are observed as tool interactions

Writer Agent model calls should be visible in traces as `tool_call` and `tool_result` messages with `tool.model` as the receiver/sender. This keeps the v0 envelope and participant vocabulary stable while making model use inspectable in the Timeline and Message Inspector.

The model tool content is provider-neutral. It may include `provider`, `model`, `prompt_summary`, and `response_summary`, but must not include credentials or provider-specific request details. Provider configuration stays inside the runtime model boundary.
