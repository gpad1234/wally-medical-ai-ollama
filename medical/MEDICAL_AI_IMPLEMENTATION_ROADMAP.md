# Medical AI Agentic Reasoner - Implementation Roadmap

**Version**: 1.0  
**Date**: February 24, 2026  
**Status**: Ready for Implementation  

---

## Executive Summary

This roadmap defines **WHAT** to build, **WHEN** to build it, and **HOW** to organize the work into logical phases with clear deliverables, success criteria, and dependencies.

---

## Project Structure & Organization

### Folder Organization

```
medical-ai-agentic-reasoner/
│
├── src/
│   ├── presentation/          # Layer 1: User-facing interfaces
│   │   ├── controllers/       # Flask route handlers
│   │   │   ├── diagnosis_controller.py
│   │   │   ├── ontology_controller.py
│   │   │   └── system_controller.py
│   │   ├── schemas/           # Request/response validation
│   │   │   ├── diagnosis_schema.py
│   │   │   └── ontology_schema.py
│   │   └── middleware/        # CORS, logging, error handling
│   │       └── error_handler.py
│   │
│   ├── orchestration/         # Layer 2: Agent & reasoning
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── medical_ai_agent.py    # Main orchestrator
│   │   │   ├── agent_state.py         # State management
│   │   │   └── agent_config.py        # Agent configuration
│   │   ├── reasoning/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py              # Reasoning algorithms
│   │   │   ├── symptom_matcher.py     # Symptom matching logic
│   │   │   ├── disease_ranker.py      # Disease ranking
│   │   │   ├── inference_engine.py    # Inference logic
│   │   │   └── explanation_generator.py # Explain reasoning
│   │   └── workflows/
│   │       ├── __init__.py
│   │       ├── diagnosis_workflow.py  # Diagnosis process
│   │       ├── treatment_workflow.py  # Treatment recommendation
│   │       └── explanation_workflow.py # Explanation generation
│   │
│   ├── services/              # Layer 3: Business logic services
│   │   ├── __init__.py
│   │   ├── nlp_service.py              # NLP with Ollama
│   │   ├── ontology_service.py         # Ontology operations
│   │   ├── inference_service.py        # Inference algorithms
│   │   ├── prompt_service.py           # Ollama prompt management
│   │   ├── text_extraction_service.py  # langextract wrapper
│   │   ├── config_service.py           # Configuration management
│   │   └── logging_service.py          # Logging & audit
│   │
│   ├── integrations/          # Layer 4: External API clients
│   │   ├── __init__.py
│   │   ├── ollama_client.py            # Ollama REST API wrapper
│   │   ├── langextract_client.py       # langextract wrapper
│   │   └── health_checker.py           # Service health checks
│   │
│   ├── storage/               # Layer 4: Data persistence
│   │   ├── __init__.py
│   │   ├── ontology_storage.py         # Ontology persistence
│   │   ├── medical_data_store.py       # Session/history storage
│   │   ├── cache_manager.py            # In-memory caching
│   │   └── db_connection.py            # Database connectivity
│   │
│   ├── models/                # Layer 5: Data structures
│   │   ├── __init__.py
│   │   ├── domain_models.py            # Disease, Symptom, Treatment
│   │   ├── diagnosis_result.py         # Diagnosis output
│   │   ├── session_models.py           # Session, PatientHistory
│   │   ├── ontology_models.py          # Ontology structures
│   │   └── reasoning_models.py         # Reasoning chain, step
│   │
│   ├── knowledge/             # Layer 5: Knowledge base
│   │   ├── __init__.py
│   │   ├── medical_ontology.json       # Ontology data
│   │   ├── symptom_keywords.json       # NLP keywords
│   │   ├── treatments.json             # Treatment protocols
│   │   └── inference_rules.json        # Domain rules
│   │
│   ├── utils/                 # Utilities & helpers
│   │   ├── __init__.py
│   │   ├── validators.py               # Data validation
│   │   ├── formatters.py               # Response formatting
│   │   └── constants.py                # Constants & enums
│   │
│   ├── config/                # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py                 # App settings
│   │   ├── ollama_config.py            # Ollama configuration
│   │   └── logging_config.py           # Logging setup
│   │
│   └── app.py                 # Flask application factory
│
├── tests/
│   ├── unit/                  # Unit tests
│   │   ├── test_reasoning_engine.py
│   │   ├── test_nlp_service.py
│   │   ├── test_ontology_service.py
│   │   └── test_inference_service.py
│   ├── integration/           # Integration tests
│   │   ├── test_agent_orchestrator.py
│   │   ├── test_diagnosis_flow.py
│   │   └── test_service_integration.py
│   ├── e2e/                   # End-to-end tests
│   │   ├── test_full_diagnosis.py
│   │   ├── test_naturallanguage_input.py
│   │   └── test_with_ollama.py
│   ├── fixtures/              # Test data
│   │   ├── sample_symptoms.json
│   │   ├── mock_ontology.json
│   │   └── test_cases.json
│   └── conftest.py            # pytest configuration
│
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile                  # App container
│   │   ├── Dockerfile.ollama           # Ollama container
│   │   └── docker-compose.yml          # Orchestration
│   ├── k8s/                   # Kubernetes manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   └── scripts/
│       ├── install_ollama.sh           # Setup script
│       ├── download_models.sh          # Model setup
│       └── health_check.sh             # Health monitoring
│
├── docs/
│   ├── ARCHITECTURE.md                 # (This is the main arch doc)
│   ├── API_REFERENCE.md                # OpenAPI/swagger
│   ├── DEPLOYMENT_GUIDE.md             # Deployment instructions
│   ├── DEVELOPER_GUIDE.md              # Development setup
│   ├── DATABASE_SCHEMA.md              # DB design
│   └── TROUBLESHOOTING.md              # Common issues
│
├── cli/
│   ├── __init__.py
│   ├── medical_ai_cli.py               # CLI entry point
│   └── commands/
│       ├── diagnose.py
│       ├── explain.py
│       ├── models.py
│       └── query.py
│
├── frontend/                  # React dashboard (separate)
│   ├── src/
│   │   ├── components/
│   │   │   ├── DiagnosisForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   ├── ReasoningViewer.jsx
│   │   │   └── TreatmentPanel.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── store/
│   │   │   └── ...
│   │   └── App.jsx
│   └── package.json
│
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation
├── pytest.ini                  # Test configuration
├── .env.example                # Environment variables template
├── .dockerignore
├── .gitignore
└── README.md                   # Project overview
```

