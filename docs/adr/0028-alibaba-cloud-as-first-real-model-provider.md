# Alibaba Cloud as first real model provider

The first real model provider should be Alibaba Cloud Model Studio through its OpenAI-compatible chat completions API. The project keeps the mock model as the default so protocol experiments remain deterministic, cheap, and credential-free.

Provider selection belongs to the runtime boundary, not the trace schema. `A2A_MODEL_PROVIDER=alibaba` or `--model-provider alibaba` selects the provider, while `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL`, and optional `DASHSCOPE_MODEL` configure the concrete call. The Research-to-Write message flow and trace contract should not contain provider-specific fields.
