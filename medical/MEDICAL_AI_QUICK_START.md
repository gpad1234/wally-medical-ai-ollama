# Medical AI Agentic Reasoner - Quick Start Guide

**Version**: 1.0  
**Date**: February 24, 2026  
**Status**: Ready to Begin Implementation  

---

## What You're Building

A **medical diagnostic AI system** that:

```
User Input (natural language)
         ↓
    NLP Service (with Ollama LLM)
    ├─ Extract symptoms from free text
    ├─ Understand medical terminology
    └─ Classify user intent
         ↓
   Agent Orchestrator
    ├─ Query medical ontology
    ├─ Run inference algorithm
    └─ Rank diseases by confidence
         ↓
    Reasoner Engine
    ├─ Weighted symptom matching
    ├─ Coverage scoring
    └─ Explanation generation
         ↓
Output: Diagnosis + Treatment + Explanation
```

**Key Innovation**: Uses **local LLMs** (Ollama) + **medical ontology** + **agentic reasoning** for explainable, offline-capable diagnosis system.

---

## Architecture at a Glance

### 5 Layers (from bottom to top)

| Layer | Purpose | Examples |
|-------|---------|----------|
| **Knowledge Base** | Structured medical knowledge | Ontology, LLM models, rules |
| **Data & Integration** | External APIs, persistence | Ollama client, database, cache |
| **Services** | Business logic | NLP, Inference, Ontology ops |
| **Orchestration** | Reasoning loops, decisions | Agent, reasoning engine |
| **Presentation** | User interfaces | REST API, CLI, Web UI |

---

## What You Have Right Now

✅ **Existing Assets**:
- Medical ontology structure (diseases, symptoms, treatments)
- Graph database implementation (graph_db.py)
- Ontology API server (ontology_api.py)
- Ontology editor (web UI)
- Medical AI design docs

❌ **What's Missing**:
- Ollama integration
- Agentic orchestration framework
- Unified NLP service
- langextract integration
- Reasoning engine
- Proper layering/separation of concerns

---

## 3-Step Implementation Plan

### ✅ **DONE: Architecture Foundation** (What you just got)

**Created Documents**:
1. **MEDICAL_AI_AGENTIC_ARCHITECTURE.md** - Complete system design with all layers and components
2. **MEDICAL_AI_IMPLEMENTATION_ROADMAP.md** - Detailed 8-phase plan with folder structure and checklist
3. **MEDICAL_AI_IMPLEMENTATION_GUIDE.md** - Code patterns and Python examples

**Key Decisions Baked In**:
- Layered architecture (5 layers)
- Separation of concerns (each service = one responsibility)
- Dependency injection (loose coupling)
- Graceful degradation (fallbacks when Ollama unavailable)
- Caching strategy (speed optimization)
- Testing approach (unit → integration → e2e)

---

### 🔥 **NEXT: Phase 1 - Foundation** (This Week)

**Goal**: Establish infrastructure foundation

**What to Do**:
1. Create folder structure from roadmap
2. Setup Python environment and requirements.txt
3. Create configuration system (.env, settings.py)
4. Setup database connection
5. Export medical ontology to JSON

**Time**: ~3-5 days
**Solo/Pair**: Perfect for one developer

**Success**: All imports work, app can start (even if just prints config).

---

### 🚀 **AFTER: Phases 2-8** (Following Weeks)

**Phase 2**: Ollama integration (1 week)
**Phase 3**: Service layer (1-2 weeks)
**Phase 4**: Agentic framework (1-2 weeks)
**Phase 5**: Text extraction (1 week)
**Phase 6**: REST API (1 week)
**Phase 7**: Testing (1 week)
**Phase 8**: Deployment (1 week)

---

## How to Get Started RIGHT NOW

### Option 1: Start Today (Recommended)

**Create the folder structure:**

```bash
# From project root
mkdir -p src/{presentation,orchestration,services,integrations,storage,models,knowledge,utils,config}
mkdir -p tests/{unit,integration,e2e,fixtures}
mkdir -p deployment/{docker,k8s,scripts}
mkdir -p docs cli frontend

# Create __init__ files
find src -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;

# Create placeholder files
touch src/app.py src/config/__init__.py src/config/settings.py
```

**Update requirements.txt** with new dependencies:
```
flask>=3.0.0
flask-cors>=4.0.0
python-dotenv>=1.0.0
ollama>=0.1.0
langextract>=0.1.0
networkx>=3.0.0
pytest>=8.0.0
pytest-cov>=4.1.0
rdflib>=6.0.0
requests>=2.31.0
pydantic>=2.0.0
```

