import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { TraceApp } from "./TraceApp";

test("loads an uploaded Trace JSON into the Timeline", async () => {
  render(<TraceApp />);

  const uploadedTrace = {
    protocol_version: "a2a-trace-v0",
    trace_id: "trace_uploaded",
    participants: [
      {
        participant_id: "human.user",
        kind: "human",
        display_name: "User",
        capabilities: []
      },
      {
        participant_id: "agent.planner",
        kind: "agent",
        display_name: "Planner Agent",
        capabilities: ["plan.research_to_write"]
      }
    ],
    messages: [
      {
        envelope: {
          message_id: "msg_uploaded_request",
          trace_id: "trace_uploaded",
          task_id: "task_uploaded",
          conversation_id: "conv_uploaded",
          sequence: 1,
          timestamp: "2026-06-23T00:00:00Z",
          sender: "human.user",
          receiver: "agent.planner",
          intent: "request",
          correlation_id: "corr_uploaded"
        },
        content: {
          summary: "Uploaded trace request summary.",
          data: {
            goal: "Inspect an uploaded trace."
          }
        }
      }
    ],
    outcome: {
      status: "completed",
      final_message_id: "msg_uploaded_request",
      summary: "Uploaded trace completed."
    }
  };
  const file = new File([JSON.stringify(uploadedTrace)], "uploaded-trace.json", {
    type: "application/json"
  });

  await userEvent.upload(screen.getByLabelText("Upload Trace JSON"), file);

  expect(await screen.findByText("uploaded-trace.json")).toBeInTheDocument();
  expect(await screen.findByText("Uploaded trace completed.")).toBeInTheDocument();

  const timeline = screen.getByRole("region", { name: "Timeline" });
  expect(within(timeline).getByText("msg_uploaded_request")).toBeInTheDocument();
  expect(within(timeline).getByText("Uploaded trace request summary.")).toBeInTheDocument();
});

test("visually replays the loaded Trace in message sequence order", async () => {
  render(<TraceApp />);

  const inspector = screen.getByRole("region", { name: "Message Inspector" });
  expect(within(inspector).getByText("msg_user_request")).toBeInTheDocument();

  await userEvent.click(screen.getByRole("button", { name: "Next message" }));

  expect(within(inspector).getByText("msg_planner_delegate_research")).toBeInTheDocument();

  await userEvent.click(screen.getByRole("button", { name: "Next message" }));

  expect(within(inspector).getByText("msg_research_tool_call")).toBeInTheDocument();
});
