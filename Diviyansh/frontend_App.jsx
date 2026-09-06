// frontend/src/App.jsx
// Member 1 — Frontend
// Week 1 deliverable: prompt input, AI response display, and a basic
// visualization of the response-quality scores returned by the backend.

import { useState } from "react";

const API_BASE = "http://localhost:8000/api";

function ScoreBar({ label, value }) {
  // value is expected to be 0-100
  const color = value >= 75 ? "#2e7d32" : value >= 50 ? "#f9a825" : "#c62828";
  return (
    <div style={{ marginBottom: "8px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px" }}>
        <span>{label}</span>
        <span>{value}/100</span>
      </div>
      <div style={{ background: "#eee", borderRadius: "4px", height: "8px" }}>
        <div
          style={{
            width: `${value}%`,
            background: color,
            height: "8px",
            borderRadius: "4px",
            transition: "width 0.3s ease",
          }}
        />
      </div>
    </div>
  );
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setResponse(null);
    setAnalysis(null);

    try {
      // Step 1: get the AI response
      const genRes = await fetch(`${API_BASE}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      if (!genRes.ok) throw new Error("Generation request failed");
      const genData = await genRes.json();
      setResponse(genData.response);

      // Step 2: analyze the response against the prompt
      const analyzeRes = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, response: genData.response }),
      });
      if (!analyzeRes.ok) throw new Error("Analysis request failed");
      const analyzeData = await analyzeRes.json();
      setAnalysis(analyzeData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: "22px" }}>AI Response Analysis Platform</h1>
      <p style={{ color: "#555", fontSize: "14px" }}>
        Enter a prompt, generate a response, and see a breakdown of its quality.
      </p>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type your prompt here..."
        rows={4}
        style={{ width: "100%", padding: "10px", fontSize: "14px", boxSizing: "border-box" }}
      />

      <button
        onClick={handleGenerate}
        disabled={loading}
        style={{
          marginTop: "10px",
          padding: "10px 18px",
          background: "#1565c0",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Generating..." : "Generate & Analyze"}
      </button>

      {error && <p style={{ color: "#c62828" }}>Error: {error}</p>}

      {response && (
        <div style={{ marginTop: "24px" }}>
          <h3>Response</h3>
          <div style={{ background: "#fafafa", padding: "12px", borderRadius: "6px", whiteSpace: "pre-wrap" }}>
            {response}
          </div>
        </div>
      )}

      {analysis && (
        <div style={{ marginTop: "24px" }}>
          <h3>Quality Analysis</h3>
          <ScoreBar label="Relevance" value={analysis.relevance} />
          <ScoreBar label="Clarity" value={analysis.clarity} />
          <ScoreBar label="Conciseness" value={analysis.conciseness} />
          <ScoreBar label="Completeness" value={analysis.completeness} />
          <ScoreBar label="Structure" value={analysis.structure} />

          <h4 style={{ marginTop: "16px" }}>Explanation</h4>
          <ul style={{ fontSize: "14px" }}>
            {analysis.explanations.map((line, idx) => (
              <li key={idx}>{line}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