---

## Development Phases

### **PHASE 1: Foundation & Setup** (2 weeks)
**Goal**: Establish architecture and core infrastructure

#### 1.1 Environment Setup
- [ ] **Create folder structure** - all dirs and __init__.py files
- [ ] **Setup virtual environment** - Python 3.10+
- [ ] **Update requirements.txt** with new packages:
  - `ollama>=0.1.0` - Ollama Python client
  - `langextract>=0.1.0` - Text extraction
  - `networkx>=3.0` - Graph operations
  - `pytest>=8.0.0` - Testing
  - `python-dotenv>=1.0.0` - Config management
  
- [ ] **Create .env.example** with configuration defaults:
  ```
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_PRIMARY_MODEL=llama3.2:3b
  OLLAMA_REASONING_MODEL=phi3.5
  FLASK_ENV=development
  LOG_LEVEL=INFO
  DATABASE_URL=sqlite:///medical_ai.db
  ```

#### 1.2 Configuration Foundation
**File**: `src/config/settings.py`
- [ ] Define app configuration class
- [ ] Load from environment variables
- [ ] Setup logging configuration
- [ ] Define constants and enums

**File**: `src/config/ollama_config.py`
- [ ] Ollama server URL defaults
- [ ] Model names and configurations
- [ ] Prompt templates
- [ ] Response timeout settings

#### 1.3 Database & Storage
**File**: `src/storage/db_connection.py`
- [ ] Create database connection handler
- [ ] Support SQLite for development, PostgreSQL for production
- [ ] Lazy initialization (only when needed)

**File**: `src/knowledge/medical_ontology.json`
- [ ] Export existing medical ontology from current system
- [ ] Format as JSON with disease hierarchy
- [ ] Include symptom relationships
- [ ] Include treatment mappings

**Deliverable**: Fully functional folder structure with all imports working

---

### **PHASE 2: Ollama Integration** (1-2 weeks)
**Goal**: Integrate local LLM capability

