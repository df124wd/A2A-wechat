import trace from "../../traces/examples/research-to-write.seed.json";

type TraceMessage = {
  envelope: {
    message_id: string;
    sequence: number;
    sender: string;
    receiver?: string;
    intent: string;
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
              <span>{message.envelope.sender}</span>
              <span>{message.envelope.intent}</span>
              <p>{message.content.summary}</p>
            </li>
          ))}
        </ol>
      </section>
    </main>
  );
}
