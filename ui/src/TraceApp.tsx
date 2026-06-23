import { useState } from "react";
import trace from "../../traces/examples/research-to-write.seed.json";

type TraceMessage = {
  envelope: {
    message_id: string;
    sequence: number;
    sender: string;
    receiver?: string;
    capability?: string;
    intent: string;
    correlation_id?: string;
    reply_to?: string;
  };
  content: {
    summary: string;
    data: Record<string, unknown>;
  };
};

type Trace = {
  outcome: {
    status: string;
    final_message_id: string;
    summary: string;
  };
  messages: TraceMessage[];
};

const curatedTrace = trace as Trace;

export function TraceApp() {
  const messages = [...curatedTrace.messages].sort(
    (a, b) => a.envelope.sequence - b.envelope.sequence
  );
  const [selectedMessageId, setSelectedMessageId] = useState(
    messages[0]?.envelope.message_id
  );
  const selectedMessage =
    messages.find((message) => message.envelope.message_id === selectedMessageId) ??
    messages[0];

  return (
    <main>
      <section aria-labelledby="trace-loader-heading">
        <h1 id="trace-loader-heading">Trace Loader</h1>
        <p>Curated Research-to-Write Trace</p>
        <dl>
          <dt>Status</dt>
          <dd>{curatedTrace.outcome.status}</dd>
          <dt>Final Message</dt>
          <dd>{curatedTrace.outcome.final_message_id}</dd>
        </dl>
      </section>

      <section aria-labelledby="timeline-heading">
        <h2 id="timeline-heading">Timeline</h2>
        <ol>
          {messages.map((message) => (
            <li key={message.envelope.message_id}>
              <button
                type="button"
                onClick={() => setSelectedMessageId(message.envelope.message_id)}
              >
                <strong>{message.envelope.message_id}</strong>
                <span>{message.envelope.sender}</span>
                <span>{message.envelope.intent}</span>
                <p>{message.content.summary}</p>
              </button>
            </li>
          ))}
        </ol>
      </section>

      {selectedMessage ? <MessageInspector message={selectedMessage} /> : null}
    </main>
  );
}

function MessageInspector({ message }: { message: TraceMessage }) {
  const envelope = message.envelope;

  return (
    <section aria-labelledby="message-inspector-heading">
      <h2 id="message-inspector-heading">Message Inspector</h2>
      <dl>
        <dt>Message</dt>
        <dd>{envelope.message_id}</dd>
        <dt>Sender</dt>
        <dd>{envelope.sender}</dd>
        <dt>Receiver</dt>
        <dd>{envelope.receiver ?? envelope.capability}</dd>
        <dt>Intent</dt>
        <dd>{envelope.intent}</dd>
        <dt>Correlation</dt>
        <dd>{envelope.correlation_id}</dd>
        <dt>Reply To</dt>
        <dd>{envelope.reply_to ?? "None"}</dd>
        <dt>Summary</dt>
        <dd>{message.content.summary}</dd>
        <dt>Data</dt>
        <dd>
          <pre>{JSON.stringify(message.content.data, null, 2)}</pre>
        </dd>
      </dl>
    </section>
  );
}