#### 2.1 Ollama Client
**File**: `src/integrations/ollama_client.py`
```python
class OllamaClient:
    def __init__(self, base_url: str)
    def is_healthy() -> bool          # Check if server running
    def list_models() -> List[Model]
    def generate(model, prompt, **kwargs) -> str
    def stream_generate(model, prompt) -> Iterator[str]
    def pull_model(model_name) -> None
    def delete_model(model_name) -> None
```

**Tests**: `tests/unit/test_ollama_client.py`
- [ ] Test health check
- [ ] Test model listing
- [ ] Test generation with mocking
- [ ] Test error handling (server down)
- [ ] Test model management

#### 2.2 Health Checker
**File**: `src/integrations/health_checker.py`
- [ ] Check Ollama server availability
- [ ] Check required models downloaded
- [ ] Check system resources (disk, memory)
- [ ] Provide startup diagnostics

#### 2.3 Ollama Setup Scripts
**File**: `deployment/scripts/install_ollama.sh`
- [ ] Auto-detect OS (macOS, Linux, Windows)
- [ ] Download and install Ollama
- [ ] Start service in background
- [ ] Verify installation

**File**: `deployment/scripts/download_models.sh`
- [ ] Download primary model (llama3.2:3b)
- [ ] Download secondary model (phi3.5)
- [ ] Show download progress
- [ ] Verify integrity

**Deliverable**: Working Ollama client that can communicate with locally-running LLM server

---

### **PHASE 3: Service Layer** (1-2 weeks)
**Goal**: Build core business logic services

#### 3.1 NLP Service
**File**: `src/services/nlp_service.py`
```python
class NLPService:
    def __init__(self, ollama_client, config)
    
    def extract_symptoms(text: str) -> Dict[str, List[str]]
        # Phase 1: keyword matching
        # Phase 2: LLM extraction
        # Phase 3: entity recognition
    
    def classify_intent(text: str) -> str
        # Determine if "diagnose", "explain", "treat", etc.
    
    def extract_entities(text: str) -> Dict[str, Any]
        # Extract symptoms, conditions, medications
    
    def llm_call(prompt: str, model: str = None) -> str
    
    def summarize_diagnosis(diagnosis) -> str
```

**Tests**: `tests/unit/test_nlp_service.py`
- [ ] Keyword matching for common symptoms
- [ ] Intent classification
- [ ] Fallback when Ollama unavailable
- [ ] Error handling

#### 3.2 Ontology Service (Enhanced)
**File**: `src/services/ontology_service.py` (refactored from existing)
```python
class OntologyService:
    def lookup_symptoms(symptoms: List[str]) -> List[Node]
    def lookup_diseases(diseases: List[str]) -> List[Node]
    def get_treatments(disease_id: str) -> List[Treatment]
    def get_disease_hierarchy(disease_id: str) -> Dict
    def get_related_diseases(disease_id: str) -> List[Disease]
    def semantic_similarity(text: str, node: Node) -> float
```

**Tests**: `tests/unit/test_ontology_service.py`
- [ ] Symptom lookup
- [ ] Disease lookup
- [ ] Relationship traversal
- [ ] Hierarchy navigation

#### 3.3 Inference Service
**File**: `src/services/inference_service.py`
```python
class InferenceService:
    def rankBySymptoms(symptoms: List[Symptom]) -> List[ScoreResult]
        # Core diagnosis algorithm
    
    def validateDiagnosis(disease, symptoms) -> float
        # Medical validation rules
    
    def findCoDiseases(disease) -> List[Disease]
        # Find comorbidities
    
    def explainReasoning(diagnosis) -> ReasoningChain
        # Generate step-by-step explanation
```

**Tests**: `tests/unit/test_inference_service.py`
- [ ] Scoring algorithm correctness
- [ ] Confidence calculation
- [ ] Ranking order
- [ ] Edge cases (no matches, ties)

#### 3.4 Prompt Service
**File**: `src/services/prompt_service.py`
```python
class PromptService:
    def build_symptom_extraction_prompt(text) -> str
    def build_explanation_prompt(diagnosis) -> str
    def build_entity_extraction_prompt(text) -> str
    def add_medical_context(prompt, ontology_context) -> str
    def add_patient_history(prompt, history) -> str
```

**Deliverable**: Complete service layer with all business logic operational

