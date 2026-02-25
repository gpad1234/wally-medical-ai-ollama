# Medical AI Agentic Reasoner - Architecture & Design
**Version**: 1.0  
**Date**: February 24, 2026  
**Status**: Architecture Definition  
**Type**: Agentic AI System (Local Ollama + Medical Ontology)  
**Cost**: $0 (Free & Open Source)

---

## Executive Summary

The **Medical AI Agentic Reasoner** is a layered, modular system that combines:
- **Local LLMs** (Ollama) for natural language understanding
- **Medical Ontology** (structured knowledge graph) for domain reasoning  
- **Agentic Framework** (orchestration loops) for intelligent decision-making
- **Text Extraction** (langextract) for clinical data parsing

This creates a reasoning system that:
1. **Understands** natural language input (symptoms, medical history)
2. **Reasons** over structural knowledge (ontology-based inference)
3. **Decides** intelligently (agentic logic with feedback loops)
4. **Acts** by providing diagnoses, treatment recommendations, and explanations

**Key Architecture Principle**: Organized in **Layers → Services → Components** to reduce complexity and enable independent testing/development.

---

## 1. System Architecture Overview

### 1.1 Layered Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                                 │
│         (Web UI, CLI, Medical Dashboard, API Clients)               │
└──────────────────────┬──────────────────────────────────────────────┘
                       │
┌───────────────────────▼──────────────────────────────────────────────┐
│                   PRESENTATION LAYER                                 │
│  - Request routing                                                   │
│  - Response formatting (JSON, HTML, etc.)                            │
│  - Error handling & validation at boundary                           │
│  - API Controllers (Flask routes)                                    │
└───────────────────────┬──────────────────────────────────────────────┘
                       │
┌───────────────────────▼────────────────────────────────────────────┐
│               ORCHESTRATION & AGENTIC LAYER                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Agent Orchestrator                                          │  │
│  │  - Manages reasoning loops                                  │  │
│  │  - Routes between services                                  │  │
│  │  - Handles agent decision-making                            │  │
│  │  - Tracks conversation state                                │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                       ↓                                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Reasoning Engine                                            │  │
│  │  - Symptom analysis logic                                   │  │
│  │  - Confidence calculation                                   │  │
│  │  - Treatment recommendation logic                           │  │
│  │  - Multi-step reasoning chains                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────────────────┐
│                    SERVICE LAYER                                   │
│  ┌─────────────────┬──────────────┬───────────┬────────────────┐  │
│  │ NLP Service     │ Ontology     │ Inference │ Prompt Service │  │
│  │ (Ollama client) │ Service      │ Service   │ (Ollama setup) │  │
│  │ - Symptom       │ - Class CRUD │ - Pattern │ - Prompt       │  │
│  │   extraction    │ - Property   │   matching│   templates    │  │
│  │ - Text          │   CRUD       │ - Ranking │ - Context      │  │
│  │   understanding │ - Instance   │ - Scoring │   building     │  │
│  │ - Intent        │   CRUD       │           │                │  │
│  │   recognition   │ - Graph      │           │                │  │
│  │ - Entity        │   traversal  │           │                │  │
│  │   extraction    │              │           │                │  │
│  └─────────────────┴──────────────┴───────────┴────────────────┘  │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Support Services                                             │ │
│  │  - Text Extraction Service (langextract wrapper)             │ │
│  │  - Logging & Audit Service                                   │ │
│  │  - Config Management Service                                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────────────────┐
│                    DATA & INTEGRATION LAYER                        │
│  ┌──────────────────┬──────────────────┬──────────────────────┐   │
│  │ Ollama Client    │ Ontology Storage │ Clinical Data Store  │   │
│  │ - REST API calls │ - Graph DB       │ - Patient history    │   │
│  │ - Model mgmt     │ - In-memory      │ - Session state      │   │
│  │ - Streaming      │   cache          │ - Audit logs         │   │
│  │ - Error handling │ - Persistence    │                      │   │
│  └──────────────────┴──────────────────┴──────────────────────┘   │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ External Integrations                                        │ │
│  │  - Ollama HTTP Server (localhost:11434)                      │ │
│  │  - langextract Python library                                │ │
│  │  - Database (SQLite/PostgreSQL for persistence)              │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────────────────┐
│                   KNOWLEDGE BASE LAYER                             │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Medical Ontology (Semantic Knowledge Graph)                 │ │
│  │  ├── Disease Taxonomy (ICD-style hierarchy)                  │ │
│  │  ├── Symptom Definitions (clinical descriptors)              │ │
│  │  ├── Treatment Protocols (evidence-based)                    │ │
│  │  ├── Symptom-Disease Relationships (weighted)                │ │
│  │  └── Inference Rules (domain logic)                          │ │
│  │                                                              │ │
│  │ LLM Models (Ollama backend)                                 │ │
│  │  ├── Primary: Llama 3.2 (3B) or Phi-3.5 (3.8B)              │ │
│  │  ├── Fallback: Mistral (7B) for complex reasoning            │ │
│  │  └── Fine-tuning: Medical domain adaptation (optional)       │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

