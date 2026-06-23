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
      "User asks for a short research-backed explanation of A2A communication."
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
  expect(entries[1]).toHaveTextContent("agent.planner");
  expect(entries[1]).toHaveTextContent("delegate");
  expect(entries[2]).toHaveTextContent("agent.researcher");
  expect(entries[2]).toHaveTextContent("tool_call");
});
