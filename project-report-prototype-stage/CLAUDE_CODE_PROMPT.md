# Prototype-stage implementation notes

This document records the current implementation constraints for the response
analysis prototype. The repository's existing application and report are the
source of truth; extend them in place rather than rebuilding the project.

## Current application

- `KeshavBatla/backend_main.py` provides FastAPI routes:
  `/api/generate`, `/api/analyze`, and `/api/health`.
- The backend loads the repository-root `.env` using a path resolved relative
  to its source file. Live text generation uses Google's official
  `google-genai` Python SDK Interactions API and `GEMINI_API_KEY`;
  `GEMINI_MODEL` configures the model and defaults to `gemini-3.8-flash`.
- `DEMO_MODE=true` opts into a deterministic, clearly labelled sample only
  when the Gemini key is absent. With `DEMO_MODE=false` and no key, generation
  returns HTTP 503. The key must remain server-side and must never be logged,
  included in frontend configuration, or committed.
- Provider requests have a finite timeout and failures return generic
  client-facing errors that do not disclose provider details.
- The response contract remains `response`, `model`, and `mode`.
- `Gurshant/database_analysis.py` supplies five bounded heuristic scores and
  explanations. They are not factuality guarantees; no interaction history is
  persisted.
- `Diviyansh/frontend_App.jsx` uses a configurable API base URL, labels live
  output `Live · Gemini`, and retains the responsive prompt and analysis flow.

## Validation and reporting

- API tests must stub provider calls; never spend API quota in automated tests.
- Report actual test/build outcomes. Do not claim live Gemini connectivity
  unless a real provider request was intentionally made and succeeded.
- Keep architecture/DFD diagrams, README commands, report text, and code
  consistent. Preserve `Project_Proposal/` and do not include `.env` or keys.