### 1.2 Layer Responsibilities

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| **Presentation** | User interaction, request/response | HTTP routes, CLI, Web UI |
| **Orchestration** | Agent logic, reasoning loops, state | Agent coordinator, reasoning engine |
| **Services** | Business logic, domain operations | NLP, Ontology, Inference |
| **Data/Integration** | Storage, external APIs, persistence | DB, Ollama client, cache |
| **Knowledge Base** | Structured knowledge, LLM models | Ontology, medical rules, LLMs |

---

## 2. Component Details

### 2.1 Presentation Layer

#### 2.1.1 Flask API Server (`ontology_api.py`)
**Endpoints:**
- `POST /api/diagnose` - Submit symptoms, get diagnosis
- `POST /api/explain` - Explain reasoning chain
- `POST /api/treatment` - Get treatment recommendations
- `GET /api/symptoms` - List available symptoms
- `GET /api/diseases` - List available diseases
- `POST /api/natural-language` - Process free-form text input

**Response Format:**
```json
{
  "status": "success",
  "data": { ... },
  "reasoning": {
    "steps": [
      {"step": 1, "description": "Symptom extraction", "details": {...}},
      {"step": 2, "description": "Pattern matching", "details": {...}},
      {"step": 3, "description": "Ranking", "details": {...}},
      {"step": 4, "description": "Treatment lookup", "details": {...}}
    ],
    "llm_calls": [
      {"model": "llama3.2", "prompt": "...", "response": "..."}
    ]
  },
  "metadata": {
    "execution_time_ms": 245,
    "llm_model_used": "llama3.2:3b",
    "confidence_score": 0.87
  }
}
```

#### 2.1.2 CLI Client (`medical_ai_cli.py`)
**Commands:**
```bash
$ medical-ai diagnose --symptoms "fever, cough, fatigue"
$ medical-ai explain --condition "pneumonia"
$ medical-ai natural-text "I have a severe headache and light sensitivity"
$ medical-ai models list
$ medical-ai models pull llama3.2:3b
```

#### 2.1.3 Web Dashboard
- React-based UI showing diagnosis results
- Symptom selector with multi-select
- Reasoning visualization
- Treatment recommendations display

---

### 2.2 Orchestration & Agentic Layer

#### 2.2.1 Agent Orchestrator (`agents/orchestrator.py`)
**Purpose:** Coordinates the entire reasoning pipeline

```python
class MedicalAIAgent:
    """Main agentic orchestrator for medical reasoning"""
    
    def __init__(self, nlp_service, ontology_service, inference_service):
        self.nlp = nlp_service
        self.ontology = ontology_service
        self.inference = inference_service
        self.state = {}
    
    def reason(self, user_input: str) -> DiagnosisResult:
        """
        Main reasoning loop:
        1. Parse natural language input
        2. Extract symptoms and entities
        3. Query ontology
        4. Perform inference
        5. Generate explanation
        """
        # Step 1: NLP processing
        parsed = self.nlp.extract_symptoms(user_input)
        
        # Step 2: Ontology query
        symptom_nodes = self.ontology.lookup_symptoms(parsed['symptoms'])
        
        # Step 3: Inference
        diseases = self.inference.rankBySymptoms(symptom_nodes)
        
        # Step 4: Enrich with treatment
        treatments = self.ontology.get_treatments(diseases[0]['id'])
        
        # Step 5: Generate explanation
        explanation = self._generate_explanation(diseases, treatments)
        
        return DiagnosisResult(diseases, treatments, explanation)
    
    def _generate_explanation(self, diseases, treatments) -> str:
        """Generate human-readable explanation using LLM"""
        prompt = f"Explain why {diseases[0]} is the top diagnosis..."
        return self.nlp.llm_call(prompt)
```

