import subprocess
import sys
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class V0EndToEndAcceptanceTest(unittest.TestCase):
    def test_python_generated_trace_passes_schema_and_cross_stack_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            trace_path = Path(tmpdir) / "research-to-write.trace.json"

            run_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "a2a_protocol",
                    "run",
                    "research-to-write",
                    "--task",
                    "Explain A2A communication.",
                    "--output",
                    str(trace_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr + run_result.stdout)

            validate_result = subprocess.run(
                [sys.executable, "-m", "a2a_protocol", "validate", str(trace_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(
                validate_result.returncode,
                0,
                validate_result.stderr + validate_result.stdout,
            )

            contract_result = subprocess.run(
                ["node", "scripts/assert_trace_contract.mjs", str(trace_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(
                contract_result.returncode,
                0,
                contract_result.stderr + contract_result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
