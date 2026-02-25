# WALLY — QA Test & Use Case Specification
## Medical AI Reasoner

**Version**: 1.1  
**Date**: February 24, 2026  
**Scope**: 🏥 Medical AI Reasoner tab only  
**Out of Scope**: Fish-Eye Graph tab, Ontology Editor tab (disabled)

---

## System Architecture (In Scope)

```
Browser (React: MedicalDiagnosisAI.jsx)
    │
    ├─► GET /api/ontology/medical   ← Flask (ontology_api.py, port 5002)
    │       └─ Parses sample_data/medical_ontology.ttl
    │       └─ Falls back to built-in JS FALLBACK_ONTOLOGY if API unreachable
    │
    └─► Reasoning Engine (client-side JS)
            ├─ Weighted symptom-to-disease scoring
            ├─ Score normalization & ranking (top 3)
            └─ Ontology inheritance chain traversal
```

**Knowledge Base (medical_ontology.ttl)**

| Category | Count |
|----------|-------|
| Diseases | 7 |
| Symptoms | 20 |
| Treatments | 14 |
| Hierarchy nodes | 6 |

---

## Knowledge Base Reference

### Diseases

| ID | Label | Severity | Key Symptoms |
|----|-------|----------|--------------|
| `resp:CommonCold` | Common Cold | mild | Runny Nose, Sore Throat, Cough, Sneezing, Fatigue |
| `resp:Influenza` | Influenza (Flu) | moderate | Fever, Cough, Fatigue, Body Aches, Headache, Sore Throat |
| `resp:Pneumonia` | Pneumonia | severe | Fever, Cough, Chest Pain, Shortness of Breath, Fatigue |
| `resp:Bronchitis` | Acute Bronchitis | moderate | Cough, Mucus, Chest Discomfort, Fatigue, Sore Throat |
| `gi:Gastroenteritis` | Gastroenteritis | moderate | Nausea, Vomiting, Diarrhea, Abdominal Pain, Fever |
| `neuro:Migraine` | Migraine | moderate | Severe Headache, Nausea, Light Sensitivity, Sound Sensitivity |
| `cardio:Hypertension` | Hypertension | moderate | Headache, Dizziness, Chest Pain |

### Symptom-to-Disease Weights (key values)

| Symptom | Highest-weighted disease | Weight |
|---------|--------------------------|--------|
| Sneezing | Common Cold | 0.90 |
| Runny Nose | Common Cold | 0.95 |
| Body Aches | Influenza | 0.90 |
| Shortness of Breath | Pneumonia | 0.85 |
| Mucus Production | Bronchitis | 0.85 |
| Diarrhea | Gastroenteritis | 0.90 |
| Severe Headache | Migraine | 0.95 |
| Dizziness | Hypertension | 0.70 |

---

## Test Cases

### TC-LOAD: Ontology Loading

| ID | Test | Steps | Expected |
|----|------|-------|----------|
| TC-LOAD-001 | API loads ontology | Flask running → open Medical AI tab | Header shows `Knowledge source: api`, 7 diseases · 20 symptoms · 14 treatments |
| TC-LOAD-002 | Fallback when API down | Stop Flask → open Medical AI tab | Console warn logged, built-in ontology used, UI fully functional |
| TC-LOAD-003 | Symptom grid populated | Load page | 20 symptom chips rendered, all unselected |
| TC-LOAD-004 | Counts in header | Load page | Header shows `7 diseases · 20 symptoms · 14 treatments` |

---

### TC-SYMP: Symptom Selection