#### 2.2.2 Reasoning Engine (`reasoning/engine.py`)
**Algorithms:**
- **Symptom Matching**: Weighted scoring algorithm
- **Disease Ranking**: Confidence calculation with normalization
- **Inference**: Recursive ontology traversal
- **Treatment Mapping**: Evidence-based protocol lookup

**Key Method:**
```python
def rankBySymptoms(self, symptoms: List[str]) -> List[Disease]:
    """
    Rank diseases by symptom match strength
    
    Algorithm:
    1. For each disease D in ontology:
       - symptom_match_score = Sum(weight * match) / total_weight
       - coverage_score = matched_count / total_required
       - confidence = symptom_match_score * coverage_score
    2. Normalize scores (0-100)
    3. Return sorted by confidence descending
    """
```

---

### 2.3 Service Layer

#### 2.3.1 NLP Service (`services/nlp_service.py`)
**Wraps Ollama client and specialized NLP functions**

```python
class NLPService:
    """Natural Language Processing integration with Ollama"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
        self.symptom_keywords = { ... }  # domain-specific keywords
    
    def extract_symptoms(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical symptoms from free-form text
        
        Uses:
        1. Keyword matching (fast path)
        2. LLM classification (accurate path)
        3. Named entity recognition (context path)
        """
    
    def classify_intent(self, text: str) -> str:
        """Determine user intent: 'diagnose', 'explain', 'treat', etc."""
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract medical entities: symptoms, conditions, medications"""
    
    def llm_call(self, prompt: str, model: str = None) -> str:
        """Call Ollama LLM with prompt"""
    
    def summarize_diagnosis(self, diagnosis: DiagnosisResult) -> str:
        """Generate natural language summary of diagnosis"""
```

#### 2.3.2 Ontology Service (`services/ontology_service.py`)
**Already exists - Enhanced for agentic reasoning**

```python
class OntologyService:
    """Medical ontology operations"""
    
    def lookup_symptoms(self, symptom_names: List[str]) -> List[Node]:
        """Find symptom nodes in ontology"""
    
    def lookup_diseases(self, disease_names: List[str]) -> List[Node]:
        """Find disease nodes in ontology"""
    
    def get_treatments(self, disease_id: str) -> List[Treatment]:
        """Get treatments for a disease"""
    
    def get_disease_hierarchy(self, disease_id: str) -> Dict:
        """Get parent-child relationships"""
    
    def semantic_similarity(self, text: str, node: Node) -> float:
        """Calculate similarity between text and ontology node"""
```

#### 2.3.3 Inference Service (`services/inference_service.py`)
**Core reasoning algorithms**

```python
class InferenceService:
    """Implement diagnosis reasoning over ontology"""
    
    def rankBySymptoms(self, symptoms: List[Symptom]) -> List[ScoreResult]:
        """Weighted scoring algorithm for diseases"""
    
    def validateDiagnosis(self, disease: Disease, symptoms: List[Symptom]) -> float:
        """Validate diagnosis against medical rules"""
    
    def explainReasoning(self, diagnosis: DiagnosisResult) -> ReasoningChain:
        """Generate step-by-step explanation"""
    
    def findCoDiseases(self, disease: Disease) -> List[Disease]:
        """Find potential comorbidities"""
```

#### 2.3.4 Text Extraction Service (`services/text_extraction_service.py`)
**Wraps langextract library**

