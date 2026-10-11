import { useState } from "react";
import "./frontend.css";

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api"
).replace(/\/+$/, "");

const SCORE_LABELS = [
  ["relevance", "Relevance", "Keyword overlap with the prompt"],
  ["clarity", "Clarity", "Average sentence length"],
  ["conciseness", "Conciseness", "Response word count"],
  ["completeness", "Completeness", "Coverage of prompt components"],
  ["structure", "Structure", "Headings and list formatting"],
];

const SAMPLE_PROMPT =
  "Explain photosynthesis to a class 8 student in three bullet points.";

async function requestJson(path, body) {
  const response = await fetch(`${API_BASE}/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(data.detail)
      ? data.detail.map((item) => item.msg).join(" ")
      : data.detail;
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return data;
}

function ScoreCard({ label, description, value }) {
  const tone = value >= 75 ? "strong" : value >= 50 ? "moderate" : "low";
  return (
    <article className="score-card">
      <div className="score-card-top">
        <span className="score-label">{label}</span>
        <span className={`score-value ${tone}`}>{value}<small>/100</small></span>
      </div>
      <div
        className="score-track"
        role="meter"
        aria-label={`${label} heuristic score`}
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow={value}
      >
        <span className={`score-fill ${tone}`} style={{ width: `${value}%` }} />
      </div>
      <p>{description}</p>
    </article>
  );
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async (event) => {
    event.preventDefault();
    if (!prompt.trim()) {
      setError("Enter a prompt before generating a response.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    setAnalysis(null);

    try {
      const generated = await requestJson("generate", { prompt: prompt.trim() });
      const scored = await requestJson("analyze", {
        prompt: prompt.trim(),
        response: generated.response,
      });
      setResult(generated);
      setAnalysis(scored);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="ResponseLens home">
          <span className="brand-mark" aria-hidden="true">R</span>
          <span>ResponseLens</span>
        </a>
        <span className="prototype-label"><span /> Prototype</span>
      </header>

      <section className="intro">
        <p className="eyebrow">AI RESPONSE EVALUATION</p>
        <h1>Understand the answer.<br /><span>Improve the next prompt.</span></h1>
        <p className="intro-copy">
          Generate a response and explore five transparent, heuristic quality indicators.
        </p>
      </section>

      <form className="prompt-panel panel" onSubmit={handleGenerate}>
        <div className="panel-heading">
          <div>
            <p className="eyebrow">01 / YOUR PROMPT</p>
            <h2>What would you like to explore?</h2>
          </div>
          <button
            className="text-button"
            type="button"
            onClick={() => setPrompt(SAMPLE_PROMPT)}
            disabled={loading}
          >
            Use sample prompt <span aria-hidden="true">↗</span>
          </button>
        </div>
        <label className="visually-hidden" htmlFor="prompt">Your prompt</label>
        <textarea
          id="prompt"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="For example: Explain photosynthesis to a class 8 student in three bullet points."
          maxLength={12000}
          rows={4}
          disabled={loading}
          aria-describedby="prompt-help"
        />
        <div className="form-footer">
          <span id="prompt-help">{prompt.length.toLocaleString()} / 12,000 characters</span>
          <button className="primary-button" type="submit" disabled={loading || !prompt.trim()}>
            {loading ? <><span className="spinner" /> Working…</> : <>Generate &amp; analyze <span aria-hidden="true">→</span></>}
          </button>
        </div>
        {error && <p className="error-message" role="alert">{error}</p>}
      </form>

      {loading && (
        <div className="loading-message" role="status">
          <span className="spinner" /> Generating your response and evaluating its observable features…
        </div>
      )}

      {result && analysis && (
        <section className="results" aria-live="polite">
          {result.mode === "demo" && (
            <div className="demo-banner">
              <span aria-hidden="true">ⓘ</span>
              <div><strong>Demo mode</strong><p>This deterministic sample is not an AI-generated answer.</p></div>
            </div>
          )}
          <div className="results-heading">
            <div>
              <p className="eyebrow">02 / RESPONSE</p>
              <h2>Generated answer</h2>
            </div>
            <span className={`mode-pill ${result.mode}`}>{result.mode === "live" ? "Live · Gemini" : "Demo · Sample"}</span>
          </div>
          <article className="response-card panel">
            <div className="response-meta"><span>MODEL</span><span>{result.model}</span></div>
            <p className="response-text">{result.response}</p>
          </article>

          <div className="analysis-heading">
            <div>
              <p className="eyebrow">03 / QUALITY ANALYSIS</p>
              <h2>Five heuristic indicators</h2>
            </div>
            <p>Signals to help you review the response — not a factuality check.</p>
          </div>
          <div className="score-grid">
            {SCORE_LABELS.map(([key, label, description]) => (
              <ScoreCard key={key} label={label} description={description} value={analysis[key]} />
            ))}
          </div>
          <article className="explanations panel">
            <div className="explanations-title">
              <span className="insight-mark" aria-hidden="true">✳</span>
              <div><p className="eyebrow">OBSERVATIONS</p><h3>What the indicators suggest</h3></div>
            </div>
            <ul>{analysis.explanations.map((line, index) => <li key={`${index}-${line}`}>{line}</li>)}</ul>
          </article>
        </section>
      )}

      {!loading && !result && !error && (
        <div className="empty-state">
          <span className="empty-icon" aria-hidden="true">✳</span>
          <p>Your response and quality breakdown will appear here.</p>
        </div>
      )}

      <footer className="footer">
        <span>Built for thoughtful AI use</span>
        <span>Scores are heuristic indicators and do not establish truth or correctness.</span>
      </footer>
    </main>
  );
}
