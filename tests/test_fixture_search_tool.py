import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from tests.support import mock_model_env


ROOT = Path(__file__).resolve().parents[1]


class FixtureSearchToolTest(unittest.TestCase):
    def test_research_to_write_trace_uses_fixture_search_tool(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "trace.json"

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
                env=mock_model_env(),
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            trace = json.loads(output_path.read_text(encoding="utf-8"))

        participant_ids = {participant["participant_id"] for participant in trace["participants"]}
        self.assertIn("tool.search", participant_ids)

        messages = trace["messages"]
        tool_call = next(
            message
            for message in messages
            if message["envelope"]["sender"] == "agent.researcher"
            and message["envelope"].get("receiver") == "tool.search"
            and message["envelope"]["intent"] == "tool_call"
        )
        self.assertEqual(tool_call["content"]["data"]["tool_name"], "search")

        tool_result = next(
            message
            for message in messages
            if message["envelope"]["sender"] == "tool.search"
            and message["envelope"].get("receiver") == "agent.researcher"
            and message["envelope"]["intent"] == "tool_result"
        )
        result_data = tool_result["content"]["data"]
        self.assertEqual(result_data["query"], "Explain A2A communication.")
        self.assertEqual(result_data["results"][0]["title"], "A2A Communication Basics")
        self.assertIn("url", result_data["results"][0])
        self.assertIn("snippet", result_data["results"][0])

    def test_search_tool_returns_raw_results_not_research_conclusions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "trace.json"

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
                env=mock_model_env(),
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            trace = json.loads(output_path.read_text(encoding="utf-8"))

        tool_result = next(
            message
            for message in trace["messages"]
            if message["envelope"]["sender"] == "tool.search"
            and message["envelope"]["intent"] == "tool_result"
        )
        research_response = next(
            message
            for message in trace["messages"]
            if message["envelope"]["sender"] == "agent.researcher"
            and message["envelope"]["intent"] == "response"
        )

        self.assertIn("results", tool_result["content"]["data"])
        self.assertNotIn("findings", tool_result["content"]["data"])
        self.assertIn("findings", research_response["content"]["data"])


if __name__ == "__main__":
    unittest.main()
