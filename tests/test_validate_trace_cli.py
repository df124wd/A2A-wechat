import subprocess
import sys
from pathlib import Path
import unittest
import json
import tempfile


ROOT = Path(__file__).resolve().parents[1]


class ValidateTraceCliTest(unittest.TestCase):
    def run_validator(self, trace_path: Path) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, "-m", "a2a_protocol", "validate", str(trace_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        return result

    def load_seed_trace(self) -> dict:
        return json.loads(
            (ROOT / "traces" / "examples" / "research-to-write.seed.json").read_text(
                encoding="utf-8"
            )
        )

    def validate_mutated_trace(self, trace: dict, filename: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            trace_path = Path(tmpdir) / filename
            trace_path.write_text(json.dumps(trace), encoding="utf-8")
            return self.run_validator(trace_path)

    def test_curated_research_to_write_trace_is_valid(self) -> None:
        trace_path = ROOT / "traces" / "examples" / "research-to-write.seed.json"

        result = self.run_validator(trace_path)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("valid", result.stdout.lower())

    def test_message_without_receiver_or_capability_is_invalid(self) -> None:
        trace = self.load_seed_trace()
        first_envelope = trace["messages"][0]["envelope"]
        first_envelope.pop("receiver")

        result = self.validate_mutated_trace(trace, "missing-routing.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not valid", result.stderr.lower())

    def test_message_can_route_by_capability_without_receiver(self) -> None:
        trace = self.load_seed_trace()
        first_envelope = trace["messages"][0]["envelope"]
        first_envelope.pop("receiver")
        first_envelope["capability"] = "plan.research_to_write"

        result = self.validate_mutated_trace(trace, "capability-routed.json")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_message_missing_required_envelope_field_is_invalid(self) -> None:
        trace = self.load_seed_trace()
        trace["messages"][0]["envelope"].pop("sequence")

        result = self.validate_mutated_trace(trace, "missing-envelope-sequence.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sequence", result.stderr.lower())

    def test_outcome_must_reference_existing_final_message(self) -> None:
        trace = self.load_seed_trace()
        trace["outcome"]["final_message_id"] = "msg_missing"

        result = self.validate_mutated_trace(trace, "missing-final-message.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("final_message_id", result.stderr)

    def test_message_participants_must_exist_in_trace_snapshot(self) -> None:
        trace = self.load_seed_trace()
        trace["messages"][0]["envelope"]["sender"] = "agent.unknown"

        result = self.validate_mutated_trace(trace, "unknown-participant.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("participant", result.stderr.lower())

    def test_message_content_requires_summary_and_data(self) -> None:
        trace = self.load_seed_trace()
        trace["messages"][0]["content"].pop("summary")

        result = self.validate_mutated_trace(trace, "missing-content-summary.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("summary", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