**Create .env.example**:
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_PRIMARY_MODEL=llama3.2:3b
OLLAMA_REASONING_MODEL=phi3.5
FLASK_ENV=development
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///medical_ai.db
```

**That's it!** You now have the infrastructure to start Phase 1.

---

### Option 2: Read First, Then Code

1. Read **MEDICAL_AI_AGENTIC_ARCHITECTURE.md** (20 min)
   - Understand the 5 layers
   - See the data flow examples
   - Understand why this design matters

2. Read **MEDICAL_AI_IMPLEMENTATION_ROADMAP.md** (15 min)
   - See the folder structure
   - Understand the 8 phases
   - Review the checklist

3. Skim **MEDICAL_AI_IMPLEMENTATION_GUIDE.md** (15 min)
   - See code patterns for your language
   - Understand testing strategy
   - Get error handling ideas

4. Start Phase 1 framework

---

## Key Design Principles (Remember These!)

### 1. **Separation of Concerns**
- Each service does ONE thing
- NLP service = understand language
- Ontology service = access knowledge graph
- Inference service = rank diseases
- Don't mix these!

### 2. **Layering**
```
User Input
    ↓
Controllers (route)
    ↓
Services (do work)
    ↓
Data Layer (get/store)
    ↓
Knowledge (medical facts)
```
Never skip layers or go bottom-up!

### 3. **Dependency Injection**
```python
# GOOD ✅
service = OntologyService(graph_db)

# BAD ❌
service = OntologyService()
service.graph_db = graph_db  # reaches into service

# TERRIBLE ❌
class OntologyService:
    def __init__(self):
        self.graph_db = GraphDB()  # global dependency
```

### 4. **Graceful Degradation**
```python
# Try LLM first
try:
    results = llm.extract()
except OllamaUnavailable:
    # Fall back to keywords
    results = keyword_extract()
```

### 5. **Test First Thinking**
Before writing code, ask:
- What am I testing?
- What's the input?
- What's the expected output?
- What could go wrong?

---

## Key Decisions Made (So You Don't Have To)

### 1. **Ollama for LLMs**
✅ Free, offline-capable, easy to use
✅ REST API = language-agnostic
✅ Models in 3GB-4GB range = laptop-friendly

**Models**:
- Primary: `llama3.2:3b` (fast, good quality)
- Secondary: `phi3.5` (balanced)
- Fallback: `mistral:7b` (high quality for complex reasoning)

### 2. **langextract for Document Parsing**
✅ Extract structured data from unstructured text
✅ Python library = easy integration
✅ Handles medical documents

### 3. **Weighted Scoring Algorithm**
Instead of deep neural nets, use **transparent math**:

```
confidence(disease) = 
    (matched_symptoms_weight / total_weight) × 
    (matched_count / required_count)
```

Why? **Explainable, fast, offline, no training needed**

### 4. **5 Instead of 3 Layers**
- More layers = better separation
- Better separation = easier testing
- Easier testing = faster development

### 5. **JSON Ontology**
- In-memory loading = fast queries
- No database overhead
- Easy to export/import
- Perfect for 100-1000 entities

---

## Common Mistakes to Avoid

❌ **Don't** mix service responsibilities
```python
# WRONG - NLP service should NOT query ontology
class NLPService:
    def extract_symptoms(self, text):
        symptoms = parse(text)
        return self.ontology.lookup(symptoms)  # NO!
```

✅ **Do** return extracted data, let caller query ontology
```python
# CORRECT
class NLPService:
    def extract_symptoms(self, text):
        return parse(text)  # Just extract

# Use it:
symptoms = nlp.extract_symptoms(text)
nodes = ontology.lookup(symptoms)
```

---

❌ **Don't** load everything at startup
```python
# WRONG - slow startup
class OllamaClient:
    def __init__(self):
        self.list_models()  # Blocks startup!
        self.models = self.pull_all_models()  # 20 minutes/users waits
```

✅ **Do** lazy-load on demand
```python
# CORRECT
class OllamaClient:
    def __init__(self):
        self.models = None  # Lazy
    
    def ensure_model_loaded(self, model):
        if model not in self.models:
            self.pull_model(model)  # Only when needed
```

---

❌ **Don't** create hard dependencies on Ollama
```python
# WRONG - system breaks if Ollama down
def extract_symptoms(text):
    return ollama.generate(extract_prompt)
```

✅ **Do** provide fallbacks
```python
# CORRECT
def extract_symptoms(text):
    try:
        return ollama.generate(extract_prompt)
    except OllamaUnavailable:
        return keyword_extract(text)  # Fallback
