# Mid-term prototype evaluation checklist

## Before evaluation
- [ ] Pull/open the latest local code; check `git status` before editing.
- [ ] Start backend and frontend using README commands in separate terminals.
- [ ] Open the app in the browser and verify the header/layout looks presentable.
- [ ] Test an example prompt with a configured provider key or visibly labelled demo mode.
- [ ] Confirm response and five metrics appear after the request.
- [ ] Test blank prompt, missing key, and provider/network failure.
- [ ] Visit `/api/health` and check for a healthy JSON response.
- [ ] Run automated tests; keep actual results, do not claim unrun tests.
- [ ] Check browser devtools and backend terminal for errors.
- [ ] Compile the LaTeX report and open the PDF to check diagrams, page breaks, and text.
- [ ] Commit/push code, diagrams, `main.tex`, and `main.pdf` to the project repository.
- [ ] Ensure no `.env`, API keys, local databases, or build artifacts are committed.

## Suggested demo sequence (2–3 minutes)
1. Explain the problem: users see generated answers but often cannot diagnose quality issues.
2. Enter a clear prompt such as: “Explain photosynthesis to a class 8 student in three bullet points.”
3. Generate the answer and point out the five heuristic indicators and their explanations.
4. Explain that scores are transparent heuristics, not factuality guarantees or hidden model reasoning.
5. Show the health endpoint/tests and explain the next planned step: persistence, prompt suggestions, and revised-response comparison.

## Likely questions
**What is the core contribution?** Integrating response generation with observable, explainable response-quality analysis and an iterative prompt-improvement workflow.

**How do your scores work?** The prototype uses transparent heuristics: prompt-response keyword overlap, average sentence length, word count, prompt-part coverage, and presence of formatting markers. These are proxies that need evaluation; they are not a definitive measure of truth or quality.

**Why use an external AI API?** The project is about the software platform, analysis workflow, and user experience, not training a foundation model.

**What happens if the API is unavailable?** The app should show a useful error or clearly label deterministic demo mode; it must not silently fake a live response.

**What is incomplete?** State the actual result honestly. Intended follow-ups are robust persistence/history, prompt-improvement suggestions, revised generation/comparison, broader testing, and security/deployment hardening.

**What are DFDs showing?** Level 0 shows the system boundary and external actors; Level 1 expands into prompt receipt, AI generation, analysis, result presentation, and planned data storage.
