---
layout: default
title: Home
---

# WALLY — Ontology Editor + Medical AI Reasoner

**Interactive Knowledge Graph Visualization with Open-Source LLM-Powered Diagnostics**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-HTTPS-blue?style=for-the-badge&logo=nginx)](https://161.35.239.151)
[![LLM](https://img.shields.io/badge/LLM-Llama%203.2%20%E2%80%A2%20Ollama-orange?style=for-the-badge)](https://161.35.239.151/llm/health)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/gpad1234/Startup-One-Wally-Clean)

---

## 🚀 Overview

WALLY combines two complementary AI systems — both **$0 cost**, open-source, and self-hosted:

1. **Ontology Editor** — Fish-eye interactive graph for visualizing and editing large-scale RDF/OWL knowledge graphs
2. **Medical AI Reasoner** — Diagnostic reasoning engine using weighted ontology traversal + Llama 3.2 LLM for natural language symptom input

### ✨ Key Features

**Ontology Editor:**
- **🎯 Fish-Eye Visualization** - Distance-based scaling with center-focus navigation
- **🗺️ Interactive MiniMap** - Click, drag, and scroll for seamless exploration  
- **⚡ BFS Viewport Pagination** - Loads only visible nodes for instant performance
- **🖱️ Click-to-Recenter** - Dynamic viewport updates on node selection
- **📊 Scalable Architecture** - Designed for 1000+ node ontologies

**Medical AI Reasoner:**
- **🏥 Weighted Ontology Reasoning** - Graph traversal scoring diseases vs. symptoms
- **💬 NLP Mode** - Type free-text symptoms, Llama 3.2 extracts them automatically
- **🖱️ Click Mode** - Select symptoms from an interactive visual panel
- **📋 Confidence Scoring** - Percentage match with reasoning path explanation
- **💊 Treatment Recommendations** - Suggested treatments per diagnosis

**Medical Ontology (RDF/OWL Backend):**
- **📄 RDF/Turtle Source of Truth** - `medical_ontology.ttl` drives both the AI Reasoner and Ontology Editor
- **🔬 Disease Ontology Integration** - All 7 diseases enriched with official [DOID](https://disease-ontology.org/) identifiers
- **🏷️ ICD-10-CM Codes** - Standard clinical codes (J00, J11.1, I10…) on every disease
- **📚 MeSH Cross-references** - NLM Medical Subject Headings linked per disease
- **📖 Official Definitions** - Verbatim definitions from disease-ontology.org
- **🔄 Updatable** - Re-run `scripts/enrich_from_do.py` to pull latest DO releases

**LLM Integration:**
- **🤖 Ollama + Llama 3.2** - Free, self-hosted, runs on the same droplet
- **🔒 Privacy-first** - Data never leaves your server
- **💰 Zero cost** - No API keys or subscriptions required

---

## 🎬 Quick Start

```bash
# Clone repository
git clone https://github.com/gpad1234/Startup-One-Wally-Clean.git
cd Startup-One-Wally-Clean

# Terminal 1: Start Flask API
python3 ontology_api.py

# Terminal 2: Start React frontend
cd graph-ui && npm install && npm run dev

# Terminal 3 (optional): Start LLM service
cd ubuntu-deploy && node llm-service.js
```

Visit **http://localhost:5173** — Ontology Editor and Medical AI Reasoner tabs both available.

[📖 Full Getting Started Guide →](getting-started)

---

## 📚 Documentation

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">

<div style="border: 2px solid #3b82f6; border-radius: 8px; padding: 20px; background: #f0f9ff;">
<h3>🎨 Features</h3>
<p>Explore the innovative fish-eye visualization and interactive features</p>
<a href="features">Learn More →</a>
</div>

<div style="border: 2px solid #10b981; border-radius: 8px; padding: 20px; background: #f0fdf4;">
<h3>💻 Development</h3>
<p>Development workflow, architecture, and contribution guidelines</p>
<a href="development">Learn More →</a>
</div>

<div style="border: 2px solid #f59e0b; border-radius: 8px; padding: 20px; background: #fffbeb;">
<h3>🚀 Deployment</h3>
<p>Complete guide for deploying to DigitalOcean or other platforms</p>
<a href="deployment">Learn More →</a>
</div>

<div style="border: 2px solid #8b5cf6; border-radius: 8px; padding: 20px; background: #faf5ff;">
<h3>🏗️ Architecture</h3>
<p>System design, pagination algorithm, and scaling strategies</p>
<a href="architecture">Learn More →</a>
</div>

</div>

---

## 🎯 Live Demo

| Service | URL |
|---------|-----|
| **Frontend** | [https://161.35.239.151](https://161.35.239.151) |
| **LLM Service** | [https://161.35.239.151/llm/health](https://161.35.239.151/llm/health) |
| **API** | [https://161.35.239.151/api/ontology/health](https://161.35.239.151/api/ontology/health) |

> Self-signed cert: click "Advanced → Proceed" in browser.

**Try the Ontology Editor:** click any node to recenter, adjust the radius slider, use the MiniMap.

**Try the Medical AI Reasoner:** go to the 🏥 tab, click "💬 Describe with AI", type your symptoms in plain English. Each diagnosis card shows the official **DOID badge** (links to disease-ontology.org), **ICD-10 code**, and **synonyms** sourced from the Human Disease Ontology.

---

## 🛠️ Technology Stack

### Backend
- **Python 3.12 + Flask** - REST API (port 5002)
- **rdflib 7.6.0** - RDF/OWL ontology handling
- **Node.js + Express** - LLM proxy service (port 3001)
- **Ollama + Llama 3.2** - Open-source LLM (port 11434)

### Frontend
- **React 18 + Vite** - UI framework and build tool
- **ReactFlow** - Graph visualization library

### Infrastructure
- **nginx** - HTTPS reverse proxy (self-signed cert)
- **systemd** - Service management (4 services, auto-restart)
- **DigitalOcean Ubuntu 24.04** - Cloud hosting

---

## 📖 Key Documentation

- **[Getting Started](getting-started)** - Local dev setup in 5 minutes
- **[Architecture](architecture)** - System design, RDF pipeline, and API reference
- **[Deployment](deployment)** - DigitalOcean production deployment guide
- **[Features](features)** - Full feature reference including fish-eye, MiniMap, and Medical Reasoner

---

## 🎨 Fish-Eye Visualization

The fish-eye effect creates a focus+context view where:

- **Center nodes (Distance 0):** Scale 1.8x, bright glow, bold labels
- **Near nodes (Distance 1):** Scale 1.3x, subtle glow
- **Mid nodes (Distance 2):** Scale 1.0x, normal appearance
- **Far nodes (Distance 3+):** Scale 0.7x-0.5x, faded for context

This allows users to focus on specific areas while maintaining awareness of the broader graph structure.

> 🖥️ **[Try it live →](https://161.35.239.151)** — click any node to see the fish-eye effect in action (self-signed cert: click "Advanced → Proceed")

---

## 📊 Performance

- **Viewport Loading:** ~100ms for 50-node viewport
- **Node Recentering:** Instant API fetch (<200ms)
- **Graph Rendering:** 60 FPS with ReactFlow optimization
- **Frontend Bundle:** 131KB gzipped
- **Memory Usage:** ~50MB backend, ~40MB frontend

Designed to scale to **1000+ nodes** with pagination and streaming.

---

## 🔗 API Endpoints

### Core Pagination APIs

```http
GET /api/ontology/graph/nodes?skip=0&limit=10
POST /api/ontology/graph/viewport
  Body: {"center_node": "owl:Thing", "radius": 2, "limit": 50}
GET /api/ontology/graph/neighbors/<node_id>

# Medical ontology endpoints
GET /api/ontology/medical          # Full knowledge graph (diseases/symptoms/treatments)
GET /api/ontology/medical/graph    # OWL classes + individuals for Ontology Editor
```

[📖 Full API Documentation →](api/)

---

## 🤝 Contributing

We welcome contributions! See our [Development Guide](development) for:

- Local development setup
- Code architecture
- Testing strategy
- Pull request process

---

## 📅 Project Timeline

- **Feb 17, 2026** - Initial fish-eye POC implemented
- **Feb 18, 2026** - Production deployment to DigitalOcean
- **Feb 19, 2026** - Interactive MiniMap navigation added
- **Feb 20, 2026** - Medical AI Reasoner + Ollama LLM NLP integration deployed
- **Feb 22, 2026** - RDF medical ontology backend: TTL file, live Flask API, Disease Ontology enrichment (DOID + ICD-10 + MeSH)
- **Coming Soon** - Search, filters, 1000+ node scaling tests, SPARQL query interface

[📖 View Full Roadmap →](https://github.com/gpad1234/Startup-One-Wally-Clean/blob/main/ACTION_PLAN.md)

---

## 📬 Contact & Links

- **GitHub:** [gpad1234/Startup-One-Wally-Clean](https://github.com/gpad1234/Startup-One-Wally-Clean)
- **Live Demo:** [https://161.35.239.151](https://161.35.239.151)
- **LLM Health:** [https://161.35.239.151/llm/health](https://161.35.239.151/llm/health)
- **Documentation:** [GitHub Pages](https://gpad1234.github.io/Startup-One-Wally-Clean/)

---

## 📄 License

See [LICENSE](https://github.com/gpad1234/Startup-One-Wally-Clean/blob/main/LICENSE) file for details.

---

<div style="text-align: center; padding: 40px 0; background: #f8fafc; margin-top: 40px; border-radius: 8px;">
<p style="font-size: 18px; margin-bottom: 15px;">Ready to explore ontologies like never before?</p>
<a href="getting-started" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: bold;">Get Started →</a>
</div>
