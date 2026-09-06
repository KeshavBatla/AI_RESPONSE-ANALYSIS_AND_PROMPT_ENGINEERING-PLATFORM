# backend/main.py
# Member 2 — Backend
# Week 1 deliverable: FastAPI service that (a) calls the AI provider to
# generate a response for a given prompt, and (b) exposes an endpoint that
# runs the response-analysis module (built by Member 3) and returns scores.

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# NOTE: analyzer + DB models live in database/analysis.py (Member 3's file).
# During integration, this import will point at the shared module, e.g.:
# from database.analysis import analyze_response, save_interaction
# For now this file includes a light local stub so the backend can run
# and be demoed independently this week.

app = FastAPI(title="AI Response Analysis Platform - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this before deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


class GenerateRequest(BaseModel):
    prompt: str
    model: str = "claude-sonnet-4-6"


class GenerateResponse(BaseModel):
    response: str
    model: str


class AnalyzeRequest(BaseModel):
    prompt: str
    response: str


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        text = await call_ai_provider(req.prompt, req.model)
    except Exception as exc:  # pragma: no cover - network dependent
        raise HTTPException(status_code=502, detail=f"AI provider error: {exc}")

    return GenerateResponse(response=text, model=req.model)


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    # Delegates to Member 3's analysis module once merged. Placeholder
    # local scoring keeps this endpoint runnable during independent testing.
    from local_analysis_stub import analyze_response

    result = analyze_response(req.prompt, req.response)
    return result


async def call_ai_provider(prompt: str, model: str) -> str:
    """
    Calls the Anthropic Messages API to generate a response for the given
    prompt. Kept as a thin wrapper so the provider can be swapped later
    (matches the 'multiple AI providers' scalability goal in the proposal).
    """
    import httpx

    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return "".join(block.get("text", "") for block in data.get("content", []))


@app.get("/api/health")
def health():
    return {"status": "ok"}
