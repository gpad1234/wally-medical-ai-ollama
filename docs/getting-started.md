---
layout: default
title: Getting Started
---

# Getting Started

Get WALLY running locally in about 5 minutes.

---

## Prerequisites

| Tool | Minimum | Check |
|------|---------|-------|
| Python | 3.12 | `python3 --version` |
| Node.js | 18 | `node --version` |
| npm | 9 | `npm --version` |
| GCC | any | `gcc --version` |
| Ollama | latest | [ollama.com/download](https://ollama.com/download) |
| Git | any | `git --version` |

> No GPU required — `llama3.2:3b` runs comfortably on CPU with 4 GB RAM.

---

## 1 — Clone the Repository

```bash
git clone https://github.com/gpad1234/wally-medical-ai-ollama.git
cd wally-medical-ai-ollama
```

---

## 2 — Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

Verify:

```bash
pip show ollama flask rdflib
```

---

## 3 — Build the C Core Library

The `libsimpledb.so` shared library is required by the adapter layer:

```bash
cd src/core
make
cd ../..
```

Expected output:

```
gcc -shared -fPIC -o build/lib/libsimpledb.so simple_db.c
Build complete: build/lib/libsimpledb.so
```

---

## 4 — Pull the LLM Model

```bash
ollama pull llama3.2:3b
```

This downloads ~2 GB on first run. Subsequent pulls are cached.

---

## 5 — Start All Services

Open **three terminals** from the project root:

**Terminal 1 — Ollama**

```bash
ollama serve
# Expected: Ollama is running at http://127.0.0.1:11434
```

**Terminal 2 — Flask API**

```bash
source .venv/bin/activate
PYTHONPATH=$(pwd) python graph/ontology_api.py
# Expected: * Running on http://0.0.0.0:5002
```

**Terminal 3 — React UI**

```bash
cd graph-ui
npm install        # first run only
npm run dev
# Expected: ➜  Local:   http://localhost:5173/
```

> If ports 5173–5175 are busy, Vite will auto-select the next free port (e.g. 5176). Check Terminal 3 output for the actual URL.

---

## 6 — Use the Medical AI Reasoner

1. Open **[http://localhost:5173](http://localhost:5173)** in your browser
2. Navigate to the **🏥 Medical AI Reasoner** tab
3. Tick 2–4 symptoms (e.g. *Fever*, *Cough*, *Fatigue*)
4. Click **🔍 Analyze Symptoms** — the JS ontology reasoner responds instantly
5. Click **🦙 Ask AI (Ollama)** — the LLM reasons with your ontology data (~5–15s)

Both results appear side-by-side for comparison.

---

## 7 — Quick API Test

Run a `curl` command against the diagnosis endpoint while all services are up:

```bash
curl -s -X POST http://localhost:5002/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["Fever", "Cough", "Fatigue"]}' | python3 -m json.tool
```

Sample response:

```json
{
  "diagnosis": "Based on the symptoms and the ontology ...",
  "reasoning": "The patient presents with fever, cough ...",
  "model_used": "llama3.2:3b",
  "symptoms_received": ["Fever", "Cough", "Fatigue"]
}
```

---

## Verify Everything

```bash
# Health check
curl http://localhost:5002/api/ontology/health

# Run unit tests
source .venv/bin/activate
pytest tests/ -v --tb=short
```

All **97 pytest tests** should pass.

---

## Project Structure

```
wally-medical-ai-ollama/
├── graph/
│   ├── ontology_api.py          ← Flask REST API (port 5002)
│   └── sample_data/
│       └── medical_ontology.ttl ← RDF/OWL knowledge graph
├── graph-ui/
│   └── src/components/Ontology/
│       ├── MedicalDiagnosisAI.jsx   ← Main React component
│       └── MedicalDiagnosisAI.css
├── src/
│   ├── core/
│   │   ├── simple_db.c/h        ← FNV-1a hash table (C)
│   │   └── Makefile
│   ├── adapters/                ← Python ctypes adapters
│   └── services/                ← Business logic
├── tests/                       ← 97 pytest tests
├── requirements.txt
└── .venv/                       ← Python virtual environment
```

---

## Troubleshooting

### Flask fails: `No module named 'src'`

Always start Flask with `PYTHONPATH`:

```bash
PYTHONPATH=$(pwd) python graph/ontology_api.py
```

### Flask fails: `Library 'libsimpledb.so' not found`

Build the C library:

```bash
cd src/core && make && cd ../..
```

### Ask AI button returns 503

Ollama is not running. Start it:

```bash
ollama serve
```

Check it's reachable: `curl http://localhost:11434/api/tags`

### Slow LLM responses

`llama3.2:3b` on CPU takes ~5–15s. This is normal. For faster responses, a GPU-enabled machine or a larger machine is recommended — no code changes needed.

### Port already in use

If port 5002 is busy: `lsof -ti:5002 | xargs kill -9`

If Vite port conflicts, it auto-selects the next free port — just use the URL printed in Terminal 3.

---

## Running Tests

```bash
source .venv/bin/activate
pytest tests/unit/ -v          # unit tests only
pytest tests/ -v --tb=short    # all 97 tests
pytest tests/ --cov=src        # with coverage report
```

---

[← Back to Home](./) | [API Reference →](api)
