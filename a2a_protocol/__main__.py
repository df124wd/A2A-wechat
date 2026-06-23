from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from a2a_protocol.model import ModelClient, ModelConfigError, MockModelClient, load_model_client


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "trace.schema.json"
SEARCH_FIXTURE_PATH = ROOT / "fixtures" / "search" / "research-to-write.json"
RUN_RESEARCH_TO_WRITE_USAGE = (
    "Usage: python -m a2a_protocol run research-to-write --task <text> "
    "[--output <trace.json>] [--model-provider mock|alibaba]"
)


def envelope(
    message_id: str,
    trace_id: str,
    task_id: str,
    conversation_id: str,
    sequence: int,
    sender: str,
    receiver: str,
    intent: str,
    correlation_id: str,
    reply_to: str | None = None,
) -> dict:
    data = {
        "message_id": message_id,
        "trace_id": trace_id,
        "task_id": task_id,
        "conversation_id": conversation_id,
        "sequence": sequence,
        "timestamp": f"2026-06-23T00:00:0{sequence - 1}Z",
        "sender": sender,
        "receiver": receiver,
        "intent": intent,
        "correlation_id": correlation_id,
    }
    if reply_to is not None:
        data["reply_to"] = reply_to
    return data


def writer_prompt(task: str, findings: list[str]) -> str:
    return (
        "Write a concise final answer for the user's task.\n"
        f"Task: {task}\n"
        "Research findings:\n"
        + "\n".join(f"- {finding}" for finding in findings)
    )


def research_to_write_trace(task: str, model_client: ModelClient | None = None) -> dict:
    trace_id = "trace_research_to_write_run"
    task_id = "task_research_to_write_run"
    conversation_id = "conv_research_to_write_run"
    search_result = json.loads(SEARCH_FIXTURE_PATH.read_text(encoding="utf-8"))
    model = model_client or MockModelClient()
    findings = [
        "A2A communication uses structured messages with routing and intent.",
        "Trace records make collaboration inspectable.",
    ]
    writer_answer = model.complete(writer_prompt(task, findings))

    return {
        "protocol_version": "a2a-trace-v0",
        "trace_id": trace_id,
        "participants": [
            {
                "participant_id": "human.user",
                "kind": "human",
                "display_name": "User",
                "capabilities": [],
            },
            {
                "participant_id": "agent.planner",
                "kind": "agent",
                "display_name": "Planner Agent",
                "capabilities": ["plan.research_to_write"],
            },
            {
                "participant_id": "agent.researcher",
                "kind": "agent",
                "display_name": "Research Agent",
                "capabilities": ["research.web"],
            },
            {
                "participant_id": "agent.writer",
                "kind": "agent",
                "display_name": "Writer Agent",
                "capabilities": ["write.summary"],
            },
            {
                "participant_id": "tool.search",
                "kind": "tool",
                "display_name": "Search Tool",
                "capabilities": ["search.web"],
            },
        ],
        "messages": [
            {
                "envelope": envelope(
                    "msg_user_request",
                    trace_id,
                    task_id,
                    conversation_id,
                    1,
                    "human.user",
                    "agent.planner",
                    "request",
                    "corr_user_task",
                ),
                "content": {
                    "summary": "Human asks Planner Agent to complete a Research-to-Write task.",
                    "data": {"goal": task},
                },
            },
            {
                "envelope": envelope(
                    "msg_planner_delegate_research",
                    trace_id,
                    task_id,
                    conversation_id,
                    2,
                    "agent.planner",
                    "agent.researcher",
                    "delegate",
                    "corr_research",
                    "msg_user_request",
                ),
                "content": {
                    "summary": "Planner Agent delegates research to Research Agent.",
                    "data": {"goal": f"Gather source material for: {task}"},
                },
            },
            {
                "envelope": envelope(
                    "msg_research_tool_call",
                    trace_id,
                    task_id,
                    conversation_id,
                    3,
                    "agent.researcher",
                    "tool.search",
                    "tool_call",
                    "corr_search",
                    "msg_planner_delegate_research",
                ),
                "content": {
                    "summary": "Research Agent calls Search Tool for source material.",
                    "data": {
                        "tool_name": "search",
                        "arguments": {"query": task},
                    },
                },
            },
            {
                "envelope": envelope(
                    "msg_search_result",
                    trace_id,
                    task_id,
                    conversation_id,
                    4,
                    "tool.search",
                    "agent.researcher",
                    "tool_result",
                    "corr_search",
                    "msg_research_tool_call",
                ),
                "content": {
                    "summary": "Search Tool returns raw fixture retrieval results.",
                    "data": search_result,
                },
            },
            {
                "envelope": envelope(
                    "msg_research_response",
                    trace_id,
                    task_id,
                    conversation_id,
                    5,
                    "agent.researcher",
                    "agent.planner",
                    "response",
                    "corr_research",
                    "msg_planner_delegate_research",
                ),
                "content": {
                    "summary": "Research Agent interprets raw search results for the Planner.",
                    "data": {
                        "findings": findings,
                        "source_message_id": "msg_search_result",
                    },
                },
            },
            {
                "envelope": envelope(
                    "msg_planner_delegate_writer",
                    trace_id,
                    task_id,
                    conversation_id,
                    6,
                    "agent.planner",
                    "agent.writer",
                    "delegate",
                    "corr_write",
                    "msg_research_response",
                ),
                "content": {
                    "summary": "Planner Agent delegates final writing to Writer Agent.",
                    "data": {"goal": "Write the final response from the research findings."},
                },
            },
            {
                "envelope": envelope(
                    "msg_writer_response",
                    trace_id,
                    task_id,
                    conversation_id,
                    7,
                    "agent.writer",
                    "human.user",
                    "response",
                    "corr_user_task",
                    "msg_user_request",
                ),
                "content": {
                    "summary": "Writer Agent returns the final response.",
                    "data": {"answer": writer_answer},
                },
            },
        ],
        "outcome": {
            "status": "completed",
            "final_message_id": "msg_writer_response",
            "summary": "The Research-to-Write Scenario completed with a Writer Agent response.",
        },
    }


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


