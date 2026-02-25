---
layout: default
title: Home
---

# WALLY — Medical AI Reasoner

**Symptom-based diagnostic reasoning powered by a local ontology knowledge graph + Ollama LLM**

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![Ollama](https://img.shields.io/badge/LLM-llama3.2%3A3b-orange?style=for-the-badge)](https://ollama.com)
[![GitHub](https://img.shields.io/badge/GitHub-wally--medical--ai--ollama-black?style=for-the-badge&logo=github)](https://github.com/gpad1234/wally-medical-ai-ollama)

---

## What is WALLY?

WALLY is a local research project that wires an **RDF/OWL medical ontology** directly to a **locally-running LLM** (Ollama `llama3.2:3b`) through a React UI.

Select symptoms → **two reasoning engines run side-by-side**:

| Engine | How it works | Speed |
|--------|-------------|-------|
| 🔍 **JS Ontology Reasoner** | Weighted graph traversal scores diseases against symptoms | Instant |
| 🦙 **Ask AI (Ollama)** | LLM prompted with ontology context gives natural-language reasoning | ~5–15s |

**100% local** — no cloud, no API keys, $0 cost.

---

## ✨ Key Features

- **Medical knowledge graph** — `medical_ontology.ttl` with 7 diseases, 20 symptoms, 14 treatments (RDF/OWL)
- **Ontology-grounded prompting** — `/api/diagnose` builds a structured prompt from live TTL data then calls the LLM
- **Side-by-side comparison** — JS reasoner + LLM response shown together
- **Confidence scoring** — percentage match with ontology classification chain
- **97 pytest tests** — full unit coverage of service and adapter layers

---

## 🎬 Quick Start

```bash
# 1 — environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd src/core && make && cd ../..

# 2 — Ollama
ollama pull llama3.2:3b && ollama serve

# 3 — Flask API
PYTHONPATH=$(pwd) python graph/ontology_api.py

# 4 — React UI
cd graph-ui && npm install && npm run dev
```

Open **[http://localhost:5173](http://localhost:5173)** → pick symptoms → hit **🦙 Ask AI (Ollama)**.

[📖 Full Getting Started Guide →](getting-started)

---

## 🏗️ Architecture

```
Browser (React 18 + Vite :5173)
        │
        ├─ GET  /api/ontology/medical  ──► Flask :5002
        │                                      │
        └─ POST /api/diagnose  ────────────────┤
                                               │  rdflib parses medical_ontology.ttl
                                               │  builds ontology-grounded prompt
                                               ▼
                                        Ollama :11434
                                        llama3.2:3b (local)
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

<div style="text-align: center; padding: 40px 0; background: #f8fafc; margin-top: 40px; border-radius: 8px;">
<p style="font-size: 18px; margin-bottom: 15px;">Ready to run WALLY locally?</p>
<a href="getting-started" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: bold;">Get Started →</a>
&nbsp;&nbsp;
<a href="api" style="display: inline-block; background: #10b981; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: bold;">API Reference →</a>
</div>
