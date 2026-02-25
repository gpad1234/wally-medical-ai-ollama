# WALLY — Medical Ontology Platform
## Pre-Sales Technical Specification & Product Vision

**Version**: 1.0  
**Date**: February 23, 2026  
**Status**: Production — Algorithmic Reasoning + Live LLM NLP Integration  
**Audience**: Prospective Customers, Healthcare IT Partners, Investors

---

## Executive Summary

WALLY is an interactive medical knowledge graph platform that structures clinical knowledge — diseases, symptoms, treatments, and their relationships — into a navigable, computable ontology. The current version demonstrates deterministic diagnostic reasoning without AI, establishing a robust, explainable foundation. The near-term roadmap integrates Large Language Models (LLMs) to enable natural language interaction, adaptive learning, and clinical decision support at scale.

> **Key Value Proposition**: WALLY bridges the gap between raw clinical data and actionable diagnostic intelligence — starting with zero-cost, fully transparent graph algorithms today, and evolving toward production-grade medical AI tomorrow.

---

## 1. Objective

### 1.1 The Problem

Modern healthcare is data-rich but knowledge-poor at the point of care:

- Clinicians cannot manually cross-reference thousands of symptom-disease relationships in real time
- Rule-based clinical decision support tools are rigid, brittle, and costly to update
- AI black boxes (GPT-style systems used directly) lack auditability, which is a regulatory and patient-safety concern
- Rare disease diagnosis averages **4–7 years** due to incomplete pattern-matching by clinicians

### 1.2 The WALLY Solution

WALLY encodes clinical knowledge as a **semantic ontology graph** — a structured network of concepts, relationships, and weighted edges — and applies reasoning algorithms to produce ranked, explainable differential diagnoses.

**Current system (v1.0 — Production):**
- Symptom selection → weighted graph traversal → ranked disease matches with confidence scores
- Hierarchical disease classification with official **DOID identifiers** (Disease Ontology), **ICD-10-CM codes** (J00, J11.1, I10…), and **MeSH cross-references** — live on every disease node
- RDF/OWL backend: `medical_ontology.ttl` is the source of truth for both the Ontology Editor and the Medical Reasoner
- Full reasoning trace: every score is explainable — no black box
- **NLP mode live**: free-text symptom input via Llama 3.2 (Ollama) — zero API cost, fully self-hosted
- Auto-enrichment pipeline (`scripts/enrich_from_do.py`) keeps disease definitions current from disease-ontology.org

**Near-term goal (v2.0):**
- Expand LLM integration depth: clinical note parsing (SOAP format), voice input via Whisper, multilingual support
- The ontology remains the **ground truth**; the LLM is a reasoning assistant, not an oracle

### 1.3 Target Markets

| Segment | Use Case | Value |
|---|---|---|
| Primary Care Clinics | Differential diagnosis support | Reduce missed diagnoses |
| Telemedicine Platforms | Triage automation | Faster, safer patient routing |
| Medical Education | Teaching diagnostic reasoning | Interactive case-based learning |
| Healthcare IT Vendors | Embeddable reasoning API | White-label clinical decision tool |
| Pharmaceutical R&D | Disease-symptom mapping | Drug target discovery, trial matching |
| Insurance / Utilization Review | Claim plausibility scoring | Fraud reduction, coding accuracy |

---

## 2. Current System Architecture (v1.0)

### 2.1 Technology Stack

| Layer | Technology | Role |
|---|---|---|
| Frontend | React 18 + Vite + ReactFlow | Interactive graph visualization and diagnostic UI |
| API Layer | Python 3.12 + Flask + rdflib 7.6.0 | REST ontology service (port 5002); RDF/OWL parsing |
| LLM Proxy | Node.js + Express | Ollama proxy service (port 3001) |
| LLM Engine | Ollama + Llama 3.2 | Free-text symptom extraction (port 11434) |
| Reasoning Engine | JavaScript (client-side) | Weighted graph traversal, scoring, ranking |
| Knowledge Base | RDF/Turtle (`medical_ontology.ttl`) | OWL ontology — source of truth for editor and reasoner |
| Ontology Standards | DOID + ICD-10-CM + MeSH | Official disease identifiers on every node |
| Visualization | Fish-eye + BFS Viewport Pagination | Pan, zoom, loads only visible nodes for instant performance |
| Infrastructure | nginx + systemd (4 services) | HTTPS reverse proxy; auto-restart service management |
| Deployment | DigitalOcean Ubuntu 24.04 | $0 AI cost, open-source stack |