def parse_research_to_write_options(args: list[str]) -> tuple[str, Path, str | None]:
    task: str | None = None
    output_path: Path | None = None
    model_provider: str | None = None

    index = 0
    while index < len(args):
        option = args[index]
        if option not in ("--task", "--output", "--model-provider"):
            raise ValueError(RUN_RESEARCH_TO_WRITE_USAGE)
        if index + 1 >= len(args):
            raise ValueError(RUN_RESEARCH_TO_WRITE_USAGE)

        value = args[index + 1]
        if option == "--task":
            task = value
        elif option == "--output":
            output_path = Path(value)
        elif option == "--model-provider":
            model_provider = value

        index += 2

    if task is None:
        raise ValueError(RUN_RESEARCH_TO_WRITE_USAGE)

    return (
        task,
        output_path or ROOT / "traces" / "runs" / "research-to-write.latest.json",
        model_provider,
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) == 2 and args[0] == "validate":
        trace_path = Path(args[1])
        errors = validate_trace(trace_path)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1

        print(f"valid: {trace_path}")
        return 0

    if args[:2] == ["run", "research-to-write"]:
        try:
            task, output_path, model_provider = parse_research_to_write_options(args[2:])
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2

        try:
            model_env = dict(os.environ)
            if model_provider is not None:
                model_env["A2A_MODEL_PROVIDER"] = model_provider
            model_client = load_model_client(model_env)
        except ModelConfigError as error:
            print(str(error), file=sys.stderr)
            return 1

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(research_to_write_trace(task, model_client), indent=2),
            encoding="utf-8",
        )
        print(f"wrote: {output_path}")
        return 0

    print(
        f"Usage: python -m a2a_protocol validate <trace.json> | {RUN_RESEARCH_TO_WRITE_USAGE}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
