import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./frontend_App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
