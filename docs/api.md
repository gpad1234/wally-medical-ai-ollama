---
layout: default
title: API Reference
---

# API Reference

All endpoints are served by the Flask backend on **port 5002**.  
The React UI proxies `/api/*` → `http://localhost:5002` via Vite.

---

## Health & Status

### `GET /api/ontology/health`

Returns service health and Ollama availability.

**Request**

```http
GET http://localhost:5002/api/ontology/health
```

**Response `200 OK`**

```json
{
  "status": "healthy",
  "service": "Ontology API",
  "ollama_available": true,
  "ontology_loaded": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always `"healthy"` if Flask is running |
| `ollama_available` | boolean | Whether Ollama responds at `localhost:11434` |
| `ontology_loaded` | boolean | Whether `medical_ontology.ttl` loaded successfully |

---

## Ontology Data

### `GET /api/ontology/medical`

Returns the full medical knowledge graph — diseases, symptoms, and treatments — parsed from `medical_ontology.ttl`.

**Request**

```http
GET http://localhost:5002/api/ontology/medical
```

**Response `200 OK`**

```json
{
  "diseases": [
    {
      "id": "Influenza",
      "label": "Influenza",
      "symptoms": ["Fever", "Cough", "Fatigue", "Headache"],
      "treatments": ["Rest", "Antiviral Medication", "Hydration"],
      "confidence_base": 0.85
    }
  ],
  "symptoms": [
    { "id": "Fever", "label": "Fever" },
    { "id": "Cough", "label": "Cough" }
  ],
  "treatments": [
    { "id": "Rest", "label": "Rest" }
  ],
  "stats": {
    "diseases": 7,
    "symptoms": 20,
    "treatments": 14
  }
}
```

**Ontology contents**

| Category | Count |
|----------|-------|
| Diseases | 7 |
| Symptoms | 20 |
| Treatments | 14 |

Diseases modelled: Influenza, Common Cold, Pneumonia, Hypertension, Diabetes, Migraine, Asthma.

---

## Diagnosis (LLM)

### `POST /api/diagnose`

The core Sprint 1 endpoint — takes a list of symptom strings, builds an ontology-grounded prompt, and asks `llama3.2:3b` via Ollama.

**Request**

```http
POST http://localhost:5002/api/diagnose
Content-Type: application/json
```

```json
{
  "symptoms": ["Fever", "Cough", "Fatigue"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symptoms` | array of strings | ✅ | Human-readable symptom labels (see `/api/ontology/medical` for valid values) |

**Response `200 OK`**

```json
{
  "diagnosis": "Based on the symptoms and the provided medical ontology, the most likely diagnoses are:\n\n1. **Influenza** (85% match) ...",
  "reasoning": "The patient presents with fever, cough, and fatigue. Cross-referencing the ontology ...",
  "model_used": "llama3.2:3b",
  "symptoms_received": ["Fever", "Cough", "Fatigue"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `diagnosis` | string | LLM-generated diagnosis with confidence estimates |
| `reasoning` | string | LLM reasoning chain referencing ontology data |
| `model_used` | string | Ollama model name (e.g. `llama3.2:3b`) |
| `symptoms_received` | array | Echo of the input symptoms |

**Response `503 Service Unavailable`** (Ollama not running)

```json
{
  "error": "Ollama LLM service is not available. Please ensure Ollama is running: ollama serve",
  "hint": "Run: ollama serve && ollama pull llama3.2:3b"
}
```

**Response `400 Bad Request`** (missing symptoms)

```json
{
  "error": "No symptoms provided. Please send a JSON body with a 'symptoms' array."
}
```

---

## How `/api/diagnose` Works

```
1. Load medical_ontology.ttl with rdflib (cached)
2. Extract all disease→symptom→treatment triples
3. Build SYSTEM prompt:
   "You are a medical diagnostic assistant. Use only this ontology:
    Diseases: Influenza (symptoms: Fever, Cough…)…"
4. Build USER prompt:
   "Patient symptoms: Fever, Cough, Fatigue.
    Which diseases match? Explain with confidence."
5. Call ollama.chat(model='llama3.2:3b', messages=[system, user])
6. Return structured JSON
```

---

## curl Examples

**Health check**

```bash
curl http://localhost:5002/api/ontology/health
```

**Get all diseases**

```bash
curl http://localhost:5002/api/ontology/medical | python3 -m json.tool | head -40
```

**Ask for diagnosis**

```bash
curl -s -X POST http://localhost:5002/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["Chest Pain", "Shortness of Breath", "Fatigue"]}' \
  | python3 -m json.tool
```

**Python example**

```python
import requests, json

resp = requests.post(
    "http://localhost:5002/api/diagnose",
    json={"symptoms": ["Fever", "Runny Nose", "Sore Throat"]}
)
data = resp.json()
print(data["diagnosis"])
print(f"\nModel: {data['model_used']}")
```

---

## Valid Symptom Labels

Use these exact strings in the `symptoms` array (case-sensitive):

| Symptom | Symptom | Symptom |
|---------|---------|---------|
| Fever | Cough | Fatigue |
| Headache | Sore Throat | Runny Nose |
| Shortness of Breath | Chest Pain | Nausea |
| Vomiting | Diarrhea | Muscle Aches |
| Joint Pain | Dizziness | Blurred Vision |
| Increased Thirst | Frequent Urination | High Blood Pressure |
| Wheezing | Sneezing | — |

> Tip: call `GET /api/ontology/medical` at runtime to get the current authoritative list.

---

[← Getting Started](getting-started) | [Home →](./)
