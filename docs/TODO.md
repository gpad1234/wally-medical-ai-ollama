# WALLY Medical AI Reasoner — TODO

**Branch**: `wally-ai-reasoner`
**Project goal**: Wire Ollama locally as a learning/research project. Keep it simple.

---

## Next Session: Wire Ollama (Sprint 1)

- [x] **1. Install Ollama Python package**
  ```bash
  source .venv/bin/activate
  pip install ollama
  # add to requirements.txt
  ```

- [x] **2. Add `POST /api/diagnose` route to `ontology_api.py`**
  - Receive `{ symptoms: ["Fever", "Cough", ...] }` from frontend
  - Build a plain prompt using the ontology data already loaded in memory
  - Call `ollama.chat(model="llama3.2:3b", messages=[...])`
  - Return `{ diagnosis, reasoning, model_used }` JSON

- [x] **3. Update `MedicalDiagnosisAI.jsx`**
  - Add **"Ask AI"** button next to existing "Analyze Symptoms"
  - `POST /api/diagnose` with selected symptoms on click
  - Show LLM response in a new panel (keep existing JS reasoner for side-by-side comparison)
  - Handle loading state + error (Ollama might be slow)

- [ ] **4. Verify end-to-end**
  - `ollama list` confirms `llama3.2:3b` is pulled
  - Select 3 symptoms → click Ask AI → see LLM reasoning in UI
  - curl test: `curl -X POST localhost:5002/api/diagnose -H "Content-Type: application/json" -d '{"symptoms":["Fever","Cough"]}'`

- [ ] **5. Commit**
  ```bash
  git add ontology_api.py graph-ui/src/components/Ontology/MedicalDiagnosisAI.jsx requirements.txt
  git commit -m "Wire Ollama llama3.2:3b into POST /api/diagnose"
  git push origin wally-ai-reasoner
  ```

---

## Startup Checklist (every session)

```bash
# 1. Start Ollama
./start_llm.sh

# 2. Start Flask
source .venv/bin/activate && python ontology_api.py &

# 3. Start React
cd graph-ui && npm run dev

# 4. Verify
curl http://localhost:5002/api/ontology/health
# Open http://localhost:5173
```

---

## Current State (Feb 25, 2026)

- Flask API running on port 5002 — serving 7 diseases, 20 symptoms
- React UI on port 5173 — Medical AI Reasoner only (tabs removed)
- Ollama installed, `llama3.2:3b` pulled, service runs via `./start_llm.sh`
- 97 pytest tests passing
- **Ollama is NOT yet wired into the UI** — that's Sprint 1 above

---

## Future Ideas (after Sprint 1 works)

- Stream LLM response token-by-token (SSE) instead of waiting for full response
- Show "Reasoning Trace" panel alongside the answer
- Try swapping in a different model (e.g. `mistral`) to compare output