### 2.2 System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Browser Client                        │
│  ┌─────────────────────┐   ┌─────────────────────────┐ │
│  │  Ontology Editor    │   │  Medical Reasoner UI    │ │
│  │  (D3.js fish-eye    │   │  (Symptom selector +    │ │
│  │   graph editor)     │   │   diagnostic results)   │ │
│  └──────────┬──────────┘   └────────────┬────────────┘ │
│             │ REST API                  │ In-memory    │
└─────────────┼───────────────────────────┼──────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  Flask Ontology API     │   │  Medical Ontology JSON  │
│  /api/ontology/*        │   │  (client-side engine)   │
│  - CRUD nodes/edges     │   │  - 7 diseases           │
│  - Import/Export RDF    │   │  - 20 symptoms          │
│  - Graph queries        │   │  - 14 treatments        │
│  - Property management  │   │  - weighted edges       │
└─────────────────────────┘   └─────────────────────────┘
```

### 2.3 Diagnostic Reasoning Algorithm

The core engine is a **weighted graph traversal with hierarchical propagation**:

```
Input: [symp:Fever, symp:Cough, symp:ChestPain, symp:ShortnessOfBreath]

For each disease D in ontology:
  1. weighted_score(D) = Σ( symptom_weight[s] for s in input ∩ D.symptoms )
  2. coverage(D) = |input ∩ D.symptoms| / |D.symptoms|
  3. confidence(D) = normalized(weighted_score) × coverage_penalty

Ontology enrichment:
  4. Traverse parent chain: resp:Pneumonia → resp:LowerRespiratoryInfection → resp:RespiratoryDisease
  5. Propagate context: inherited properties, severity class, care pathway

Output: Ranked differential [Pneumonia 87%, Bronchitis 61%, Influenza 54%]
        + reasoning trace
        + treatment recommendations
```

**Key design principle**: Every diagnosis is fully auditable. No probabilistic opaqueness.

### 2.4 Knowledge Base Schema

```javascript
// Disease node
{
  id: "resp:Pneumonia",         // Namespaced IRI (ICD-compatible)
  label: "Pneumonia",
  parent: "resp:LowerRespiratoryInfection",  // Ontology hierarchy
  symptoms: ["symp:Fever", "symp:Cough", "symp:ChestPain", ...],
  severity: "severe",           // mild | moderate | severe
  treatments: ["treat:Antibiotics", "treat:Hospitalization", ...],
  description: "Inflammation of lung tissue, often bacterial"
}

// Symptom node
{
  id: "symp:Fever",
  label: "Fever",
  weight: 0.8                   // Diagnostic specificity (0.0–1.0)
}
```

### 2.5 Current Knowledge Coverage

| System | Diseases | Symptoms | Treatments |
|---|---|---|---|
| Respiratory | Pneumonia, Bronchitis, Influenza, Common Cold | 8 | 7 |
| Digestive | Gastroenteritis | 4 | 3 |
| Neurological | Migraine | 4 | 2 |
| Cardiovascular | Hypertension | 4 | 2 |
| **Total** | **7** | **20** | **14** |

Each disease node carries:
- **DOID identifier** linking to the official [Disease Ontology](https://disease-ontology.org/) definition
- **ICD-10-CM code** (e.g., J18.9 Pneumonia, J11.1 Influenza, I10 Hypertension)
- **MeSH cross-reference** (NLM Medical Subject Headings)
- **Verbatim clinical definition** from disease-ontology.org

> **Expansion capability**: The RDF/Turtle schema is domain-agnostic. Re-running `scripts/enrich_from_do.py` pulls the latest Disease Ontology release automatically. Any specialty (oncology, dermatology, psychiatry) can be added without architecture changes.

### 2.6 Measured Performance

| Metric | Value |
|---|---|
| Viewport load (50-node BFS) | ~100ms |
| Node recentering (API fetch) | <200ms |
| Graph render frame rate | 60 FPS (ReactFlow optimized) |
| Frontend bundle size | 131KB gzipped |
| Backend memory footprint | ~50MB |
| Frontend memory footprint | ~40MB |
| Designed scale target | 1,000+ nodes with pagination |

---

## 3. Current System Capabilities

### 3.1 Ontology Editor
- Visual fish-eye graph rendering with D3.js — pan, zoom, select
- Add / edit / delete nodes and edges via interactive UI
- OWL/RDF import and export
- Class hierarchy browser (subclass tree)
- Property management (object properties, data properties)
- Multi-user collaboration ready (API-first design)

### 3.2 Medical Reasoner
- **Click mode**: Select symptoms from an interactive visual panel
- **NLP mode** *(live)*: Type free-text symptoms in plain English — Llama 3.2 extracts structured symptom IDs automatically
- Confidence-ranked differential diagnosis with percentage scores
- Full reasoning trace (which symptoms matched, weights applied, ontology path)
- Disease cards display official **DOID badge** (links to disease-ontology.org), **ICD-10 code**, synonyms, and verbatim clinical definition
- Ontology path visualization (disease → parent class → category)
- Treatment recommendations per matched disease
- Severity triage indication (mild / moderate / severe)

### 3.3 Developer / Integration API
- REST API at `/api/ontology/*` — full CRUD for nodes, edges, properties
- RDF/OWL endpoints: serve `medical_ontology.ttl` classes + individuals to the Ontology Editor
- Viewport pagination API: `POST /api/ontology/graph/viewport` — BFS from center node, radius-limited
- Medical knowledge API: `GET /api/ontology/medical` — full disease/symptom/treatment graph
- JSON-LD and RDF/XML serialization support
- Health endpoints for CI/CD and monitoring (`/health`, `/api/ontology/health`, `/llm/health`)
- Embeddable as a microservice; LLM proxy decoupled on separate port

---

## 4. LLM Integration — Near-Future Roadmap (v2.0)

### 4.1 Why LLMs on Top of Ontologies?

| Capability | Ontology Alone | LLM Alone | WALLY Hybrid |
|---|---|---|---|
| Structured knowledge | ✅ Excellent | ❌ Hallucination risk | ✅ Excellent |
| Free-text input | ❌ Rigid | ✅ Excellent | ✅ Excellent |
| Explainability | ✅ Full trace | ❌ Black box | ✅ Full trace |
| Clinical safety | ✅ Deterministic | ⚠️ Unreliable alone | ✅ Ontology-grounded |
| Knowledge updates | Manual | ❌ Retraining required | ✅ Edit graph in UI |
| Rare diseases | ❌ Manual addition | ⭐ Can suggest | ✅ Graph + LLM suggestions |

The hybrid architecture solves the core tension in medical AI: **flexibility vs. safety**.

### 4.2 v2.0 Architecture — Ontology-Grounded LLM

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Input Layer                            │
│                                                                 │
│   "Patient reports persistent dry cough for 3 weeks,           │
│    low-grade fever, and night sweats"                           │
│           [Free-text clinical note OR voice input]              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                  NLP Extraction Layer (LLM)                    │
│                                                               │
│  Input → Structured Symptoms:                                 │
│    symp:DryCough (duration: 3 weeks)                          │
│    symp:LowGradeFever                                         │
│    symp:NightSweats                                           │
│                                                               │
│  Also flags: Duration anomaly → elevates TB/lymphoma signals  │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│               Medical Ontology Reasoning Engine               │
│           (unchanged — deterministic, auditable)              │
│                                                               │
│  Weighted graph traversal → ranked differential               │
│  ┌─────────────────────────────────────────┐                 │
│  │  1. Tuberculosis          72% confidence│                 │
│  │  2. Atypical Pneumonia    61% confidence│                 │
│  │  3. Lymphoma (flag)       43% confidence│                 │
│  └─────────────────────────────────────────┘                 │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│               LLM Explanation & Enrichment Layer              │
│                                                               │
│  "The 3-week duration of dry cough combined with night sweats │
│   places tuberculosis at the top of the differential. Per     │
│   CDC guidelines, TB workup including Mantoux test and CXR    │
│   is indicated. Lymphoma should be co-investigated given      │
│   the B-symptom pattern..."                                   │
│                                                               │
│  Grounded in ontology facts — no hallucination of symptoms    │
└───────────────────────────────────────────────────────────────┘
```

### 4.3 Recommended LLM: Clinical Use Cases

#### Primary Recommendation: **Meta LLaMA 3.1 / 3.2 (70B or 8B)**

**Why LLaMA for WALLY:**

| Factor | LLaMA 3.1/3.2 | GPT-4o | Claude 3.5 | Gemini 1.5 |
|---|---|---|---|---|
| **Cost** | $0 (self-hosted) | ~$15/M tokens | ~$15/M tokens | ~$7/M tokens |
| **Data privacy** | ✅ On-premises | ❌ Data leaves org | ❌ Data leaves org | ❌ Data leaves org |
| **HIPAA compliance** | ✅ Achievable self-hosted | Business Associate Agreement required | BAA required | BAA required |
| **Medical fine-tuning** | ✅ MedLLaMA, Meditron available | Not accessible | Not accessible | Not accessible |
| **Current WALLY stack** | ✅ Already using Ollama/LLaMA | New dependency | New dependency | New dependency |
| **Offline / air-gapped** | ✅ Yes | ❌ No | ❌ No | ❌ No |

**Deployment tiers:**

| Scenario | Model | Hardware | Use Case |
|---|---|---|---|
| Development / demo | `llama3.2:1b` via Ollama | Any laptop (CPU) | Prototyping, testing |
| Clinical pilot | `llama3.1:8b` via Ollama | DigitalOcean GPU droplet | Small clinic, telemedicine |
| Enterprise / hospital | `llama3.1:70b` or `Meditron-70B` | On-prem GPU server (A100) | Full EHR integration |

#### Secondary Recommendation: **Meditron-70B (EPFL)**
A LLaMA 2-based model fine-tuned on medical literature (PubMed, clinical guidelines). Achieves near-GPT-4 performance on clinical benchmarks (MedQA, MedMCQA) while remaining fully self-hostable. Ideal for production clinical environments.

#### When to Use Cloud APIs (GPT-4o / Claude):
Use cloud APIs only for:
- Non-PHI use cases (de-identified research datasets)
- Rapid prototyping under BAA agreement
- Benchmark comparison against self-hosted models

### 4.4 LLM Integration Points

| Module | LLM Role | Ontology Role |
|---|---|---|
| Symptom extraction | Parse free-text → structured symptom IDs | Validate extracted symptoms against ontology vocabulary |
| Differential ranking | N/A | Weighted graph traversal (deterministic) |
| Diagnosis explanation | Generate natural language reasoning narrative | Provide ranked diagnoses + reasoning trace as context |
| Knowledge expansion | Suggest new disease/symptom nodes | Human review before graph ingestion |
| ICD coding | Map diagnosis to ICD-10/11 codes | Anchor to existing coded ontology nodes |
| Patient Q&A | Answer follow-up questions | Ground answers in ontology facts to prevent hallucination |

### 4.5 Safety Architecture (Medical AI Guardrails)

```
┌───────────────────────────────────────────────────────────┐
│                   Safety Layer                            │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Rule 1: LLM output NEVER bypasses ontology engine   │ │
│  │         Ontology is source of truth for diagnoses   │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Rule 2: All diagnoses carry confidence bounds       │ │
│  │         No single disease presented as certain      │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Rule 3: "Consult a physician" disclaimer on output  │ │
│  │         WALLY is decision support, not replacement  │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Rule 4: All LLM calls are logged with input/output  │ │
│  │         Full audit trail for regulatory review      │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Rule 5: PHI never leaves the deployment boundary    │ │
│  │         LLM runs on-premises or in private cloud    │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

---

### 4.6 LLM Scope Boundaries

This section defines explicitly what the LLM layer is — and is not — responsible for. This distinction is critical for clinical safety, regulatory viability, and clinician trust.

#### ✅ LLM IS in scope for:

| Function | Description | Why Safe |
|---|---|---|
| **Symptom extraction** | Parse free-text clinical notes → structured ontology symptom IDs | Output is validated against the ontology vocabulary before use; unrecognized terms are flagged, not silently passed |
| **Explanation generation** | Translate the ontology engine's reasoning trace into readable clinical narrative | LLM only narrates what the ontology engine already concluded — it cannot introduce new diagnoses |
| **Patient Q&A** | Answer follow-up questions about a completed diagnosis | Answers are grounded in ontology-provided disease facts; out-of-scope questions are rejected |
| **Knowledge suggestions** | Propose new disease/symptom nodes for curator review | All suggestions are held in a staging queue; nothing enters the live ontology without human approval |
| **ICD / SNOMED mapping** | Suggest standard codes for ontology concepts | Mapping is advisory; a human or rules-based lookup confirms the final code |
| **Multilingual translation** | Translate UI and symptom terms for non-English patients | Does not affect diagnostic logic, which remains language-agnostic |

#### ❌ LLM is NOT in scope for:

| Function | Why Excluded |
|---|---|
| **Generating a diagnosis** | LLMs hallucinate. A fabricated disease in a clinical context is a patient safety event. The ontology engine is the sole diagnostic authority. |
| **Assigning confidence scores** | Confidence is a mathematical output of the weighted graph traversal — not a language model's estimate |
| **Modifying edge weights** | Symptom-disease weights encode clinical evidence; changes require curator review and versioned audit trail |
| **Writing directly to the ontology** | All ontology writes go through a human-reviewed staging pipeline regardless of source |
| **Overriding a low-confidence result** | If the ontology finds no strong match, the correct output is "insufficient data" — not an LLM guess |
| **Interpreting lab values / imaging** | Out of scope for v2.0; these are distinct modalities requiring separate validation |

#### Architectural Guarantee

```
User Input (text)
      │
      ▼
  LLM Layer          ← only touches: text in, structured symptoms out
      │
      ▼
 Ontology Engine     ← sole source of diagnostic output
      │
      ▼
  LLM Layer          ← only touches: structured results in, narrative out
      │
      ▼
 Clinician / User
```

The LLM sits **around** the diagnostic engine, never **inside** it. The ontology engine can function with zero LLM involvement (current v1.0 does exactly this). The LLM adds usability; the ontology provides correctness.

---

## 5. Future Enhancements Roadmap

### Phase 1 — Ontology Expansion (Months 1–3)
> *Foundation for clinical breadth*

- Expand knowledge base from 7 diseases → 500+ (using ICD-10 disease hierarchy)
- Ingest SNOMED CT and UMLS terminology mappings
- Add rare disease catalog (OMIM/Orphanet integration)
- Age/sex/risk-factor modifiers on symptom weights
- Lab result integration (CBC, metabolic panel → diagnostic signals)

### Phase 2 — LLM Integration Depth (Months 3–6)
> *Natural language front door — foundation already live*

> ✅ **Already deployed**: Free-text symptom extraction via Llama 3.2 (NLP mode), on-prem Ollama, zero API cost

- Upgrade to LLaMA 3.1 (8B or 70B) for improved clinical NLP accuracy
- Clinical note parsing: convert full SOAP notes to ontology-structured input
- Natural language explanation generation from diagnostic reasoning trace
- Voice input via Whisper (speech-to-text → symptom extraction pipeline)
- Multilingual support (Spanish, Mandarin, French patient-facing UI)
- SPARQL query interface for ontology exploration

### Phase 3 — EHR Integration (Months 6–12)
> *Enterprise clinical workflow*

> ✅ **Already in ontology**: ICD-10-CM codes and MeSH references on all disease nodes — EHR mapping foundation is live

- HL7 FHIR R4 API adapter (consume patient records from Epic, Cerner, Athena)
- SMART on FHIR app launch from within EHR
- Bi-directional: read patient history, write diagnostic suggestions back to chart
- CDS Hooks implementation (real-time alerts at order entry)
- DICOM image metadata ingestion (radiology report summarization)

### Phase 4 — Learning & Feedback Loop (Months 9–18)
> *System improves with clinical use*

- Clinician feedback loop: accept / reject / modify diagnostic suggestions
- Reinforcement signal updates edge weights in the ontology graph
- Cohort analytics: population-level disease pattern dashboards
- Rare disease detection: flag low-confidence matches for specialist escalation
- De-identified case library for model benchmarking and continuous evaluation

### Phase 5 — Regulatory & Compliance (Months 12–24)
> *Path to FDA SaMD clearance*

- Software as a Medical Device (SaMD) documentation (IEC 62304, ISO 14971)
- FDA 510(k) or De Novo pathway assessment for Class II clinical decision support
- SOC 2 Type II and HIPAA audit preparation
- Bias audit: demographic parity across age, sex, ethnicity in diagnostic output
- Clinical validation study: prospective cohort (WALLY vs. attending diagnosis)

---

## 6. Competitive Differentiation

| Capability | WALLY | IBM Watson Health (discontinued) | Epic CDS | Generic GPT-4 Wrapper |
|---|---|---|---|---|
| Explainable reasoning trace | ✅ Full | ⚠️ Partial | ⚠️ Rule-based | ❌ Black box |
| Editable knowledge graph | ✅ Live UI | ❌ Vendor-locked | ❌ Vendor-locked | ❌ N/A |
| Self-hosted / HIPAA native | ✅ Yes | ❌ No | ✅ Yes | ❌ BAA required |
| Open ontology standards | ✅ OWL/RDF/SNOMED | ⚠️ Proprietary | ❌ Proprietary | ❌ N/A |
| LLM integration path | ✅ Designed in | ❌ N/A | ❌ Minimal | ✅ Only capability |
| Zero AI API cost | ✅ Yes | ❌ Per-query pricing | ❌ License fees | ❌ Per-token cost |
| Rare disease support | ✅ Graph extensible | ⚠️ Limited | ❌ Not focus | ⚠️ Hallucination risk |

---

## 7. Deployment & Pricing Model

### 7.1 Current Deployment

| Environment | URL | Cost |
|---|---|---|
| Live demo | https://161.35.239.151 | $12/mo DigitalOcean droplet |
| Local dev | http://localhost:5173 | $0 |
| Self-hosted enterprise | Customer infrastructure | $0 infrastructure (open source) |

### 7.2 Commercial Tiers (Proposed)

| Tier | Target | Includes | Price Model |
|---|---|---|---|
| **Open Core** | Researchers, students | Full ontology editor + base reasoner | Free / MIT License |
| **Clinical Pilot** | Small practices (1–10 providers) | LLM integration + 500 diseases + support | $299/mo per site |
| **Enterprise** | Hospitals, health systems | FHIR adapter + EHR integration + SLA | Custom contract |
| **OEM / API** | Health IT vendors | Embeddable API license + white-label | Revenue share |

---

## 8. Technical Risk & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| LLM hallucination of symptoms | High — patient safety | Ontology acts as semantic validator; LLM output always checked against known concept IDs |
| Ontology staleness | Medium — diagnostic accuracy | Versioned graph with audit trail; sync pipeline from SNOMED/ICD updates |
| Regulatory classification | High — market access | Early FDA pre-submission meeting; design for SaMD Predetermined Change Control Plan |
| Model bias (demographic) | High — equity | Bias testing suite built into Phase 4; diverse training/evaluation cohorts |
| HIPAA breach on cloud LLM | Critical | Default to on-prem LLM; cloud APIs only under signed BAA with PHI controls |

---

## 9. Project Timeline

| Date | Milestone |
|---|---|
| Feb 17, 2026 | Fish-eye ontology editor POC |
| Feb 18, 2026 | Production deployment to DigitalOcean |
| Feb 19, 2026 | Interactive MiniMap navigation |
| Feb 20, 2026 | Medical AI Reasoner + Ollama/Llama 3.2 NLP integration deployed |
| Feb 22, 2026 | RDF/Turtle backend: `medical_ontology.ttl`, DOID + ICD-10 + MeSH enrichment live |
| Coming soon | SPARQL interface, search/filter, 1,000+ node scaling tests |

---

## 10. Summary

WALLY is not a prototype — it is a **production system** running today at [https://161.35.239.151](https://161.35.239.151), combining graph-algorithm diagnostic reasoning with a live Llama 3.2 NLP layer. The deterministic ontology core was a deliberate design choice:

1. **Trust first**: Clinicians and regulators need to understand *how* a system reaches a diagnosis before they trust it with patients
2. **Ontology as ground truth**: The knowledge graph is the medical model; LLMs are added as a natural language interface, not as the judge
3. **Privacy by architecture**: Self-hosted from day one means PHI never touches a third-party API
4. **Extensible without retraining**: Adding a new disease is editing a graph node, not retraining a 70B parameter model

The LLM layer is already live — free-text symptom input works today via Llama 3.2 on the same self-hosted droplet. The v2.0 roadmap deepens that integration: clinical note parsing, voice input, FHIR connectivity. But the fundamental architecture is proven and deployed: every diagnosis traces back to a weighted edge in an auditable, editable, standards-compliant RDF ontology enriched with DOID, ICD-10-CM, and MeSH identifiers.

**WALLY is what medical AI should look like: transparent, structured, safe — and open.**

---

*WALLY — Medical Ontology Platform*  
*Contact: [github.com/gpad1234/Startup-One-Wally-Clean](https://github.com/gpad1234/Startup-One-Wally-Clean)*  
*Live Demo: [https://161.35.239.151](https://161.35.239.151)*  
*Documentation: [https://gpad1234.github.io/Startup-One-Wally-Clean/](https://gpad1234.github.io/Startup-One-Wally-Clean/)*