```

---

## Architecture Validation

**Before coding, validate your understanding:**

### Checklist:
- [ ] I can explain the 5 layers and their purpose
- [ ] I can draw the data flow from input → diagnosis
- [ ] I understand why each layer exists
- [ ] I know which service handles what
- [ ] I understand how services don't talk to each other directly
- [ ] I know the fallback strategy for Ollama unavailability
- [ ] I understand the folder structure and where to put new code
- [ ] I can name 3 advantages of this architecture over monolithic

**If any ❌, re-read ARCHITECTURE doc and ask questions.**

---

## Timeline Reality Check

This is a **realistic 8-10 week project**:

- **Weeks 1-2**: Foundation + Ollama (you can parallelize setup)
- **Weeks 3-4**: Services (core business logic)
- **Weeks 5-6**: Agentic orchestrator (tying it together)
- **Week 7**: Text extraction + API layer
- **Week 8**: Testing + quality assurance
- **Weeks 9-10**: Documentation + deployment

**Parallel work**: 
- Setup Ollama and download models while doing Phase 1
- Have test data ready while building services
- Design UI while building backend

---

## Success Looks Like

### After Phase 1 ✅
```python
python -c "from src.config.settings import Config; print('OK')"
# Prints: OK
```

### After Phase 2 ✅
```bash
ollama serve &  # Ollama running
python -c "from src.integrations.ollama_client import OllamaClient; \
           c = OllamaClient(); print(c.is_healthy())"
# Prints: True
```

### After Phase 4 ✅
```bash
python
>>> from src.orchestration.agents.medical_ai_agent import MedicalAIAgent
>>> agent = MedicalAIAgent(nlp, ontology, inference, prompts)
>>> result = agent.reason("I have fever and cough")
>>> print(result.primary_diagnosis)
# Prints: Pneumonia (confidence: 0.87)
```

### After Phase 8 ✅
```bash
docker-compose up
curl http://localhost:5000/api/diagnose -d '{"input":"fever, cough"}'
# Returns JSON diagnosis with confidence, treatments, explanation
```

---

## Questions to Ask Team

Before starting, clarify:

1. **Ollama Setup**
   - Will Ollama be pre-installed on deployment servers?
   - Should we download models during build or runtime?
   - What models should be mandatory vs. optional?

2. **Performance**
   - Target response time? (e.g., <500ms)
   - Expected concurrent users?
   - Will we cache LLM responses?

3. **Integration**
   - Will this integrate with existing ontology editor?
   - What's the patient data source?
   - Do we need audit trail of all diagnoses?

4. **Scope**
   - How many diseases to support initially? (start with 10-20)
   - How many symptoms? (start with 30-50)
   - Is medical accuracy critical or educational?

5. **Constraints**
   - Memory limits?
   - Internet availability (offline requirement)?
   - Data privacy requirements?

---

## Next Actions

**Today**:
- [ ] Read MEDICAL_AI_AGENTIC_ARCHITECTURE.md
- [ ] Review folder structure in IMPLEMENTATION_ROADMAP.md
- [ ] Create GitHub issue to track Phase 1 work

**This Week**:
- [ ] Complete Phase 1 foundation
- [ ] Install Ollama locally
- [ ] Download primary model
- [ ] Create test script that shows architecture is working

**Next Week**:
- [ ] Start Phase 2: Ollama client
- [ ] Write unit tests for OllamaClient
- [ ] Build health check script

---

## Getting Help

### When you're stuck:

1. **"Which file do I create?"** → Check IMPLEMENTATION_ROADMAP.md "Implementation Checklist"
2. **"What should this function do?"** → Check IMPLEMENTATION_GUIDE.md code patterns
3. **"Why is there this layer?"** → Check ARCHITECTURE.md "Layer Responsibilities"
4. **"How do I test this?"** → Check IMPLEMENTATION_GUIDE.md "Testing Patterns"
5. **"What's the data flow?"** → Check ARCHITECTURE.md "Data Flow Examples"

---

## Documents You Now Have

✅ **MEDICAL_AI_AGENTIC_ARCHITECTURE.md** (Main Design)
- System overview
- All 5 layers explained
- Component details
- Data flow examples
- Technology stack
- Success criteria

✅ **MEDICAL_AI_IMPLEMENTATION_ROADMAP.md** (Execution Plan)
- Folder structure
- 8 phases with details
- Implementation checklist
- Timeline and dependencies
- Risk mitigation

✅ **MEDICAL_AI_IMPLEMENTATION_GUIDE.md** (Code Patterns)
- Layer 1-5 patterns
- Testing patterns
- Error handling
- Performance optimization
- Configuration management

✅ **This Document** (Quick Start)
- What you're building
- 3-step plan
- Getting started checklist
- Key principles
- Common mistakes
- Success criteria

---

## Final Thought

You're building something **genuinely interesting**:
- ✅ Explainable AI (not a black box)
- ✅ Privacy-preserving (offline capable)
- ✅ Cost-effective (no API fees)
- ✅ Technically sophisticated (layered architecture)
- ✅ Medically grounded (ontology-based)

The architecture you now have is **enterprise-grade** and **production-ready in design**.

**Your job now is to implement it, one layer at a time, one service at a time, one test at a time.**

Ready to go? Start with Phase 1! 🚀

