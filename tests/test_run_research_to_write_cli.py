import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
import json


ROOT = Path(__file__).resolve().parents[1]


class RunResearchToWriteCliTest(unittest.TestCase):
    def run_scenario(self, task: str = "Explain A2A communication.") -> tuple[Path, subprocess.CompletedProcess[str]]:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "trace.json"

            run_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "a2a_protocol",
                    "run",
                    "research-to-write",
                    "--task",
                    task,
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            copied_output = ROOT / "traces" / "runs" / "test-output.json"
            copied_output.parent.mkdir(parents=True, exist_ok=True)
            if output_path.exists():
                copied_output.write_text(output_path.read_text(encoding="utf-8"), encoding="utf-8")

        return copied_output, run_result

    def test_cli_generates_valid_research_to_write_trace(self) -> None:
        output_path, run_result = self.run_scenario()

        self.assertEqual(run_result.returncode, 0, run_result.stderr + run_result.stdout)
        self.assertTrue(output_path.exists(), run_result.stderr + run_result.stdout)

        validate_result = subprocess.run(
            [sys.executable, "-m", "a2a_protocol", "validate", str(output_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(
            validate_result.returncode,
            0,
            validate_result.stderr + validate_result.stdout,
        )

    def test_generated_trace_exercises_research_to_write_agent_boundaries(self) -> None:
        output_path, run_result = self.run_scenario("Explain A2A communication.")

        self.assertEqual(run_result.returncode, 0, run_result.stderr + run_result.stdout)
        trace = json.loads(output_path.read_text(encoding="utf-8"))
        messages = trace["messages"]

        observed_steps = [
            (
                message["envelope"]["sender"],
                message["envelope"].get("receiver"),
                message["envelope"]["intent"],
            )
            for message in messages
        ]

        self.assertIn(("human.user", "agent.planner", "request"), observed_steps)
        self.assertIn(("agent.planner", "agent.researcher", "delegate"), observed_steps)
        self.assertIn(("agent.researcher", "agent.planner", "response"), observed_steps)
        self.assertIn(("agent.planner", "agent.writer", "delegate"), observed_steps)
        self.assertIn(("agent.writer", "human.user", "response"), observed_steps)

        writer_tool_calls = [
            message
            for message in messages
            if message["envelope"]["sender"] == "agent.writer"
            and message["envelope"]["intent"] == "tool_call"
        ]
        self.assertEqual(writer_tool_calls, [])

    def test_cli_defaults_output_to_ignored_trace_runs_directory(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "a2a_protocol",
                "run",
                "research-to-write",
                "--task",
                "Explain A2A communication.",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        output_line = result.stdout.strip()
        self.assertIn("traces", output_line)
        self.assertIn("runs", output_line)

        output_path = Path(output_line.removeprefix("wrote: ").strip())
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
