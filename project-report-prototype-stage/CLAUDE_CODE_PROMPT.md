# Claude Code task: prepare a demonstrable prototype for tomorrow

You are working inside the existing repository `AI_RESPONSE-ANALYSIS_AND_PROMPT_ENGINEERING-PLATFORM`. This is a software-engineering course prototype checkpoint tomorrow. The goal is a small, presentable, locally runnable vertical slice—not a large set of unintegrated features.

## Ground truth: inspect before changing
The current repository has these relevant sources:
- `KeshavBatla/backend_main.py`: FastAPI `/api/generate`, `/api/analyze`, `/api/health`; uses Anthropic Messages API and `ANTHROPIC_API_KEY`; the analysis route imports `local_analysis_stub`, which may not exist.
- `Diviyansh/frontend_App.jsx`: a basic React prompt/response/scores screen; hardcodes `http://localhost:8000/api`.
- `Gurshant/database_analysis.py`: a heuristic `analyze_response(prompt, response)` returning relevance, clarity, conciseness, completeness, structure, explanations, plus SQLAlchemy prompt/response/analysis models.
- `Project_Proposal/AI_Response_Analysis_Prompt_Engineering_Platform_Report_v2.tex`: proposal and scope.
- `README.md`: describes intended architecture but current paths don't fully match committed files.

Do not assume code runs. Inspect the actual repository and preserve existing work. Do not overwrite the proposal. Do not invent test results. Do not commit secrets or real API keys.

## Priority 1: make one complete working vertical slice
Deliver this workflow:
1. User opens a neat responsive web dashboard.
2. Enters a non-empty prompt.
3. Clicks Generate & Analyze.
4. Backend generates a response using Anthropic API if `ANTHROPIC_API_KEY` exists.
5. Backend runs the real shared heuristic analyzer and returns score fields plus explanations.
6. UI shows response and five labeled quality scores, explanation/feedback, loading status, and useful errors.
7. `/api/health` works.

## Integration implementation requirements
- Choose a simple reliable folder layout (`backend/`, `frontend/`, `database/`, `tests/`) but first inspect what exists. If moving code, leave no broken imports or duplicate stale implementations. Keep the team's current source files accessible or move them deliberately and update the README.
- Make the analyzer a real shared module. Remove the nonexistent `local_analysis_stub` dependency; import the module correctly or provide explicit deterministic fallback only if clearly labelled.
- Create a backend dependency file and frontend `package.json` that match actual imports. Keep dependencies minimal.
- Make API base URL configurable (`VITE_API_BASE_URL`), default to local FastAPI, and avoid CORS wildcard where easy; document allowed local origin.
- Validate prompt and response strings. Return useful HTTP errors without leaking provider keys or internal exception details. Keep network timeouts finite.
- Handle missing API key gracefully. For demo without a key, it is acceptable to provide a clearly-labelled **Demo Mode** with a deterministic sample generator controlled by an env var such as `DEMO_MODE=true`. The UI must display a banner that this is sample/demo output and must never imply it came from a live LLM. Keep live mode as the default when a key is configured.
- Do not require PostgreSQL just to start the prototype. Either make database persistence optional and configured through `DATABASE_URL`, or use SQLite as a local default if you implement persistence. If the database work cannot be completed safely, document it as planned and do not claim interactions persist.
- The score values should be clamped to 0–100, schema-stable, and explained as **heuristic indicators**, not factuality scores or guarantees.
- Improve the UI into a polished but restrained evaluation dashboard: coherent header, textarea, prompt counter if easy, Generate & Analyze button, clear output panel, five score cards/bars, strengths/weaknesses/explanations, responsive layout, empty/loading/success/error states. No fake charts or fake history. A prefilled example prompt button is useful.
- No authentication, admin panel, prompt optimizer, side-by-side comparison, or deployment work unless the basic workflow is stable first.

## Priority 2: tests and local runbook
- Add unit tests for analyzer outputs/ranges, empty inputs, long/unstructured text, and explanation output.
- Add API tests for health, invalid/empty generation prompt, analysis response shape, and missing API key/demo-mode behaviour. Stub outbound API calls in tests—tests must not incur real API charges.
- Run tests, lint/build checks where available. Fix failures rather than hiding them.
- Add a `README.md` with exact PowerShell commands for Windows: create venv, install deps, set env vars, run backend, install/run frontend in a second terminal, test URLs, and expected behaviour. Include both real API mode and explicitly-labelled demo mode. Mention never commit `.env`.
- Ensure `.env`, keys, virtual environments, node_modules, build output, caches, and local database files are ignored by Git.

## Priority 3: report and diagrams
I have prepared a draft under `prototype_report/` in my local workspace, but the report must match the code that actually results after your implementation. Read it and update status statements, architecture, module names, dependencies, commands, test cases, DFDs, and planned-vs-done sections accurately. The teacher's template repository is `https://github.com/tiet-ucs503/ucs503p-202627odd-template`; its Prototype Stage directory is `project-report-prototype-stage/`, currently only a TODO placeholder. The proposal template uses an `article` LaTeX document, 11pt A4, geometry/hyperref/enumitem/graphicx/xcolor/titling, with bold centered title. Keep the report reasonably close to that style.
- Preserve both `main.tex` and compiled `main.pdf` under a stage folder named `project-report-prototype-stage/` or `Project_Report_Prototype_Stage/`; be consistent and make the intended path obvious.
- Include DFD Level 0 context and DFD Level 1 process/data-store diagrams, plus architecture diagram.
- Do not report tests passed unless you ran them.
- Use team members as currently listed: Keshav Batla (backend/AI integration), Diviyansh (frontend), Gurshant (analysis/data layer), unless repository information shows otherwise.
- Leave roll numbers/emails as clearly marked editable placeholders if the actual values are not in the repo. Do not invent them.
- Compile the PDF with `latexmk`/`xelatex`/`pdflatex` if available; check page count/render for overflow, missing diagrams, and unreadably tiny graphics.

## Git hygiene
- Work on current checked-out branch and inspect `git status` first. Avoid overwriting uncommitted work. Do not push unless I specifically ask after reviewing. At end give a concise list of files changed, checks run and results, launch commands, any remaining known limitations, and a proposed commit message.

## Working order
1. Inspect `git status`, tree, and the four source artifacts.
2. Fix the app integration and make it run.
3. Run tests and frontend build.
4. Update README and report to match actual implementation.
5. Compile and visually inspect report PDF.
6. Summarize honestly. Stop expanding scope once the vertical slice works.
