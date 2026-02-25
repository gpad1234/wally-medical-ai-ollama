# Enhanced Medical AI Reasoner Specification

**Version**: 2.1
**Date**: February 24, 2026
**Status**: Active Design — Sprint 1 architecture + longer-term roadmap
**Extends**: MEDICAL_AI_AGENTIC_ARCHITECTURE.md, MEDICAL_AI_REASONER.md

---

## Quick Navigation

- [1. Foundation](#1-foundation)
- [2. Near-Term Design & Architecture (Sprint 1)](#2-near-term-design--architecture-sprint-1)
  - [2.1 What We're Building](#21-what-were-building)
  - [2.2 Updated System Architecture](#22-updated-system-architecture)
  - [2.3 New Components](#23-new-components)
  - [2.4 Request Flow](#24-request-flow)
  - [2.5 Implementation Plan](#25-implementation-plan)
- [3. Longer-Term Goals (Roadmap)](#3-longer-term-goals-roadmap)

---

## 1. Foundation

Ollama enables local, private, and secure medical reasoning by running specialized, open-source large language models (LLMs) on personal hardware or private servers. It is used to analyze patient-reported symptoms, aid in differential diagnosis, process clinical notes, and de-identify protected health information (PHI) without sending sensitive data to the cloud.

**Commonly Used Models:**

| Model | Best For |
|---|---|
| Meditron | Diagnostic support, medical exam questions |
| MedGemma | Medical text reasoning, differential diagnosis |
| Mistral / Llama 3 | PHI de-identification, summarization |
| DeepSeek-R1 | Complex multi-step clinical reasoning |

**AI Doctor Research Baseline** (multi-model ensemble):
- Combines Meditron, MedLLaMA2, WizardLM2, and Mistral via prompt filtering
- Federated learning across institutions preserves privacy
- Outperforms individual models on BLEU score, inference speed, and consistency
- Provides the design target for our longer-term ensemble architecture

---

## 2. Near-Term Design & Architecture (Sprint 1)

### 2.1 What We're Building

Sprint 1 adds three capabilities to the existing agentic architecture with no new infrastructure — only new service files on top of the already-working `graph_service`, `ontology_service`, and Flask API:

| # | Capability | Why Now |
|---|---|---|
| A | **Graph-RAG** — ground every LLM call in the ontology | Eliminates hallucination; uses existing graph_service |
| B | **Structured JSON output** — Pydantic schema + Ollama format mode | Makes the API reliable; 1 file change |
| C | **Streaming responses** — SSE endpoint for chain-of-thought UI | Massive UX improvement; uses existing Flask |
| D | **Safety guard** — post-generation validation against ontology | Clinical safety; blocks bad output at the boundary |

Together these four form a **grounded, safe, structured reasoning pipeline** that replaces the current free-text LLM response pattern.

---

### 2.2 Updated System Architecture

The four Sprint 1 changes are highlighted with `[NEW]` below. Everything else is unchanged from MEDICAL_AI_AGENTIC_ARCHITECTURE.md.

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                          │
│         (Web UI, CLI, Medical Dashboard, API Clients)           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  - POST /api/diagnose          (batch, structured JSON)         │
│  - GET  /api/diagnose/stream   [NEW] (SSE streaming)            │
│  - POST /api/feedback          (clinician corrections)          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│               ORCHESTRATION & AGENTIC LAYER                     │
│  Agent Orchestrator  ->  Reasoning Engine                       │
│                           |                                     │
│              [NEW] Graph-RAG context injection                  │
│              (query ontology BEFORE calling LLM)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      SERVICE LAYER                              │
│  ┌──────────────┬────────────────┬────────────┬──────────────┐  │
│  │ NLP Service  │ Ontology Svc   │ Inference  │ Prompt Svc   │  │
│  │ (Ollama)     │ (existing)     │ Service    │ (existing)   │  │
│  └──────────────┴────────────────┴────────────┴──────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ [NEW] graph_rag_service.py   — build grounded context      │  │
│  │ [NEW] diagnosis_schema.py    — Pydantic output contract    │  │
│  │ [NEW] safety_guard.py        — post-gen validation         │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  DATA & INTEGRATION LAYER                       │
│  Ollama Client  |  graph_db / ontology storage  |  Audit logs  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                     KNOWLEDGE BASE LAYER                        │
│  Medical Ontology (disease taxonomy, symptom weights, rules)    │
│  LLM Models: Meditron / MedGemma / DeepSeek-R1 via Ollama       │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.3 New Components

#### A. `src/services/graph_rag_service.py` — Grounded Context Builder

Queries the ontology graph before every LLM call and formats the results as a structured system prompt, anchoring all model output to verified knowledge.

```python
class GraphRAGService:
    def __init__(self, graph_service, ontology_service):
        self.graph = graph_service
        self.ontology = ontology_service

    def build_context(self, symptoms: list[str]) -> str:
        """Build a grounded system prompt from ontology nodes."""
        nodes = self.graph.query_symptom_nodes(symptoms)
        chain = self.ontology.get_inheritance_chain(nodes)
        weights = self.graph.get_symptom_weights(symptoms)

        return GROUNDED_CONTEXT_TEMPLATE.format(
            condition_nodes=self._format_nodes(nodes),
            symptom_weights=self._format_weights(weights),
            inheritance_chain=self._format_chain(chain),
        )

GROUNDED_CONTEXT_TEMPLATE = """
You are a medical reasoning assistant. Base all diagnoses ONLY on the following
verified conditions from our knowledge base:

Relevant conditions:
{condition_nodes}

Symptom-disease weights for the reported symptoms:
{symptom_weights}

Disease hierarchy:
{inheritance_chain}

Do not reference any condition not listed above.
"""
```

#### B. `src/services/diagnosis_schema.py` — Structured Output Contract

Enforces a machine-readable response shape from every LLM call using Pydantic + Ollama's `format="json"`.

```python
from pydantic import BaseModel
from typing import List, Optional

class ReasoningStep(BaseModel):
    step_number: int
    description: str
    evidence: List[str]

class DiagnosisResult(BaseModel):
    conditions: List[str]            # Must match ontology node IDs
    icd_codes: List[str]
    confidence_score: float          # 0.0 – 1.0
    severity: str                    # "mild" | "moderate" | "severe" | "critical"
    reasoning_steps: List[ReasoningStep]
    recommended_treatments: List[str]
    requires_escalation: bool
    escalation_reason: Optional[str] = None

class DiagnosisResponse(BaseModel):
    status: str
    diagnosis: DiagnosisResult
    model_used: str
    inference_time_ms: int
```

**Ollama call pattern** (in NLPService / agent):
```python
response = ollama.chat(
    model=selected_model,
    messages=[
        {"role": "system", "content": rag_service.build_context(symptoms)},
        {"role": "user",   "content": user_input},
    ],
    format="json",
    options={"temperature": 0.1},
)
result = DiagnosisResponse.model_validate_json(response["message"]["content"])
```

#### C. `src/presentation/controllers/stream_controller.py` — SSE Streaming Endpoint

Streams DeepSeek-R1's chain-of-thought to the UI token-by-token. Separates `<think>` blocks (internal reasoning trace) from the final answer.

```python
from flask import Response, stream_with_context
import json

def stream_diagnosis(messages):
    """Server-Sent Events endpoint: GET /api/diagnose/stream"""
    def generate():
        reasoning_buffer = []
        in_think_block = False

        for chunk in ollama.chat(model="deepseek-r1", messages=messages, stream=True):
            token = chunk["message"]["content"]

            if "<think>" in token:
                in_think_block = True
            elif "</think>" in token:
                in_think_block = False
                yield f"data: {json.dumps({'type': 'reasoning', 'content': ''.join(reasoning_buffer)})}\n\n"
                reasoning_buffer = []
            elif in_think_block:
                reasoning_buffer.append(token)
                yield f"data: {json.dumps({'type': 'thinking', 'token': token})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'answer', 'token': token})}\n\n"

        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")
```

**UI contract**: The frontend listens for three event types:
- `thinking` — display in collapsible "Reasoning Trace" panel
- `reasoning` — complete reasoning block (on `</think>`)
- `answer` — stream into the main result card

#### D. `src/services/safety_guard.py` — Post-Generation Validation

Runs after every LLM response, before returning to the user. Blocks output that references unknown conditions or unapproved treatments.

```python
class SafetyGuard:
    def validate(self, result: DiagnosisResult) -> SafetyReport:
        issues = []

        for condition in result.conditions:
            if not self.ontology.node_exists(condition):
                issues.append(SafetyIssue(
                    severity="critical",
                    message=f"'{condition}' not in knowledge base",
                    field="conditions",
                ))

        for treatment in result.recommended_treatments:
            if not self.formulary.is_approved(treatment):
                issues.append(SafetyIssue(
                    severity="high",
                    message=f"'{treatment}' not in approved formulary",
                    field="recommended_treatments",
                ))

        return SafetyReport(
            passed=not any(i.severity == "critical" for i in issues),
            issues=issues,
            validated_result=result if not issues else None,
        )
```

---

### 2.4 Request Flow

**Batch diagnosis (POST /api/diagnose)**:
```
Request
  -> DiagnosisController.handle_diagnosis()
  -> GraphRAGService.build_context(symptoms)       # query ontology
  -> NLPService.llm_call(grounded_prompt)          # call Ollama with format="json"
  -> DiagnosisResponse.model_validate_json(...)    # parse & validate schema
  -> SafetyGuard.validate(result)                  # check against ontology + formulary
  -> return validated JSON
```

**Streaming diagnosis (GET /api/diagnose/stream)**:
```
Request
  -> GraphRAGService.build_context(symptoms)       # query ontology
  -> ollama.chat(..., stream=True)                 # streaming tokens
  -> StreamController.generate()                  # split <think> vs answer tokens
  -> SSE stream to frontend
```

---

### 2.5 Implementation Plan

**Sprint 1 deliverables** (no new infrastructure required):

| Step | File | Description |
|---|---|---|
| 1 | `src/services/diagnosis_schema.py` | Create Pydantic output schema |
| 2 | `src/services/graph_rag_service.py` | Build grounded context from ontology |
| 3 | `src/services/safety_guard.py` | Post-generation validation |
| 4 | `src/presentation/controllers/stream_controller.py` | SSE streaming endpoint |
| 5 | `src/services/nlp_service.py` | Update `llm_call()` to use `format="json"` + RAG context |
| 6 | `ontology_api.py` | Register `/api/diagnose/stream` route |
| 7 | Tests | Unit tests for schema, RAG context builder, safety guard |

**Definition of done**: `POST /api/diagnose` returns a validated `DiagnosisResponse`, `GET /api/diagnose/stream` streams tokens with reasoning/answer split, and `SafetyGuard` rejects any condition not in the ontology.

---

## 3. Longer-Term Goals (Roadmap)

The following capabilities are valuable but require more design, infrastructure, or clinical process changes. They are documented here for future sprints.

---

### Goal 1: Intelligent Model Routing

Route each query to the right model based on complexity instead of always calling the same model.

```
simple_lookup  (1-2 symptoms)   -> meditron
differential   (3-5 symptoms)   -> medgemma
complex        (>5, rare flags) -> deepseek-r1
phi_deidentify                  -> llama3
summarization                   -> mistral
```

**File**: `src/services/model_router.py`
**Dependency**: Stable schema from Sprint 1 must be in place first.

---

### Goal 2: PHI De-identification Two-Pass Pipeline

HIPAA-compliant processing of real clinical notes via a two-pass local pipeline.

```
Pass 1: raw_note -> llama3 (de-id prompt) -> anonymized_note + phi_token_map
Pass 2: anonymized_note -> reasoning_model -> DiagnosisResult
Post:   re-inject phi_token_map for clinician view only (never logged)
```

**Dependency**: Requires audit log design and data retention policy decisions before implementation.

---

### Goal 3: Confidence Calibration via Ensemble Voting

Run 2–3 models in parallel on the same input and aggregate results. Model disagreement becomes a first-class "low confidence / escalate" signal.

```python
async def ensemble_diagnose(symptoms):
    results = await asyncio.gather(
        run_model("meditron", symptoms),
        run_model("medgemma", symptoms),
        run_model("deepseek-r1", symptoms),
    )
    agreement_ratio = vote_count / len(results)
    return EnsembleResult(
        ensemble_confidence=avg_confidence * agreement_ratio,
        requires_escalation=(agreement_ratio < 0.5),
    )
```

**File**: `src/services/ensemble_service.py`
**Dependency**: Model routing (Goal 1) + sufficient GPU/RAM for parallel inference.

---

### Goal 4: Ontology-Traced Explainability

Extend the response to include the specific ontology edges that drove the diagnosis, bridging LLM output and the knowledge graph for clinician trust.

```json
{
  "ontology_evidence": [
    {"symptom": "fever",    "weight": 0.9, "edge": "fever -> Influenza"},
    {"symptom": "myalgia",  "weight": 0.8, "edge": "myalgia -> Influenza"}
  ],
  "hierarchy_context": {
    "parent_class": "Viral Respiratory Infection",
    "icd_category": "J09-J18"
  },
  "alternative_conditions_considered": ["Common Cold (0.52)", "COVID-19 (0.44)"]
}
```

**Dependency**: Graph-RAG (Sprint 1, item A) must be working; this extends its output.

---

### Goal 5: Agentic Tool Use (Function Calling)

Give the reasoning model the ability to call tools mid-inference — looking up ICD codes, checking drug interactions, querying patient history, or escalating to a clinician autonomously.

```python
MEDICAL_TOOLS = [
    {"name": "lookup_icd_code",      ...},
    {"name": "check_drug_interaction",...},
    {"name": "query_patient_history", ...},
    {"name": "escalate_to_clinician", ...},
]

def reason_with_tools(input):
    while True:
        response = ollama.chat(model=model, messages=messages, tools=MEDICAL_TOOLS)
        if response.get("tool_calls"):
            for call in response["tool_calls"]:
                messages.append({"role": "tool", "content": dispatch(call)})
        else:
            return DiagnosisResult.model_validate_json(response["message"]["content"])
```

**Dependency**: Requires Ollama version with stable tool-call support + full test coverage of every tool function.

---

### Goal 6: Temporal & Longitudinal Reasoning

Store all encounters as timestamped nodes in the graph DB and build a structured clinical timeline prompt, enabling progression-aware diagnosis across visits.

```
Patient Node
  -> HAS_ENCOUNTER -> Encounter Node (timestamp, symptoms[], vitals{})
        -> RESULTED_IN -> Diagnosis Node (condition, confidence, verified)
```

**Timeline prompt**: "3 weeks ago: fever + cough; today: dyspnea + SpO2 89%" enables the model to distinguish a resolving cold from developing pneumonia.

**Dependency**: Graph DB schema extension + patient identity design + HIPAA review.

---

### Goal 7: Clinician Feedback Loop & Active Learning

A feedback endpoint (`POST /api/feedback`) lets clinicians mark diagnoses as confirmed or incorrect. Results drive ontology edge weight recalibration and surface model drift in `qc_dashboard.py`.

```
clinician submits correction
  -> add_validation_edge(encounter_id, suggested, verified)
  -> if feedback_count >= THRESHOLD: recalibrate_symptom_weights()
  -> qc_dashboard: model_agreement_rate, top misclassifications, weight_drift_chart
```

**Dependency**: Temporal reasoning schema (Goal 6) + defined recalibration policy.

---

### Roadmap Summary

| Goal | Description | Sprint Target |
|---|---|---|
| 1 | Model Routing | Sprint 2 |
| 2 | PHI De-id Pipeline | Sprint 2 |
| 3 | Ensemble Voting | Sprint 3 |
| 4 | Ontology Explainability | Sprint 2 |
| 5 | Agentic Tool Use | Sprint 4 |
| 6 | Temporal Reasoning | Sprint 4 |
| 7 | Feedback Loop | Sprint 5 |
