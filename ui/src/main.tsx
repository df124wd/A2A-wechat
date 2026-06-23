import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { TraceApp } from "./TraceApp";
import "./styles.css";

const root = document.getElementById("root");

if (root) {
  createRoot(root).render(
    <StrictMode>
      <TraceApp />
    </StrictMode>
  );
}
