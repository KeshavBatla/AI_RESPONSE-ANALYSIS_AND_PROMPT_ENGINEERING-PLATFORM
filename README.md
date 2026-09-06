# AI Response Analysis and Prompt Engineering Platform

A web-based platform that helps users understand, evaluate, and improve the AI responses they receive from generative AI systems. It analyzes response quality against the user's prompt and explains *why* a response has its observable characteristics — then suggests targeted prompt changes when the response falls short.

Prompt engineering is a supporting feature here, not the core focus. The core focus is response analysis, diagnosis, and explanation.

## Problem

Users often get AI responses that are too long, too short, too technical, incomplete, or misaligned with what they asked for — but they don't always know *why*, or what to change. This platform closes that gap by turning the final response into a transparent, explainable breakdown instead of a black box.

## Core Workflow

```
Prompt → AI Response → Response Analysis → Explanation → Prompt Improvement → Revised Response → Comparison
```

1. User enters a prompt and generates a response.
2. The system analyzes the response for relevance, clarity, conciseness, completeness, structure, and constraint adherence.
3. The dashboard surfaces strengths, weaknesses, and likely causes, tied back to the prompt.
4. If needed, the system suggests a targeted prompt revision.
5. The user regenerates and compares the two responses side by side.

## Features

- **AI Response Analyzer** — scores relevance, clarity, conciseness, completeness, structure, and constraint adherence.
- **Response Diagnosis** — flags observable issues (excessive length, missing info, poor structure, unmet format).
- **Response Explanation** — connects those issues back to specific prompt instructions (no claims about hidden model reasoning).
- **Prompt Analyzer** — extracts task, topic, audience, constraints, tone, and desired format from the prompt.
- **Prompt Optimizer** — suggests targeted prompt edits when a response underperforms.
- **Comparison Dashboard** — shows how prompt changes affect response quality across versions.

## Architecture

Standard 3-tier web app:

| Layer | Tech | Responsibility |
|---|---|---|
| Frontend | React | Prompt input, response display, score visualization, comparisons |
| Backend | Python + FastAPI | AI API calls, analysis orchestration, prompt/response history |
| Database | PostgreSQL | Prompts, responses, analysis results, timestamps |

```
repo/
├── frontend/       # Member 1 — UI: prompt input, response + score display
├── backend/        # Member 2 — FastAPI service, AI API integration
├── database/       # Member 3 — schema + response-analysis engine
└── README.md
```

## Setup

**Backend**
```bash
cd backend
pip install fastapi uvicorn httpx sqlalchemy psycopg2-binary
export ANTHROPIC_API_KEY=your_key_here
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Database**
```bash
# PostgreSQL connection string is set in database/analysis.py (get_session)
# Tables are created automatically on first run via SQLAlchemy metadata.create_all
```

## Evaluation Criteria

- **Primary:** whether the platform consistently identifies real response characteristics and whether responses satisfy the user's stated objective and constraints.
- **Secondary:** response quality, alignment, diagnosis accuracy, explanation usefulness, prompt-impact, and reduction in unnecessary repeated prompts.

## Scope (Iteration 1)

- Prompt input and AI response generation
- Core quality analysis (relevance, clarity, conciseness, completeness, structure, constraints)
- Strengths/weaknesses + response diagnosis display
- Basic response explanation
- Basic prompt component identification and initial improvement suggestions
- Database storage for prompts and responses
- Automated tests for the main workflow

## Later Iterations

- Deeper diagnosis and explanation
- Full prompt/response comparison dashboard
- Multi-task-type analysis (coding, summarization, Q&A)
- Prompt evolution history and A/B testing
- Prompt templates
- Optional multi-provider support

## Constraints & Principles

- No claims about hidden model reasoning or chain-of-thought — explanations are based only on observable prompt/response characteristics.
- Uses an existing AI API rather than training a model.
- Avoids storing unnecessary personal or sensitive conversation content.
- Records the model/version used for each response so comparisons stay interpretable.

## Team

| Member | Area |
|---|---|
| Member 1 | Frontend |
| Member 2 | Backend / AI integration |
| Member 3 | Database / Analysis engine |

## Status

🚧 In development — Software Engineering course project, weekly progress demos.
