import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./App";
import { useAuthStore } from "./shared/auth/store";
import "./styles/main.css";

useAuthStore.getState().restore();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
