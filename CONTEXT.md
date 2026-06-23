# A2A Communication Lab

This context describes a practice project for studying agent-to-agent and agent-to-tool communication. The project starts with protocol experiments, then uses practical multi-agent applications to validate the communication model.

## Language

**A2A**:
Agent-to-Agent communication: multiple agents exchange structured messages, capability declarations, requests, results, and state to collaborate on a task.
_Avoid_: multi-agent app, agent demo

**Participant**:
A communication entity that can appear as the sender or receiver in a message envelope. Agents and tools are participants, but only agents have task-level autonomy.
_Avoid_: node, actor

**Human**:
An external participant that may start tasks, provide feedback, approve high-risk actions, and receive results. A human may appear as a sender or receiver for traceability, but is not schedulable and does not declare capabilities.
_Avoid_: agent, operator

**Agent**:
An addressable collaborator that can receive messages, maintain task context, decide its next action, and request work from other agents or tools. A participant that cannot decide its next action is a tool or service, not an agent.
_Avoid_: bot, worker, service

**Tool**:
A capability unit invoked by an agent to perform a bounded operation from explicit input and return a structured result. A tool may have internal execution strategy, but it does not own task-level autonomy.
_Avoid_: agent, collaborator

**Search Tool**:
A tool that returns raw search results and basic retrieval metadata. The research agent interprets those results and owns the research conclusion.
_Avoid_: research agent, answer engine

**Message**:
A structured communication unit exchanged between agents, or between an agent and a tool. A message has a protocol envelope and content; natural language is one possible form of content, not the whole message.
_Avoid_: chat message, prompt

**Envelope**:
The protocol-level wrapper of a message, carrying routing, intent, correlation, sender, receiver, and ordering information.
_Avoid_: metadata

**Routing**:
The process of delivering a message to a target participant by explicit receiver or by matching requested capability. Explicit receiver routing takes precedence over capability routing.
_Avoid_: dispatch, selection

**Content**:
The meaning-bearing body of a message, expressed as natural language, structured data, or both.
_Avoid_: payload-only message

**Intent**:
The protocol purpose of a message. Intent uses a fixed core vocabulary for common interactions and may allow namespaced extensions for experiments.
_Avoid_: free-form action text, message type

**Task**:
A goal that a user or agent wants to complete.
_Avoid_: conversation, session

**Conversation**:
The message flow among participants around a task.
_Avoid_: task, chat

**Agent Context**:
An individual agent's local understanding and memory for a task.
_Avoid_: shared state, conversation state

**Conversation State**:
The observable shared progress of a conversation, such as completed steps and unresolved questions.
_Avoid_: agent memory, shared store

**Shared Store**:
An external place for logging and observing communication state. Agents must not use a shared store to bypass message-based collaboration.
_Avoid_: blackboard, global memory

**Trace**:
The inspectable record of all messages, tool calls, results, errors, refusals, and approvals within a task.
_Avoid_: log, transcript

**Outcome**:
The top-level result summary of a trace, including completion status, the final message reference, and a short summary.
_Avoid_: final report, message content

**Protocol Version**:
The version of the communication protocol used by a trace. A trace has one protocol version for all messages it contains.
_Avoid_: message version, schema version

**Timeline**:
A chronological view of a trace.
_Avoid_: chat history, event log

**Message Inspector**:
A view for inspecting an individual message's envelope and content.
_Avoid_: debug panel, raw JSON viewer

**Visual Replay**:
A UI-driven replay of a trace in message order for observation only.
_Avoid_: deterministic replay, rerun

**Correlation**:
The trace relationship that connects a response, tool result, or error back to the request or tool call it answers.
_Avoid_: session, conversation

**Error**:
A failure in handling a single message or call that can be traced through correlation.
_Avoid_: task failure, refusal

**Task Failure**:
The final inability to complete a task.
_Avoid_: error, refusal

**Refusal**:
A participant's explicit decision not to handle a request. A refusal is a normal protocol outcome, not necessarily a technical error.
_Avoid_: error, exception

**Permission**:
A rule that determines whether a participant may request or execute a class of action.
_Avoid_: approval, role

**Approval**:
A human's explicit authorization for a risky action.
_Avoid_: permission, confirmation

**Risky Action**:
An action that may create external side effects, spend money, expose data, or damage state.
_Avoid_: tool call, operation

**Research-to-Write Scenario**:
The first validation scenario: a planner decomposes a task, a research agent gathers information through a search tool, and a writer agent produces the final output.
_Avoid_: generic demo, chat workflow

**v0**:
The first successful version of the project: a schema-validated Research-to-Write trace generated by the Python CLI with a mock model and inspectable in the TypeScript trace UI.
_Avoid_: MVP, prototype

**Planner Agent**:
The agent that decomposes a task into delegated subgoals and decides which participant should handle the next step.
_Avoid_: manager, orchestrator

**Research Agent**:
The agent responsible for gathering and organizing external information. It does not own the final expression of the result.
_Avoid_: search tool, writer

**Writer Agent**:
The agent responsible for organizing available information into the final output. In the first validation scenario, it must request missing information through another agent rather than calling the search tool directly.
_Avoid_: researcher, formatter

**Agent-to-Tool Communication**:
Communication where an agent invokes a tool through the shared message envelope while using tool-specific content constraints.
_Avoid_: direct function call, agent conversation

**Capability**:
A declaration of what a participant can handle, including supported tasks, intents, input constraints, and output commitments. Capabilities may be declared statically and discovered at runtime.
_Avoid_: feature, skill