---

### **PHASE 4: Agentic Framework** (1-2 weeks)
**Goal**: Build orchestration and reasoning loops

#### 4.1 Domain Models
**File**: `src/models/domain_models.py`
```python
@dataclass
class Symptom:
    id: str
    name: str
    description: str
    severity: str

@dataclass
class Disease:
    id: str
    name: str
    description: str
    severity: str
    symptom_ids: List[str]

@dataclass
class Treatment:
    id: str
    name: str
    type: str  # 'medication', 'procedure', 'lifestyle'
    description: str
```

**File**: `src/models/diagnosis_result.py`
```python
@dataclass
class DiagnosisResult:
    primary_diagnosis: Disease
    confidence_score: float
    alternative_diagnoses: List[Disease]
    treatments: List[Treatment]
    reasoning_chain: List[ReasoningStep]
    warnings: List[str]
```

**File**: `src/models/reasoning_models.py`
```python
@dataclass
class ReasoningStep:
    step_number: int
    description: str
    details: Dict[str, Any]
    duration_ms: float

@dataclass
class ReasoningChain:
    total_steps: int
    steps: List[ReasoningStep]
    total_duration_ms: float
    llm_calls_made: int
```

#### 4.2 Agent Orchestrator
**File**: `src/orchestration/agents/medical_ai_agent.py`
```python
class MedicalAIAgent:
    def __init__(self, nlp_service, ontology_service, 
                 inference_service, prompt_service):
        self.nlp = nlp_service
        self.ontology = ontology_service
        self.inference = inference_service
        self.prompt_service = prompt_service
        self.state = AgentState()
    
    def reason(self, user_input: str) -> DiagnosisResult:
        """Main reasoning loop"""
        # Step 1: Parse input
        # Step 2: Extract symptoms
        # Step 3: Query ontology
        # Step 4: Perform inference
        # Step 5: Generate explanation
        # Step 6: Get treatments
        # Return complete result
```

#### 4.3 Reasoning Engine
**File**: `src/orchestration/reasoning/engine.py`
```python
class ReasoningEngine:
    def rankBySymptoms(symptoms) -> List[Disease]:
        """
        Algorithm:
        1. For each disease, calculate symptom_match_score
        2. Calculate coverage_score (% of symptoms matched)
        3. confidence = match_score * coverage_score
        4. Normalize to 0-100
        5. Return sorted descending
        """
    
    def validateDiagnosis(disease, symptoms) -> ValidationResult:
        """Check medical rules"""
    
    def findCoDiseases(disease) -> List[Disease]:
        """Find related conditions"""
```

**Tests**: `tests/unit/test_reasoning_engine.py`
- [ ] Correct scoring calculation
- [ ] Proper normalization (0-100)
- [ ] Correct ranking order
- [ ] Edge cases

**Tests**: `tests/integration/test_agent_orchestrator.py`
- [ ] Full diagnosis flow
- [ ] State management
- [ ] Service integration
- [ ] Error handling and recovery

**Deliverable**: Complete agentic framework that coordinates all services

---

### **PHASE 5: Text Extraction & langextract** (1 week)
**Goal**: Enable document parsing and entity extraction

#### 5.1 Text Extraction Service
**File**: `src/services/text_extraction_service.py`
```python
class TextExtractionService:
    def __init__(self, langextract_client):
        self.extractor = langextract_client
    
    def extract_structured_data(document: str) -> Dict[str, Any]
        # Extract key-value pairs, tables from documents
    
    def extract_entities(text: str) -> Dict[str, List[str]]
        # Extract medical entities: symptoms, drugs, procedures
    
    def extract_sections(document: str) -> Dict[str, str]
        # Extract: Diagnosis, Treatment, History, etc.
    
    def parse_clinical_notes(notes: str) -> ClinicalData
        # Convert unstructured notes to structured form
```

#### 5.2 Langextract Client Wrapper
**File**: `src/integrations/langextract_client.py`
```python
class LangExtractClient:
    def extract(document: str, extraction_type: str) -> Dict
        # Wrapper around langextract library
    
    def supported_formats() -> List[str]
        # JSON, markdown, plain text, etc.
```

#### 5.3 Clinical Parser
**File**: `src/orchestration/agents/clinical_parser.py`
- [ ] Parse clinical notes
- [ ] Link entities to ontology
- [ ] Extract structured data
- [ ] Validate extracted information

