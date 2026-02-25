# WALLY — Medical AI Reasoner

**Symptom-based diagnostic reasoning powered by a local ontology knowledge graph + Ollama LLM**

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/API-Flask%205002-green?style=flat-square)](http://localhost:5002/api/ontology/health)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20llama3.2%3A3b-orange?style=flat-square)](https://ollama.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB?style=flat-square&logo=react)](http://localhost:5173)
[![Tests](https://img.shields.io/badge/Tests-97%20passing-brightgreen?style=flat-square)](tests/)

---

## What is WALLY?

WALLY is a local research/learning project that wires an **RDF/OWL medical ontology** to a **locally-running LLM** (Ollama `llama3.2:3b`) through a React UI.

Select symptoms → **two reasoning engines run side-by-side**:

| Engine | How it works | Speed |
|--------|-------------|-------|
| 🔍 **JS Ontology Reasoner** | Weighted graph traversal scores diseases against symptoms | Instant |
| 🦙 **Ask AI (Ollama)** | LLM prompted with ontology context gives natural-language reasoning | ~5–15s |

Everything runs **100% locally** — no cloud, no API keys, $0 cost.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+ / npm
- GCC
- [Ollama](https://ollama.com) installed

### 1. Clone & set up environment

```bash
git clone https://github.com/gpad1234/wally-medical-ai-ollama.git
cd wally-medical-ai-ollama

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build the native C hash-table library (one-time)
cd src/core && make && cd ../..
```

### 2. Pull the LLM model & start Ollama

```bash
ollama pull llama3.2:3b   # ~2 GB download, one-time
ollama serve              # or: ./scripts/start_llm.sh
```

### 3. Start the Flask API

```bash
source .venv/bin/activate
PYTHONPATH=$(pwd) python graph/ontology_api.py
# → http://localhost:5002
```

### 4. Start the React frontend

```bash
cd graph-ui
npm install   # first time only
npm run dev
# → http://localhost:5173
```

Open **http://localhost:5173**, pick symptoms, hit **🦙 Ask AI (Ollama)**.

---

## ✨ Features

- **Medical knowledge graph** — `sample_data/medical_ontology.ttl` with 7 diseases, 20 symptoms, 14 treatments (RDF/OWL, parsed by `rdflib`)
- **Ontology-grounded prompting** — `/api/diagnose` builds a structured prompt from the live TTL data before calling the LLM
- **Side-by-side comparison** — JS weighted reasoner result + LLM natural-language reasoning shown together
- **Confidence scoring** — percentage match with ontology classification chain displayed
- **Loading & error states** — graceful fallback if Ollama is not running
- **97 pytest tests** — full unit coverage of the service and adapter layers

---

## 🏗️ Architecture

```
Browser (React 18 + Vite)
        │
        ├─ GET  /api/ontology/medical  ──► Flask (port 5002)
        │                                      │
        └─ POST /api/diagnose  ────────────────┤
                                               │  rdflib parses medical_ontology.ttl
                                               │  builds ontology-grounded prompt
                                               ▼
                                        Ollama :11434
                                        llama3.2:3b (local)
```

---

## 📁 Project Structure

```
wally-medical-ai-ollama/
├── graph/
│   └── ontology_api.py              # Flask REST API (port 5002)
│                                    #  ├─ GET  /api/ontology/medical
│                                    #  └─ POST /api/diagnose  ← Ollama LLM
├── graph-ui/
│   └── src/components/Ontology/
│       ├── MedicalDiagnosisAI.jsx   # Symptom selector + dual-engine results
│       └── MedicalDiagnosisAI.css
├── src/
│   ├── core/
│   │   ├── simple_db.c / .h        # FNV-1a chained hash-table (C)
│   │   └── Makefile                # → build/lib/libsimpledb.so
│   ├── adapters/simple_db.py       # ctypes wrapper
│   └── services/                   # OntologyService, GraphService …
├── sample_data/
│   └── medical_ontology.ttl        # 7 diseases · 20 symptoms · 14 treatments
├── tests/                          # 97 pytest unit tests
├── requirements.txt                # flask, rdflib, ollama>=0.6.0, pytest …
└── docs/TODO.md                    # Sprint tracker
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ontology/health` | Service health check |
| GET | `/api/ontology/medical` | Full medical knowledge graph as JSON |
| **POST** | **`/api/diagnose`** | **LLM diagnosis via Ollama** |

```bash
# Test the LLM endpoint directly
curl -X POST http://localhost:5002/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["Fever", "Cough", "Fatigue"]}'
```

```json
{
  "data": {
    "diagnosis": "Based on the symptoms...",
    "reasoning": "LLM-based reasoning over medical ontology (3 symptoms analyzed)",
    "model_used": "llama3.2:3b",
    "symptoms_received": ["Fever", "Cough", "Fatigue"]
  }
}
```

---

## 🧪 Tests

```bash
source .venv/bin/activate
pytest tests/ -v
# 97 passed
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Backend API | Flask + Python 3.12 |
| Ontology parsing | rdflib 7.6.0 |
| LLM runtime | Ollama (local) |
| LLM model | llama3.2:3b |
| C core library | libsimpledb — FNV-1a hash table (ctypes) |
| Testing | pytest 8 + pytest-cov |

---

## License

MIT — see [LICENSE](LICENSE)

---

**Last updated**: February 25, 2026 · Sprint 1 complete  
**Reference**: https://disease-ontology.org/