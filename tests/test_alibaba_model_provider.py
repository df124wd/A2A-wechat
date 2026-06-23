import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from a2a_protocol.model import AlibabaModelClient


ROOT = Path(__file__).resolve().parents[1]


class AlibabaModelProviderCliTest(unittest.TestCase):
    def test_alibaba_provider_requires_dashscope_api_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "trace.json"
            env = os.environ.copy()
            env["A2A_MODEL_PROVIDER"] = "alibaba"
            env.pop("DASHSCOPE_API_KEY", None)

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "a2a_protocol",
                    "run",
                    "research-to-write",
                    "--task",
                    "Explain A2A communication.",
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )
            trace_was_written = output_path.exists()

        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertIn("DASHSCOPE_API_KEY", result.stderr)
        self.assertFalse(trace_was_written, "trace should not be written without provider credentials")

    def test_cli_model_provider_option_selects_alibaba(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "trace.json"
            env = os.environ.copy()
            env.pop("A2A_MODEL_PROVIDER", None)
            env.pop("DASHSCOPE_API_KEY", None)

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "a2a_protocol",
                    "run",
                    "research-to-write",
                    "--task",
                    "Explain A2A communication.",
                    "--model-provider",
                    "alibaba",
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )
            trace_was_written = output_path.exists()

        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertIn("DASHSCOPE_API_KEY", result.stderr)
        self.assertFalse(trace_was_written, "trace should not be written without provider credentials")


class AlibabaModelClientTest(unittest.TestCase):
    def test_alibaba_client_uses_openai_compatible_chat_completions(self) -> None:
        captured_requests = []

        def fake_transport(request):
            captured_requests.append(request)
            return {
                "choices": [
                    {
                        "message": {
                            "content": "A model-written answer.",
                        }
                    }
                ]
            }

        client = AlibabaModelClient(
            api_key="test-key",
            base_url="https://example.aliyuncs.com/compatible-mode/v1/",
            model="qwen-plus",
            transport=fake_transport,
        )

        answer = client.complete("Summarize the research findings.")

        self.assertEqual(answer, "A model-written answer.")
        self.assertEqual(len(captured_requests), 1)
        request = captured_requests[0]
        self.assertEqual(
            request.url,
            "https://example.aliyuncs.com/compatible-mode/v1/chat/completions",
        )
        self.assertEqual(request.headers["Authorization"], "Bearer test-key")
        self.assertEqual(request.headers["Content-Type"], "application/json")
        self.assertEqual(
            request.json,
            {
                "model": "qwen-plus",
                "messages": [
                    {
                        "role": "user",
                        "content": "Summarize the research findings.",
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
