import { render, screen } from "@testing-library/react";
import { TraceApp } from "./TraceApp";

test("renders the curated Trace as a Timeline", () => {
  render(<TraceApp />);

  expect(screen.getByRole("heading", { name: "Trace Loader" })).toBeInTheDocument();
  expect(screen.getByRole("heading", { name: "Timeline" })).toBeInTheDocument();
  expect(screen.getByText("completed")).toBeInTheDocument();
  expect(screen.getByText("human.user")).toBeInTheDocument();
  expect(screen.getByText("request")).toBeInTheDocument();
  expect(
    screen.getByText("User asks for a short research-backed explanation of A2A communication.")
  ).toBeInTheDocument();
});

test("orders Timeline entries by message sequence", () => {
  render(<TraceApp />);

  const entries = screen.getAllByRole("listitem");

  expect(entries[0]).toHaveTextContent("human.user");
  expect(entries[0]).toHaveTextContent("request");
  expect(entries[1]).toHaveTextContent("agent.planner");
  expect(entries[1]).toHaveTextContent("delegate");
  expect(entries[2]).toHaveTextContent("agent.researcher");
  expect(entries[2]).toHaveTextContent("tool_call");
});
