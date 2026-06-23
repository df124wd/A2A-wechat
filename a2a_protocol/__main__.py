from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "trace.schema.json"


def validate_trace(trace_path: Path) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    trace = json.loads(trace_path.read_text(encoding="utf-8"))

    validator = Draft202012Validator(schema)
    errors = [error.message for error in validator.iter_errors(trace)]
    if errors:
        return errors

    message_ids = {message["envelope"]["message_id"] for message in trace["messages"]}
    final_message_id = trace["outcome"]["final_message_id"]
    if final_message_id not in message_ids:
        return [f"outcome.final_message_id does not reference an existing message: {final_message_id}"]

    participant_ids = {participant["participant_id"] for participant in trace["participants"]}
    for message in trace["messages"]:
        envelope = message["envelope"]
        sender = envelope["sender"]
        if sender not in participant_ids:
            return [f"message sender is not in participant snapshot: {sender}"]

        receiver = envelope.get("receiver")
        if receiver is not None and receiver not in participant_ids:
            return [f"message receiver is not in participant snapshot: {receiver}"]

    return []


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2 or args[0] != "validate":
        print("Usage: python -m a2a_protocol validate <trace.json>", file=sys.stderr)
        return 2

    trace_path = Path(args[1])
    errors = validate_trace(trace_path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"valid: {trace_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
