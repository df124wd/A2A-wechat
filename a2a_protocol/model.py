from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol
from urllib import request as urllib_request


class ModelConfigError(Exception):
    pass


class ModelClient(Protocol):
    def complete(self, prompt: str) -> str:
        pass


@dataclass(frozen=True)
class ModelRequest:
    url: str
    headers: Mapping[str, str]
    json: Mapping[str, Any]


JsonTransport = Callable[[ModelRequest], Mapping[str, Any]]


class UrllibJsonTransport:
    def __call__(self, model_request: ModelRequest) -> Mapping[str, Any]:
        body = json.dumps(model_request.json).encode("utf-8")
        http_request = urllib_request.Request(
            model_request.url,
            data=body,
            headers=dict(model_request.headers),
            method="POST",
        )
        with urllib_request.urlopen(http_request, timeout=60) as response:
            response_body = response.read().decode("utf-8")
        return json.loads(response_body)


@dataclass(frozen=True)
class MockModelClient:
    def complete(self, prompt: str) -> str:
        return (
            "A2A communication coordinates agents through structured "
            "messages that carry routing, intent, content, correlation, "
            "and trace information."
        )


@dataclass(frozen=True)
class AlibabaModelClient:
    api_key: str
    base_url: str
    model: str = "qwen-plus"
    transport: JsonTransport = UrllibJsonTransport()

    def complete(self, prompt: str) -> str:
        endpoint = f"{self.base_url.rstrip('/')}/chat/completions"
        response = self.transport(
            ModelRequest(
                url=endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        )
        return str(response["choices"][0]["message"]["content"])


def load_model_client(env: Mapping[str, str] | None = None) -> ModelClient:
    source = os.environ if env is None else env
    provider = source.get("A2A_MODEL_PROVIDER", "mock").strip().lower()

    if provider in ("", "mock"):
        return MockModelClient()

    if provider == "alibaba":
        api_key = source.get("DASHSCOPE_API_KEY", "").strip()
        if not api_key:
            raise ModelConfigError("A2A_MODEL_PROVIDER=alibaba requires DASHSCOPE_API_KEY.")

        base_url = source.get("DASHSCOPE_BASE_URL", "").strip()
        if not base_url:
            raise ModelConfigError("A2A_MODEL_PROVIDER=alibaba requires DASHSCOPE_BASE_URL.")

        model = source.get("DASHSCOPE_MODEL", "qwen-plus").strip() or "qwen-plus"
        return AlibabaModelClient(api_key=api_key, base_url=base_url, model=model)

    raise ModelConfigError(f"Unsupported A2A_MODEL_PROVIDER: {provider}")
