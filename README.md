# A2A Communication Lab

Protocol-first experiments for Agent-to-Agent and Agent-to-Tool communication.

## Run the Research-to-Write scenario

The default model provider is `mock`, so the scenario runs without credentials:

```powershell
python -m a2a_protocol run research-to-write --task "Explain A2A communication."
```

To use Alibaba Cloud Model Studio through its OpenAI-compatible API:

```powershell
$env:DASHSCOPE_API_KEY = "<your-api-key>"
$env:DASHSCOPE_BASE_URL = "<your-compatible-mode-base-url>"
$env:DASHSCOPE_MODEL = "qwen-plus"
python -m a2a_protocol run research-to-write --task "Explain A2A communication." --model-provider alibaba
```

`DASHSCOPE_MODEL` is optional and defaults to `qwen-plus`. Keep generated traces under `traces/runs/`; that directory is ignored by git.
