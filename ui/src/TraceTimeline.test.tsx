import { render, screen, within } from "@testing-library/react";
import { TraceApp } from "./TraceApp";

test("renders the curated Trace as a Timeline", () => {
  render(<TraceApp />);

  expect(screen.getByRole("heading", { name: "Trace Loader" })).toBeInTheDocument();
  const timeline = screen.getByRole("region", { name: "Timeline" });
  expect(within(timeline).getByRole("heading", { name: "Timeline" })).toBeInTheDocument();
  expect(screen.getByText("completed")).toBeInTheDocument();
  expect(within(timeline).getByText("human.user")).toBeInTheDocument();
  expect(within(timeline).getByText("request")).toBeInTheDocument();
  expect(
    within(timeline).getByText(
      "Human asks Planner Agent to complete a Research-to-Write task."
    )
  ).toBeInTheDocument();
});

test("orders Timeline entries by message sequence", () => {
  render(<TraceApp />);

  const entries = within(screen.getByRole("region", { name: "Timeline" })).getAllByRole(
    "listitem"
  );

  expect(entries[0]).toHaveTextContent("human.user");
  expect(entries[0]).toHaveTextContent("request");
  expect(entries[1]).toHaveTextContent("msg_planner_discover_research");
  expect(entries[1]).toHaveTextContent("agent.planner");
  expect(entries[1]).toHaveTextContent("tool_call");
  expect(entries[2]).toHaveTextContent("msg_capability_research_result");
  expect(entries[2]).toHaveTextContent("tool.capability_registry");
  expect(entries[2]).toHaveTextContent("tool_result");
  expect(entries[3]).toHaveTextContent("msg_planner_delegate_research");
  expect(entries[3]).toHaveTextContent("agent.planner");
  expect(entries[3]).toHaveTextContent("delegate");
});

test("renders model service interaction in the curated Timeline", () => {
  render(<TraceApp />);

  const timeline = screen.getByRole("region", { name: "Timeline" });

  expect(within(timeline).getByText("msg_writer_model_call")).toBeInTheDocument();
  expect(within(timeline).getByText("msg_writer_model_result")).toBeInTheDocument();
  expect(within(timeline).getByText("tool.model")).toBeInTheDocument();
});

test("renders capability discovery in the curated Timeline", () => {
  render(<TraceApp />);

  const timeline = screen.getByRole("region", { name: "Timeline" });

  expect(within(timeline).getByText("msg_planner_discover_research")).toBeInTheDocument();
  expect(within(timeline).getByText("msg_capability_research_result")).toBeInTheDocument();
  expect(within(timeline).getByText("tool.capability_registry")).toBeInTheDocument();
});
