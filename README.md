# WALLY — Ontology Editor + Medical AI Reasoner

**Interactive Knowledge Graph Visualization with Open-Source LLM-Powered Diagnostics**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-HTTPS-blue?style=flat-square&logo=nginx)](https://161.35.239.151)
[![LLM Service](https://img.shields.io/badge/LLM-Llama%203.2%20%E2%80%A2%20Ollama-orange?style=flat-square)](https://161.35.239.151/llm/health)
[![API](https://img.shields.io/badge/API-Flask%205002-green?style=flat-square)](https://161.35.239.151/api/ontology/health)
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-lightgrey?style=flat-square)](https://gpad1234.github.io/Startup-One-Wally-Clean/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=flat-square&logo=github)](https://github.com/gpad1234/Startup-One-Wally-Clean)

---

## 📚 **[Full Documentation →](https://gpad1234.github.io/Startup-One-Wally-Clean/)**

---

## What is WALLY?

WALLY combines two complementary systems:

1. **Ontology Editor** — A fish-eye interactive graph for visualizing and editing large-scale RDF/OWL knowledge graphs
2. **Medical AI Reasoner** — A diagnostic reasoning engine using weighted ontology traversal + open-source LLM (Llama 3.2 via Ollama) for natural language symptom input

Both systems are **$0 cost** — no paid AI APIs, fully open-source, deployed on a DigitalOcean Ubuntu droplet.

---

## 🌐 Live Deployment

| Service | URL | Notes |
|---------|-----|-------|
| **Frontend** | [https://161.35.239.151](https://161.35.239.151) | React app (HTTPS, self-signed cert) |
| **Flask API** | [https://161.35.239.151/api/](https://161.35.239.151/api/) | Ontology REST API |
| **LLM Service** | [https://161.35.239.151/llm/](https://161.35.239.151/llm/) | Ollama Llama 3.2 proxy |
| **Health** | [https://161.35.239.151/health](https://161.35.239.151/health) | nginx health check |

> **Note**: The self-signed cert will trigger a browser warning — click "Advanced → Proceed" to access the site.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Node.js 18+ / npm 10+
- GCC (for C library build)
- [Ollama](https://ollama.com) installed with `llama3.2:3b` pulled

### 1. Create the virtual environment & build C library

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build native hash-table library (one-time)
cd src/core && make && cd ../..
```

### 2. Start Ollama

```bash
ollama pull llama3.2:3b   # first time only (~2 GB)
./scripts/start_llm.sh    # or: ollama serve
```

### 3. Start the Flask Ontology API

```bash
source .venv/bin/activate
PYTHONPATH=$(pwd) python graph/ontology_api.py
# Running on http://localhost:5002
```

### 4. Start the React Frontend

```bash
cd graph-ui
npm install      # first time only
npm run dev
# Running on http://localhost:5173
```

---

## ✨ Features

### 🔬 Ontology Editor

- **Fish-Eye Visualization** — Nodes scale by distance from center (1.8× center → 0.5× periphery)
- **Interactive MiniMap** — Pannable overview with click-to-navigate
- **Click-to-Recenter** — Any node becomes the new viewport center
- **BFS Viewport Pagination** — Loads only visible nodes; scales to 1000+ node ontologies
- **Bidirectional Traversal** — Navigate parent→child and child→parent edges
- **RDF/OWL Support** — Full `rdflib` integration for ontology import/export

### 🏥 Medical AI Reasoner

- **Weighted Ontology Reasoning** — Graph traversal scoring diseases against symptoms
- **7 Diseases × 20 Symptoms × 14 Treatments** — Built-in medical knowledge graph
- **Two input modes**:
  - **Click Mode** — Select symptoms from an interactive panel
  - **NLP Mode** — Type free-text ("I have a headache and fever") → LLM extracts symptoms
- **Confidence Scoring** — Percentage-based match with reasoning path explanation
- **Treatment Recommendations** — Suggested treatments per diagnosis

### 🤖 LLM Integration (Ollama + Llama 3.2) — Sprint 1 ✅

- **Model**: `llama3.2:3b` — ~2 GB, runs locally via Ollama
- **New button**: **🦙 Ask AI (Ollama)** alongside the existing JS reasoner — side-by-side comparison
- **Endpoint**: `POST /api/diagnose` — builds an ontology-grounded prompt, calls `ollama.chat()`, returns `{ diagnosis, reasoning, model_used }`
- **Cost**: $0 — open-source, self-hosted, no API keys
- **Privacy**: All inference runs on your machine

---

## 🏗️ Architecture

```
DigitalOcean Ubuntu 24.04 / 161.35.239.151

  nginx HTTPS :443  (HTTP :80 -> HTTPS redirect)
       |                   |                   |
       v                   v                   v
 wally-frontend     wally-ontology-api    medical-ai-llm
 React 18 + Vite     Flask + rdflib       Node.js Express
    port 5173            port 5002           port 3001
       /                  /api/               /llm/
                                                |
                                                v
                                         ollama :11434
                                        llama3.2:1b model

All four services run as systemd units (auto-restart on failure).
```

---

## 📦 Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React + Vite | 18.2 / 5.x |
| Graph Rendering | ReactFlow | 11.x |
| Backend API | Flask + Python | 3.x / 3.12 |
| Ontology | rdflib | 7.6.0 |
| LLM Runtime | Ollama | latest |
| LLM Model | Llama 3.2 | 3b (~2 GB) |
| C Core | libsimpledb (hash table) | gcc / ctypes |
| Reverse Proxy | nginx | 1.24 |
| SSL | Self-signed cert | 365-day |
| Process Mgmt | systemd | — |
| Hosting | DigitalOcean | Ubuntu 24.04 |

---

## 📁 Key Files

```
wally-medical-ai-ollama/
├── graph/
│   └── ontology_api.py                     # Flask REST API (port 5002)
│                                           #  └─ POST /api/diagnose  ← Sprint 1
├── graph-ui/
│   └── src/components/Ontology/
│       ├── MedicalDiagnosisAI.jsx          # Medical Reasoner (JS + 🦙 Ask AI button)
│       └── MedicalDiagnosisAI.css          # Styles incl. Ollama result panel
├── src/
│   ├── core/
│   │   ├── simple_db.c / .h               # Hash-table C library
│   │   ├── Makefile                        # → build/lib/libsimpledb.so
│   │   └── build/lib/libsimpledb.so        # (generated, not committed)
│   ├── adapters/simple_db.py              # ctypes Python wrapper
│   └── services/                          # Business logic
├── sample_data/medical_ontology.ttl        # 7 diseases · 20 symptoms · 14 treatments
├── requirements.txt                        # incl. ollama>=0.6.0
└── docs/TODO.md                            # Sprint tracker
```

---

## 🔌 API Reference

### Ontology API (`/api/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ontology/health` | Service health |
| GET | `/api/ontology/medical` | Medical knowledge graph (diseases/symptoms/treatments) |
| GET | `/api/ontology/classes` | List all ontology classes |
| POST | `/api/ontology/classes` | Create class |
| **POST** | **`/api/diagnose`** | **🦙 Ollama LLM diagnosis — Sprint 1** |

```bash
# Example: LLM diagnosis via /api/diagnose
curl -X POST http://localhost:5002/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["Fever", "Cough", "Fatigue"]}'
# {"data": {"diagnosis": "...", "reasoning": "...", "model_used": "llama3.2:3b"}}
```

---

## 🖥️ Server Management

```bash
# Connect
ssh -i ~/.ssh/fisheye_rsa root@161.35.239.151

# Check all services
systemctl status wally-frontend wally-ontology-api medical-ai-llm ollama

# Restart / view logs
systemctl restart medical-ai-llm
journalctl -u medical-ai-llm -f
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [MEDICAL_AI_TECH_SPEC.md](MEDICAL_AI_TECH_SPEC.md) | Algorithmic reasoning architecture (827 lines) |
| [MEDICAL_AI_LLM_INTEGRATION.md](MEDICAL_AI_LLM_INTEGRATION.md) | LLM integration design (860 lines) |
| [UBUNTU_OLLAMA_DEPLOYMENT.md](UBUNTU_OLLAMA_DEPLOYMENT.md) | Ubuntu + Ollama setup guide |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Full deployment reference |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [DIGITALOCEAN_DEPLOY.md](DIGITALOCEAN_DEPLOY.md) | DigitalOcean-specific guide |

📖 **[GitHub Pages →](https://gpad1234.github.io/Startup-One-Wally-Clean/)**

---

## ⚡ Performance Notes

- **LLM cold start**: ~90s on 1 GB droplet (model loads from swap)
- **LLM warm requests**: ~5–15s after first load
- **Recommended**: Resize to 2 GB RAM ($12/mo) in DigitalOcean → cold start drops to ~2–3s
- **Algorithmic reasoning**: instant — no LLM required for click-mode diagnosis

---

## License

MIT — see [LICENSE](LICENSE)

---

**Last Updated**: February 25, 2026 · Sprint 1 complete
**Stack**: React 18 · Flask · Ollama Llama 3.2:3b · Python venv · C libsimpledb · rdflib

## Reference:
https://disease-ontology.org/