```python
class TextExtractionService:
    """Extract clinical information from medical documents"""
    
    def extract_structured_data(self, document: str) -> Dict[str, Any]:
        """Extract key-value pairs, tables, lists from medical text"""
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities: drugs, symptoms, procedures"""
    
    def extract_sections(self, document: str) -> Dict[str, str]:
        """Extract sections: Diagnosis, Treatment, History, etc."""
    
    def parse_clinical_notes(self, notes: str) -> ClinicalData:
        """Parse unstructured clinical notes into structured form"""
```

#### 2.3.5 Prompt Service (`services/prompt_service.py`)
**Manages Ollama prompts and context**

```python
class PromptService:
    """Construct and manage LLM prompts"""
    
    def build_symptom_extraction_prompt(self, text: str) -> str:
        """Build prompt for symptom extraction"""
    
    def build_diagnosis_explanation_prompt(self, diagnosis: DiagnosisResult) -> str:
        """Build prompt to explain diagnosis"""
    
    def build_treatment_recommendation_prompt(self, disease: Disease) -> str:
        """Build prompt for treatment recommendations"""
    
    def add_medical_context(self, prompt: str) -> str:
        """Augment prompt with ontology context"""
    
    def add_patient_history(self, prompt: str, history: PatientHistory) -> str:
        """Add patient-specific context to prompt"""
```

---

### 2.4 Data & Integration Layer

#### 2.4.1 Ollama Client (`integrations/ollama_client.py`)
**Wrapper around Ollama HTTP API**

```python
class OllamaClient:
    """Client for Ollama local LLM server"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> str:
        """Generate text from prompt"""
    
    def list_models(self) -> List[Model]:
        """List available downloaded models"""
    
    def pull_model(self, model_name: str) -> None:
        """Download a new model"""
    
    def delete_model(self, model_name: str) -> None:
        """Remove a model"""
    
    def get_model_info(self, model_name: str) -> ModelInfo:
        """Get info about a specific model"""
    
    def is_healthy(self) -> bool:
        """Check if Ollama server is running"""
    
    def stream_generate(self, model: str, prompt: str) -> Iterator[str]:
        """Stream generation response"""
```

#### 2.4.2 Ontology Storage (`storage/ontology_storage.py`)
**Graph database wrapper**

```python
class OntologyStorage:
    """Persist and retrieve ontology from GraphDB"""
    
    def save_ontology(self, ontology: Ontology) -> None:
        """Save to persistent storage"""
    
    def load_ontology(self) -> Ontology:
        """Load from persistent storage"""
    
    def get_node(self, node_id: str) -> Node:
        """Retrieve node by ID"""
    
    def search_nodes(self, query: str) -> List[Node]:
        """Search nodes by text"""
```

#### 2.4.3 Medical Data Store (`storage/medical_data_store.py`)
**Patient sessions, history, audit logs**

```python
class MedicalDataStore:
    """Store clinical data and session state"""
    
    def save_session(self, session: Session) -> str:
        """Save a diagnosis session"""
    
    def get_session(self, session_id: str) -> Session:
        """Retrieve a session"""
    
    def save_patient_history(self, patient_id: str, history: PatientHistory) -> None:
        """Save patient medical history"""
    
    def get_patient_history(self, patient_id: str) -> PatientHistory:
        """Retrieve patient history"""
```

---

### 2.5 Knowledge Base Layer

#### 2.5.1 Medical Ontology Structure

**Taxonomy:**
```
MedicalEntity (root)
├── Disease
│   ├── RespiratoryDisease
│   │   ├── Pneumonia
│   │   ├── Bronchitis
│   │   └── Influenza
│   ├── GastrointestinalDisease
│   │   ├── Gastroenteritis
│   │   └── [others]
│   └── [more categories]
├── Symptom
│   ├── Respiratory
│   │   ├── Cough
│   │   ├── ShortnessOfBreath
│   │   └── [more]
│   └── Systemic
│       ├── Fever
│       ├── Fatigue
│       └── [more]
└── Treatment
    ├── Medication
    ├── Procedure
    └── [more]
```