**Tests**: `tests/unit/test_text_extraction.py`
- [ ] Entity extraction accuracy
- [ ] Section extraction
- [ ] Format handling

**Deliverable**: Complete document parsing and entity extraction

---

### **PHASE 6: API Layer & Controllers** (1 week)
**Goal**: Build HTTP endpoints

#### 6.1 Controllers
**File**: `src/presentation/controllers/diagnosis_controller.py`
```python
@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    # GET user_input
    # CALL agent.reason(user_input)
    # RETURN DiagnosisResult as JSON

@app.route('/api/natural-language', methods=['POST'])
def natural_language_input():
    # Handle free-form text input
    # Extract symptoms via NLP
    # Run diagnosis

@app.route('/api/explain', methods=['POST'])
def explain_diagnosis():
    # Explain reasoning chain

@app.route('/api/symptoms', methods=['GET'])
def list_symptoms():
    # Return available symptoms

@app.route('/api/diseases', methods=['GET'])
def list_diseases():
    # Return available diseases
```

**File**: `src/presentation/controllers/ontology_controller.py`
```python
@app.route('/api/ontology/diseases', methods=['GET'])
def get_diseases():
    # List diseases with filtering

@app.route('/api/ontology/symptoms', methods=['GET'])
def get_symptoms():
    # List symptoms with filtering

@app.route('/api/ontology/search', methods=['POST'])
def search_ontology():
    # Full-text search on ontology
```

**File**: `src/presentation/controllers/system_controller.py`
```python
@app.route('/api/health', methods=['GET'])
def health_check():
    # Check system status
    # Verify Ollama connection
    # Check ontology loaded

@app.route('/api/models', methods=['GET'])
def list_models():
    # List downloaded LLM models

@app.route('/api/config', methods=['GET'])
def get_config():
    # Return system configuration
```

#### 6.2 Request/Response Schemas
**File**: `src/presentation/schemas/diagnosis_schema.py`
- [ ] Request validation
- [ ] Response serialization
- [ ] Error response format

**Tests**: `tests/integration/test_diagnosis_flow.py`
- [ ] Full diagnosis API flow
- [ ] Response validation
- [ ] Error handling

**Deliverable**: Complete REST API for all features

---

### **PHASE 7: Testing & Quality** (1 week)
**Goal**: Comprehensive test coverage

#### 7.1 Unit Tests
- [ ] Reasoning algorithms
- [ ] Service functions
- [ ] Utility functions
- [ ] Model validation

**Target**: >80% code coverage

#### 7.2 Integration Tests
- [ ] Service interactions
- [ ] Agent orchestration
- [ ] Database operations
- [ ] Cache functionality

#### 7.3 End-to-End Tests
- [ ] Full diagnosis flow (symptom → diagnosis → treatment)
- [ ] Natural language processing
- [ ] Document parsing
- [ ] API endpoints

#### 7.4 Ollama Integration Tests
- [ ] Test with real Ollama server
- [ ] Test model switching
- [ ] Test streaming responses
- [ ] Test error cases

**Deliverable**: Comprehensive test suite with >80% coverage

---

### **PHASE 8: Documentation & Deployment** (1 week)
**Goal**: Complete documentation and deployment setup

#### 8.1 API Documentation
- [ ] OpenAPI/Swagger spec
- [ ] Endpoint examples
- [ ] Error codes
- [ ] Authentication (if needed)

#### 8.2 Developer Guide
- [ ] Setup instructions
- [ ] Architecture walkthrough
- [ ] Adding new services
- [ ] Debugging guide

#### 8.3 Deployment
- [ ] Docker Dockerfile
- [ ] docker-compose.yml
- [ ] Kubernetes manifests (optional)
- [ ] Deployment guide

#### 8.4 Monitoring & Logging
- [ ] Structured logging
- [ ] Performance metrics
- [ ] Error tracking
- [ ] Health monitoring

**Deliverable**: Production-ready deployment package

---

## Implementation Checklist

### Core Files to Create

**Phase 1 - Foundation**
- [ ] `src/config/settings.py`
- [ ] `src/config/ollama_config.py`
- [ ] `src/storage/db_connection.py`
- [ ] `src/knowledge/medical_ontology.json`
- [ ] `.env.example`
- [ ] Updated `requirements.txt`