| ID | Test | Steps | Expected |
|----|------|-------|----------|
| TC-SYMP-001 | Select single symptom | Click "Fever" chip | Chip highlighted with ✓, counter shows "1 symptom selected" |
| TC-SYMP-002 | Deselect symptom | Click highlighted "Fever" again | Chip unselected, counter shows "0 symptoms selected" |
| TC-SYMP-003 | Select multiple | Click "Fever", "Cough", "Fatigue" | 3 chips highlighted, counter shows "3 symptoms selected" |
| TC-SYMP-004 | Analyze disabled when empty | Load page, no selection | "Analyze Symptoms" button disabled |
| TC-SYMP-005 | Clear All | Select 3 symptoms, click "Clear All" | All chips unselected, results panel removed |
| TC-SYMP-006 | Clear All disabled when empty | Load page | "Clear All" button disabled |

---

### TC-REASON: Reasoning Engine

| ID | Test | Symptoms to Select | Expected Top Diagnosis |
|----|------|--------------------|------------------------|
| TC-REASON-001 | Cold signature | Runny Nose, Sneezing, Sore Throat | #1: Common Cold |
| TC-REASON-002 | Flu signature | Fever, Body Aches, Cough, Headache | #1: Influenza |
| TC-REASON-003 | Pneumonia signature | Fever, Shortness of Breath, Chest Pain | #1: Pneumonia |
| TC-REASON-004 | Bronchitis signature | Cough, Mucus Production, Chest Discomfort | #1: Acute Bronchitis |
| TC-REASON-005 | GI signature | Nausea, Vomiting, Diarrhea, Abdominal Pain | #1: Gastroenteritis |
| TC-REASON-006 | Migraine signature | Severe Headache, Light Sensitivity, Sound Sensitivity | #1: Migraine |
| TC-REASON-007 | Ambiguous single symptom | Headache only | Multiple candidates, Hypertension or Migraine in top 3 |
| TC-REASON-008 | Returns top 3 | Fever, Cough, Fatigue | 3 diagnosis cards returned |
| TC-REASON-009 | Confidence is numeric | Any run | Confidence shown as `XX.X%`, value 0–100 |
| TC-REASON-010 | Confidence ordered | Any multi-result run | Card #1 confidence ≥ Card #2 ≥ Card #3 |

---

### TC-DISPLAY: Results Display

| ID | Test | Steps | Expected |
|----|------|-------|----------|
| TC-DISP-001 | 4 reasoning steps | Run any diagnosis | Steps: "Symptom Analysis", "Pattern Matching", "Ontology Reasoning", "Confidence Calculation" |
| TC-DISP-002 | Step 1 counts symptoms | Run with 3 symptoms | Step 1 says "Analyzed 3 reported symptoms..." |
| TC-DISP-003 | Matched symptom count | Flu signature | Each card shows "Matched Symptoms: X / Y" |
| TC-DISP-004 | Severity SEVERE | Pneumonia diagnosed | Badge shows `SEVERE` |
| TC-DISP-005 | Severity MILD | Common Cold diagnosed | Badge shows `MILD` |
| TC-DISP-006 | Treatments listed | Any diagnosis | Treatment list with type labels (general / medication / prescription / urgent) |
| TC-DISP-007 | Urgent treatment | Pneumonia #1 | "Hospital Admission" and "Oxygen Therapy" labelled `urgent` |
| TC-DISP-008 | Ontology chain on #1 only | Any run | Only card #1 shows inheritance chain |
| TC-DISP-009 | Chain absent on #2/#3 | Any run | Cards #2 and #3 have no inheritance chain section |
| TC-DISP-010 | Spinner on analyze | Click "Analyze Symptoms" | Spinner + "AI is reasoning..." shown during 1.5s delay |
| TC-DISP-011 | No results panel on load | Fresh page | Results panel not rendered until first Analyze |
| TC-DISP-012 | Reset clears results | Run → Clear All | Results panel disappears |

---

### TC-API: Flask API Endpoints (Verified ✅)

