import { readFileSync } from "node:fs";

const tracePath = process.argv[2];

if (!tracePath) {
  console.error("Usage: node scripts/assert_trace_contract.mjs <trace.json>");
  process.exit(2);
}

const trace = JSON.parse(readFileSync(tracePath, "utf8"));

const messages = [...trace.messages].sort(
  (a, b) => a.envelope.sequence - b.envelope.sequence
);
const participants = new Set(
  trace.participants.map((participant) => participant.participant_id)
);

function assert(condition, message) {
  if (!condition) {
    console.error(message);
    process.exit(1);
  }
}

assert(trace.protocol_version === "a2a-trace-v0", "Trace must use v0 protocol");
assert(trace.outcome.status === "completed", "Trace outcome must be completed");
assert(
  messages.some(
    (message) =>
      message.envelope.sender === "human.user" &&
      message.envelope.receiver === "agent.planner" &&
      message.envelope.intent === "request"
  ),
  "Trace must include Human request to Planner Agent"
);
assert(
  messages.some(
    (message) =>
      message.envelope.sender === "agent.planner" &&
      message.envelope.receiver === "agent.researcher" &&
      message.envelope.intent === "delegate"
  ),
  "Trace must include Planner delegation to Research Agent"
);
assert(
  messages.some(
    (message) =>
      message.envelope.sender === "agent.researcher" &&
      message.envelope.receiver === "tool.search" &&
      message.envelope.intent === "tool_call"
  ),
  "Trace must include Research Agent tool_call"
);
assert(
  messages.some(
    (message) =>
      message.envelope.sender === "tool.search" &&
      message.envelope.receiver === "agent.researcher" &&
      message.envelope.intent === "tool_result"
  ),
  "Trace must include Search Tool tool_result"
);
assert(
  messages.some(
    (message) =>
      message.envelope.sender === "agent.writer" &&
      message.envelope.receiver === "human.user" &&
      message.envelope.intent === "response"
  ),
  "Trace must include Writer Agent response to Human"
);

for (const message of messages) {
  assert(participants.has(message.envelope.sender), "Message sender must be known");
  if (message.envelope.receiver) {
    assert(participants.has(message.envelope.receiver), "Message receiver must be known");
  }
  assert(message.content.summary, "Message must have a content summary");
  assert(message.content.data, "Message must have structured content data");
}

console.log(`contract ok: ${tracePath}`);