**Relationships:**
- `has_symptom`: Disease → Symptom (weighted by frequency/importance)
- `treated_by`: Disease → Treatment
- `symptom_severity`: Symptom → Severity level
- `contraindication`: Treatment → Disease (avoid combinations)

**Storage:**
- JSON representation (in-memory for speed)
- GraphDB for persistence
- SQLite/PostgreSQL for sessions and history

#### 2.5.2 LLM Models in Ollama

**Recommended Models:**

| Model | Size | Download | Speed | Quality | Use Case |
|-------|------|----------|-------|---------|----------|
| **Llama 3.2 (3B)** | 2GB | 5 min | ⚡⚡⚡ | ⭐⭐⭐ | Fast symptom extraction, entity recognition |
| **Phi-3.5** | 2.3GB | 5 min | ⚡⚡⚡ | ⭐⭐⭐⭐ | Balanced: good quality, reasonable speed |
| **Mistral (7B)** | 4.1GB | 10 min | ⚡⚡ | ⭐⭐⭐⭐⭐ | Complex reasoning, detailed explanations |
| **Neural Chat (7B)** | 4GB | 10 min | ⚡⚡ | ⭐⭐⭐⭐ | Conversational interface |

**Default Strategy:**
```python
# Primary model for fast operations
PRIMARY_MODEL = "llama3.2:3b"  # 3GB, ~50ms response

# Secondary model for complex reasoning
REASONING_MODEL = "phi3.5"  # 2.3GB, ~80ms response

# Fallback model for detailed analysis
DETAILED_MODEL = "mistral:7b"  # 4GB, ~200ms response
```

---

## 3. Data Flow Examples

### 3.1 Diagnosis Flow

```
User Input: "I have fever, cough, and fatigue"
    ↓
[Presentation] POST /api/diagnose
    ↓
[Controller] Route to Agent
    ↓
[Agent Orchestrator] reason()
    ├─ Step 1: Parse input
    │  └→ NLPService.extract_symptoms()
    │     └→ OllamaClient.generate() - "Extract symptoms from text"
    ├─ Step 2: Lookup ontology
    │  └→ OntologyService.lookup_symptoms(['fever', 'cough', 'fatigue'])
    ├─ Step 3: Inference
    │  └→ InferenceService.rankBySymptoms()
    │     └→ algorithm: weighted scoring
    ├─ Step 4: Get treatments
    │  └→ OntologyService.get_treatments('resp:Pneumonia')
    └─ Step 5: Generate explanation
       └→ NLPService.llm_call() - "Explain the diagnosis"
    ↓
[Result] Return DiagnosisResult with:
- diagnosis: Pneumonia (87% confidence)
- treatments: [Antibiotics, Supportive care, Rest]
- explanation: "The combination of fever, cough, and fatigue..."
- reasoning_chain: [step1, step2, step3, step4, step5]
```

### 3.2 Natural Language Understanding Flow

```
User Input: "I feel really sick - my head hurts, I can't see the light, and loud noises bother me"
    ↓
[NLP Service] extract_symptoms()
    ├─ Keyword matching (fast): matches 'headache'
    ├─ LLM classification (accurate): calls Ollama
    │  Prompt: "List medical symptoms mentioned in: '...'"
    │  Response: "[severe headache, photophobia, sound sensitivity]"
    └─ Entity extraction: extracts severity ('really', 'can't')
    ↓
Result: {
  'symptoms': ['severe_headache', 'photophobia', 'sound_sensitivity'],
  'severity': 'high',
  'confidence': 0.92
}
    ↓
[Ontology] Lookup matched symptoms
    ↓
[Inference] Rank diseases
    → Top result: Migraine (94% confidence)
```

### 3.3 Clinical Document Processing Flow

```
Input: Clinical notes (unstructured text)
    ↓
[TextExtractionService] parse_clinical_notes()
    ├─ Extract sections: Diagnosis, Treatment, History
    ├─ Call langextract: extract structured data
    └─ Return ClinicalData object
    ↓
[Ontology Service] Link to known diseases/treatments
    ↓
[Agent] Incorporate into reasoning
    ↓
[Database] Store in MedicalDataStore
```

---

## 4. Technology Stack

