import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { TraceApp } from "./TraceApp";

test("inspects the selected Message Envelope and Content", async () => {
  render(<TraceApp />);

  await userEvent.click(screen.getByRole("button", { name: /msg_research_tool_call/i }));

  const inspector = screen.getByRole("region", { name: "Message Inspector" });

  expect(within(inspector).getByRole("heading", { name: "Message Inspector" })).toBeInTheDocument();
  expect(within(inspector).getByText("msg_research_tool_call")).toBeInTheDocument();
  expect(within(inspector).getByText("agent.researcher")).toBeInTheDocument();
  expect(within(inspector).getByText("tool.search")).toBeInTheDocument();
  expect(within(inspector).getByText("tool_call")).toBeInTheDocument();
  expect(within(inspector).getByText("corr_search")).toBeInTheDocument();
  expect(within(inspector).getByText("msg_planner_delegate_research")).toBeInTheDocument();
  expect(
    within(inspector).getByText("Research Agent searches for A2A communication references.")
  ).toBeInTheDocument();
  expect(within(inspector).getByText(/agent to agent communication protocol/i)).toBeInTheDocument();
});
