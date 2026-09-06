# database/analysis.py
# Member 3 — Database & Analysis Engine
# Week 1 deliverable: (1) the database schema for storing prompts, responses,
# and analysis results, and (2) the core heuristic analyzer that computes
# relevance, clarity, conciseness, completeness, and structure scores.
#
# This is the module the backend (Member 2) imports and calls after
# generating a response.

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

# ---------------------------------------------------------------------------
# 1. Database schema (SQLAlchemy models — target: PostgreSQL)
# ---------------------------------------------------------------------------
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class PromptRecord(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    task_type = Column(String(50))  # e.g. explanation, coding, summarization
    created_at = Column(DateTime, default=datetime.utcnow)

    responses = relationship("ResponseRecord", back_populates="prompt")


class ResponseRecord(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    text = Column(Text, nullable=False)
    model = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    prompt = relationship("PromptRecord", back_populates="responses")
    analysis = relationship("AnalysisRecord", back_populates="response", uselist=False)


class AnalysisRecord(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey("responses.id"))
    relevance = Column(Float)
    clarity = Column(Float)
    conciseness = Column(Float)
    completeness = Column(Float)
    structure = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    response = relationship("ResponseRecord", back_populates="analysis")


def get_session(db_url: str = "postgresql://user:pass@localhost/ai_analysis"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


# ---------------------------------------------------------------------------
# 2. Response analysis engine (observable, heuristic — no hidden-reasoning
#    claims, per the project's operational constraints)
# ---------------------------------------------------------------------------

@dataclass
class AnalysisResult:
    relevance: int
    clarity: int
    conciseness: int
    completeness: int
    structure: int
    explanations: List[str] = field(default_factory=list)


def _keyword_overlap(prompt: str, response: str) -> float:
    prompt_words = set(re.findall(r"\w+", prompt.lower())) - _STOPWORDS
    response_words = set(re.findall(r"\w+", response.lower())) - _STOPWORDS
    if not prompt_words:
        return 100.0
    overlap = len(prompt_words & response_words) / len(prompt_words)
    return round(min(overlap, 1.0) * 100, 1)


def _avg_sentence_length(text: str) -> float:
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    words_per_sentence = [len(s.split()) for s in sentences]
    return sum(words_per_sentence) / len(words_per_sentence)


def _has_structure_markers(text: str) -> bool:
    return bool(re.search(r"(^|\n)\s*([-*•]|\d+\.)\s", text)) or "\n#" in text


_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "to", "of", "in", "on",
    "and", "or", "for", "with", "this", "that", "it", "as", "be", "at",
}


def analyze_response(prompt: str, response: str) -> AnalysisResult:
    explanations = []

    # Relevance: keyword overlap between prompt and response
    relevance = _keyword_overlap(prompt, response)
    if relevance < 40:
        explanations.append(
            "Relevance is low — the response shares few key terms with the prompt."
        )

    # Clarity: penalize very long average sentence length
    avg_len = _avg_sentence_length(response)
    clarity = max(0, min(100, round(100 - max(0, avg_len - 20) * 3)))
    if avg_len > 25:
        explanations.append(
            "Sentences are long on average, which may reduce clarity for a general audience."
        )

    # Conciseness: penalize responses much longer than the prompt would suggest
    word_count = len(response.split())
    conciseness = 100 if word_count <= 250 else max(0, 100 - (word_count - 250) // 10)
    if word_count > 400:
        explanations.append(
            "The response is long; consider whether the prompt requested this level of detail."
        )

    # Completeness: rough proxy — does the response address multiple
    # distinct request components found in the prompt (split on 'and', commas)?
    prompt_parts = re.split(r",| and ", prompt)
    covered = sum(1 for part in prompt_parts if _keyword_overlap(part, response) > 30)
    completeness = round((covered / max(1, len(prompt_parts))) * 100, 1)
    if completeness < 60:
        explanations.append(
            "Some parts of the prompt may not be fully addressed in the response."
        )

    # Structure: presence of headings/bullets/numbered lists
    structure = 100 if _has_structure_markers(response) else 50
    if structure < 100 and word_count > 150:
        explanations.append(
            "A longer response like this could benefit from headings or bullet points."
        )

    if not explanations:
        explanations.append("Response aligns well with the prompt on the measured criteria.")

    return AnalysisResult(
        relevance=int(relevance),
        clarity=int(clarity),
        conciseness=int(conciseness),
        completeness=int(completeness),
        structure=int(structure),
        explanations=explanations,
    ).__dict__