### 4.1 Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | Python Flask | 3.0+ | API server |
| LLM Integration | Ollama REST API | Latest | Local LLMs |
| Text Extraction | langextract | Latest | Document parsing |
| Ontology Storage | NetworkX / GraphDB | Latest | Graph operations |
| Database | SQLite / PostgreSQL | Latest | Persistence |
| NLP | NLTK / spaCy | Latest | Text utilities |
| Testing | pytest | 8.0+ | Unit/integration tests |

### 4.2 Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React 18+ | UI rendering |
| State Mgmt | Redux / Context API | State management |
| HTTP Client | axios / fetch API | API communication |
| Visualization | D3.js / Cytoscape.js | Graph rendering |
| UI Components | Material-UI / custom CSS | Responsive design |

### 4.3 Infrastructure

| Component | Purpose |
|-----------|---------|
| Ollama Server | Local LLM engine |
| PostgreSQL / SQLite | Data persistence |
| Docker | Containerization |
| Docker Compose | Multi-service orchestration |

---

## 5. Development Phases

### Phase 1: Foundation (Week 1-2)
- [x] Architecture definition (this document)
- [ ] Ollama setup & client development
- [ ] Refactor existing services into layered structure
- [ ] Integrate langextract library
- [ ] Create base agentic framework

### Phase 2: Core Agent (Week 3-4)
- [ ] Agent orchestrator implementation
- [ ] Reasoning engine with ontology integration
- [ ] NLP service with Ollama
- [ ] Text extraction service
- [ ] Prompt templates and management

### Phase 3: Integration (Week 5-6)
- [ ] Connect all layers
- [ ] End-to-end diagnosis flow
- [ ] Explanation generation
- [ ] Treatment recommendations
- [ ] Error handling and fallbacks

### Phase 4: Enhancement (Week 7-8)
- [ ] Medical context augmentation
- [ ] Patient history tracking
- [ ] Conversational interface
- [ ] Reasoning visualization
- [ ] Performance optimization

### Phase 5: Deployment (Week 9+)
- [ ] Docker containerization
- [ ] Docker Compose orchestration
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Monitoring and logging
- [ ] Scaling strategies

---

## 6. Key Design Patterns

### 6.1 Separation of Concerns
- Each service handles ONE domain (NLP, Ontology, Inference)
- Layering prevents cross-layer dependencies
- Services communicate via well-defined interfaces

### 6.2 Dependency Injection
- Services receive dependencies (Ollama client, etc.)
- Enables testing with mock objects
- Loose coupling between components

### 6.3 Caching Strategy
- Ontology: Loaded in memory at startup
- Symptom keywords: In-memory dictionary
- LLM responses: Cache recent calls (optional)
- Session data: Persistent storage

### 6.4 Error Handling
- Graceful fallbacks (if Ollama unavailable, use keyword matching)
- Clear error messages with context
- Logging for debugging
- Retry logic for transient failures

### 6.5 Testing Strategy
- Unit tests for algorithms (inference, scoring)
- Integration tests for service orchestration
- Mock Ollama client for offline testing
- End-to-end tests on real ontology

---

## 7. Next Steps

1. **Review & Validate** this architecture with stakeholders
2. **Create detailed component specifications** for each service
3. **Set up project structure** with proper folder organization
4. **Implement services sequentially** (bottom-up: Data → Services → Orchestration)
5. **Build agentic loop** with proper reasoning chains
6. **Integrate Ollama** with fallback mechanisms
7. **Wire langextract** for clinical document parsing
8. **End-to-end testing** on real medical scenarios

---

## 8. Success Criteria

The system is successful when:
- ✅ Can process natural language input (symptoms, descriptions)
- ✅ Correctly diagnoses common conditions using ontology + inference
- ✅ Provides confidence scores and explanations
- ✅ Recommends treatments based on diagnosis
- ✅ Uses local LLMs (no API costs)
- ✅ Handles medical documents (clinical notes, prescriptions)
- ✅ Scales to 100+ diseases and 200+ symptoms
- ✅ Responds in <500ms for typical queries
- ✅ Works offline after Ollama download
- ✅ Maintains audit trail of all diagnoses

