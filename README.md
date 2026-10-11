# AI Response Analysis and Prompt Engineering Platform

A locally runnable React + FastAPI prototype for the core workflow:

**Prompt → response generation → heuristic analysis → five scores and explanations**

The browser sends prompts to the FastAPI service. If a `GEMINI_API_KEY` is
configured in the repository-root `.env` file, generation uses the official
Google Gemini SDK and Interactions API. The key remains on the backend. If no
key is available, an explicitly enabled deterministic demo mode can illustrate
the workflow. Demo output is labelled in the API, response text, and UI; it is
not an AI-generated answer.

All five analysis values (relevance, clarity, conciseness, completeness, and
structure) are transparent **heuristic indicators** on a 0–100 scale. They are
not factuality scores or guarantees of correctness. This checkpoint does not
save prompts or response history.

## Project layout

```text
Diviyansh/
  frontend_App.jsx       React dashboard
  main.jsx               React DOM mount entry point
  frontend.css           Responsive dashboard styles
  index.html              Vite entry page
  package.json            Frontend dependencies and scripts
  package-lock.json       Reproducible npm dependency lock
Gurshant/
  database_analysis.py   Shared heuristic analysis and legacy SQLAlchemy models
KeshavBatla/
  backend_main.py        FastAPI routes and Gemini integration
project-report-prototype-stage/
  main.tex                Prototype-stage report
  main.pdf                Compiled report
  assets/                 Architecture and DFD diagrams
tests/
  test_analysis.py       Heuristic unit tests
  test_api.py            FastAPI endpoint tests
requirements.txt          Python dependencies
README.md
```

The existing team directories are retained so current work remains accessible.
SQLAlchemy models are not wired into the application: there is no database
dependency, history, or persistence in this prototype.

## Requirements

- Windows 10/11 with Python 3.10 or newer and the Python launcher (`py`).
- Node.js 18 or newer with npm.
- Internet access to install packages; live generation additionally requires
  a Google Gemini API key and network access to Gemini.

## Windows PowerShell setup

Open PowerShell at the repository root:

```powershell
cd "C:\path\to\AI_RESPONSE-ANALYSIS_AND_PROMPT_ENGINEERING-PLATFORM"
```

Create the virtual environment and install the backend, test, and analysis
dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Install the frontend dependencies from the `Diviyansh` directory:

```powershell
cd .\Diviyansh
npm install
cd ..
```

### Configure the root `.env`

Create or edit `.env` in the repository root (the same directory as this
README). The backend resolves this file relative to
`KeshavBatla\backend_main.py`, so startup works from any current directory.
Use your private key locally; do not paste it into source code or commit `.env`.

```dotenv
GEMINI_API_KEY=your-private-Gemini-API-key
GEMINI_MODEL=gemini-3.8-flash
DEMO_MODE=false
```

`GEMINI_MODEL` can be set to another text-generation model enabled for your
key. The default is `gemini-3.8-flash`, used in [Google's current Gemini API
Python quickstart](https://ai.google.dev/gemini-api/docs/get-started?lang=python).
Set `DEMO_MODE=false` for real provider requests; with no key, the API returns
HTTP 503 instead of demo output.

### Start the app in demo mode (no API key)

**PowerShell window 1 — backend, from the repository root:**

```powershell
$env:DEMO_MODE = "true"
$env:GEMINI_API_KEY = ""
.\.venv\Scripts\python.exe -m uvicorn KeshavBatla.backend_main:app --host 127.0.0.1 --port 8000
```

**PowerShell window 2 — frontend, from the repository root:**

```powershell
cd .\Diviyansh
npm run dev
```

Open <http://127.0.0.1:5173>. Choose **Use sample prompt**, then **Generate &
analyze**. The deterministic sample is visibly marked **Demo mode** and is not
an answer from an AI model.

If port 8000 or 5173 is already occupied, stop the application using that port
if it is yours, or choose another API port. For example, on the backend set
`--port 8002`; also set the frontend environment before starting Vite:

```powershell
# Frontend PowerShell window:
$env:VITE_API_BASE_URL = "http://127.0.0.1:8002/api"
$env:FRONTEND_ORIGINS = "http://127.0.0.1:5173,http://127.0.0.1:5174"
cd .\Diviyansh
npm run dev -- --port 5174
```

When changing the frontend origin/port, set this in the **backend window**
before launching Uvicorn:

```powershell
$env:FRONTEND_ORIGINS = "http://127.0.0.1:5174"
```

### Start the app with live Gemini generation

Put the key in the root `.env` as described above. In the backend PowerShell
window, enable live generation:

```powershell
$env:DEMO_MODE = "false"
.\.venv\Scripts\python.exe -m uvicorn KeshavBatla.backend_main:app --host 127.0.0.1 --port 8000
```

Start Vite in a second window using the command above. The default model is
`gemini-3.8-flash`; change `GEMINI_MODEL` in the root `.env` to another text
model enabled for your key. Never put API keys in `VITE_*` frontend variables:
Vite variables are exposed to the browser.

When no API key is configured and demo mode is disabled, generation returns a
clear HTTP 503 configuration error. Provider failures return a generic HTTP
502 error; key values and provider error details are not sent to the browser.

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/health` | Service status (`{"status":"ok"}`) |
| `POST` | `/api/generate` | Generate a live or explicitly labelled deterministic demo response |
| `POST` | `/api/analyze` | Analyze a non-empty prompt/response pair |
| `GET` | `/docs` | Interactive FastAPI API documentation |

Example request body for `/api/analyze`:

```json
{
  "prompt": "Explain photosynthesis in three points",
  "response": "Plants use sunlight to make food.\n- Water and carbon dioxide are inputs.\n- Oxygen is released."
}
```

The response contains integer `relevance`, `clarity`, `conciseness`,
`completeness`, and `structure` fields (each 0–100), and an `explanations`
array. Generation responses contain `response`, `model`, and `mode` (`live` or
`demo`).

## Run tests and build

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
cd .\Diviyansh
npm run build
```

Tests stub the provider path and do not make paid API requests. The frontend
production output is generated under `Diviyansh\dist\` and is ignored by Git.

## Prototype report

The Prototype Stage report, source, and architecture/DFD diagrams are in
[`project-report-prototype-stage`](./project-report-prototype-stage/). The PDF
is compiled from `main.tex`; editable student roll-number and email placeholders
are intentionally left for the team.

## Limitations and next steps

- Heuristic signals are simple proxies, can mis-score paraphrases and context,
  and do not establish factual correctness or safety.
- The demonstration response is deterministic sample text, not a real LLM
  answer. Live Gemini generation requires a private key and was not exercised
  by the automated tests.
- The Gemini Interactions API is marked experimental by the SDK. The configured
  key's access to `gemini-3.8-flash` and live generation have not been tested;
  set `GEMINI_MODEL` to a text model available to your key if needed.
- Prompt and response history is not saved; the optional model definitions in
  `Gurshant/database_analysis.py` are not connected to runtime code.
- Prompt optimization, revised-response comparison, authentication, and
  deployment are outside this checkpoint.

Do not commit `.env`, key files, local database files, `.venv`, `node_modules`,
or build artifacts. These are ignored by `.gitignore`.