**Phase 2 - Ollama**
- [ ] `src/integrations/ollama_client.py`
- [ ] `src/integrations/health_checker.py`
- [ ] `deployment/scripts/install_ollama.sh`
- [ ] `deployment/scripts/download_models.sh`

**Phase 3 - Services**
- [ ] `src/services/nlp_service.py`
- [ ] `src/services/ontology_service.py` (refactor)
- [ ] `src/services/inference_service.py`
- [ ] `src/services/prompt_service.py`

**Phase 4 - Agent**
- [ ] `src/models/domain_models.py`
- [ ] `src/models/diagnosis_result.py`
- [ ] `src/orchestration/agents/medical_ai_agent.py`
- [ ] `src/orchestration/reasoning/engine.py`

**Phase 5 - Text Extraction**
- [ ] `src/services/text_extraction_service.py`
- [ ] `src/integrations/langextract_client.py`

**Phase 6 - API**
- [ ] `src/presentation/controllers/diagnosis_controller.py`
- [ ] `src/presentation/controllers/ontology_controller.py`
- [ ] `src/presentation/schemas/diagnosis_schema.py`

**Phase 7 - Tests**
- [ ] Multiple test files in `tests/`

**Phase 8 - Documentation**
- [ ] `API_REFERENCE.md`
- [ ] `DEVELOPER_GUIDE.md`
- [ ] `DEPLOYMENT_GUIDE.md`

### Refactoring Existing Code
- [ ] Move `ontology_api.py` routes → controllers
- [ ] Extract service logic → services layer
- [ ] Refactor `graph_db.py` → storage layer
- [ ] Consolidate configuration → config module

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| 1: Foundation | 1 week | Folder structure, config, DB |
| 2: Ollama | 1 week | LLM client, model tools |
| 3: Services | 1.5 weeks | Core business logic |
| 4: Agent | 1.5 weeks | Orchestrator, reasoning loops |
| 5: Text Extract | 1 week | Document parsing |
| 6: API | 1 week | REST endpoints |
| 7: Testing | 1 week | Test suite |
| 8: Deployment | 1 week | Docker, docs |
| **Total** | **~9-10 weeks** | **Production-ready system** |

---

## Success Criteria per Phase

### Phase 1 ✅
- [ ] All folders created with proper __init__.py
- [ ] All imports working
- [ ] Configuration system operational
- [ ] Database connection working

### Phase 2 ✅
- [ ] Ollama client communicates with server
- [ ] Model listing works
- [ ] Health check operational
- [ ] Installation scripts functional

### Phase 3 ✅
- [ ] All services instantiate without error
- [ ] NLP service extracts symptoms
- [ ] Ontology service queries correctly
- [ ] Inference service ranks diseases

### Phase 4 ✅
- [ ] Agent orchestrator runs full diagnosis
- [ ] Reasoning chain generates properly
- [ ] State management works
- [ ] Multiple diagnoses rank correctly

### Phase 5 ✅
- [ ] Text extraction works on documents
- [ ] Entity extraction identifies medical terms
- [ ] Section parsing works
- [ ] langextract integrated

### Phase 6 ✅
- [ ] All API endpoints operational
- [ ] Request validation works
- [ ] Response formatting correct
- [ ] Error handling functional

### Phase 7 ✅
- [ ] >80% test coverage
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] E2E tests with real Ollama pass

### Phase 8 ✅
- [ ] Dockerfile runs cleanly
- [ ] docker-compose orchestrates all services
- [ ] Documentation complete
- [ ] Deployment guide tested

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Ollama installation fails | Medium | High | Pre-built Docker image, fallback keyword matching |
| LLM response slow | Medium | Medium | Response caching, timeout handling, fast model option |
| Ontology too large | Low | Medium | Lazy loading, in-memory caching, pagination |
| Service dependencies break | Low | Medium | Dependency injection, interface contracts |
| Test environment differs from prod | Medium | Low | Dockerization, consistent environment setup |

---

## Dependencies & Prerequisites

- Python 3.10+
- Ollama (downloaded separately or via Docker)
- PostgreSQL or SQLite
- Modern browser (for React dashboard)
- 4GB+ free disk space (for LLM models)