| ID | Endpoint | Method | Expected | Verified |
|----|----------|--------|----------|---------|
| TC-API-001 | `/api/ontology/health` | GET | 200, `{"status": "healthy"}` | ✅ |
| TC-API-002 | `/api/ontology/medical` | GET | 200, 7 diseases | ✅ |
| TC-API-003 | `/api/ontology/medical` | GET | 20 symptoms | ✅ |
| TC-API-004 | `/api/ontology/medical` | GET | All symptoms have `weights` map | ✅ |
| TC-API-005 | `/api/ontology/medical/graph` | GET | 200, 5 classes + 49 instances | ✅ |
| TC-API-006 | `/api/ontology/medical` with `.ttl` missing | GET | 404, error message | ⬜ Not yet run |
| TC-API-007 | Any endpoint from browser | GET | `Access-Control-Allow-Origin` header present | ⬜ Not yet run |

---

### TC-FALLBACK: Offline / Degraded Mode

| ID | Test | Steps | Expected |
|----|------|-------|----------|
| TC-FALL-001 | Full UI works offline | Stop Flask; open tab | All symptoms visible, diagnosis runs |
| TC-FALL-002 | Source label changes | Flask down | Header shows `built-in` as source |
| TC-FALL-003 | No console errors | Flask down, run diagnosis | Only a `warn` — no uncaught errors |
| TC-FALL-004 | Hot-reconnect | Start Flask → refresh | Source switches back to `api` |

---

### TC-EDGE: Edge Cases

| ID | Test | Steps | Expected |
|----|------|-------|----------|
| TC-EDGE-001 | All 20 symptoms | Click all → Analyze | Runs without crash, top 3 returned |
| TC-EDGE-002 | Rapid re-run | Run → clear → different symptoms → run | Second result replaces first cleanly |
| TC-EDGE-003 | Disclaimer visible | Open tab | `⚠️ Educational demonstration only...` always shown |

---

## Manual Test Scenarios (End-to-End)

### Scenario A: Flu Symptoms

1. Open `http://localhost:5177`, click **🏥 Medical AI Reasoner** tab
2. Verify: `7 diseases · 20 symptoms · 14 treatments`
3. Select: **Fever**, **Cough**, **Fatigue**, **Body Aches**, **Headache**
4. Click **Analyze Symptoms** → observe spinner ~1.5s
5. **Expected:**
   - 4 reasoning steps, Step 1 says "Analyzed 5 reported symptoms"
   - #1: **Influenza (Flu)**, highest confidence, severity MODERATE
   - Treatments include "Antiviral Medications"
   - Ontology chain on card #1: `Disease → Respiratory Infection → Viral Respiratory Infection → Influenza (Flu)`
   - Cards #2 and #3 have no chain

---

### Scenario B: Pneumonia (Severe)

1. Select: **Fever**, **Shortness of Breath**, **Chest Pain**, **Fatigue**
2. Click **Analyze Symptoms**
3. **Expected:** #1 Pneumonia, severity `SEVERE`, treatments include "Hospital Admission" (urgent), "Oxygen Therapy" (urgent)

---

### Scenario C: GI Case

1. Select: **Nausea**, **Vomiting**, **Diarrhea**, **Abdominal Pain**
2. Click **Analyze Symptoms**
3. **Expected:** #1 Gastroenteritis, no respiratory diseases in top 3

---

### Scenario D: Fallback Mode

1. Kill Flask: `pkill -f ontology_api`
2. Refresh browser, click Medical AI tab
3. **Expected:** Warn in console, header shows `built-in`, full diagnosis still works

---

## Automated Test Baseline

```
97 passed, 0 failed — 0.18s
(tests/unit/ covering C core, adapter, ontology inheritance, graph service)
```

Run with:
```bash
source .venv/bin/activate && python -m pytest tests/ -v
```

---

## Priority 1 — Flask API Tests to Implement

```
tests/unit/test_api/
└── test_medical_api.py
    ├── test_health_endpoint()            → TC-API-001
    ├── test_medical_ontology_loads()     → TC-API-002/003
    ├── test_symptom_weights_present()    → TC-API-004
    ├── test_medical_graph_structure()    → TC-API-005
    └── test_missing_ttl_returns_404()    → TC-API-006
```
