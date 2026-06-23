import os


def mock_model_env() -> dict[str, str]:
    env = os.environ.copy()
    env["A2A_MODEL_PROVIDER"] = "mock"
    env.pop("DASHSCOPE_API_KEY", None)
    env.pop("DASHSCOPE_BASE_URL", None)
    env.pop("DASHSCOPE_MODEL", None)
    return env
