# Medical AI Agentic Reasoner - Component Implementation Guide

**Version**: 1.0  
**Date**: February 24, 2026  
**Purpose**: Code patterns, design decisions, and implementation details for developers

---

## Quick Navigation

- [Layer 1: Presentation](#layer-1-presentation)
- [Layer 2: Orchestration](#layer-2-orchestration)
- [Layer 3: Services](#layer-3-services)
- [Layer 4: Data & Integration](#layer-4-data--integration)
- [Layer 5: Models & Knowledge](#layer-5-models--knowledge)
- [Testing Patterns](#testing-patterns)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)

---

## Layer 1: Presentation

### Controllers Pattern

**File**: `src/presentation/controllers/diagnosis_controller.py`

```python
from flask import request, jsonify
from ..services.nlp_service import NLPService
from ..orchestration.agents.medical_ai_agent import MedicalAIAgent

class DiagnosisController:
    def __init__(self, agent: MedicalAIAgent):
        self.agent = agent
    
    def handle_diagnosis(self):
        """POST /api/diagnose"""
        try:
            # 1. Validate request
            data = request.get_json()
            if not data or 'input' not in data:
                return jsonify({'error': 'Missing input'}), 400
            
            # 2. Extract parameters
            user_input = data['input']
            include_reasoning = data.get('include_reasoning', True)
            
            # 3. Execute agent
            result = self.agent.reason(user_input)
            
            # 4. Format response
            response = {
                'status': 'success',
                'data': {
                    'diagnosis': result.to_dict(),
                    'confidence': result.confidence_score,
                    'treatments': [t.to_dict() for t in result.treatments]
                }
            }
            
            if include_reasoning:
                response['reasoning'] = result.reasoning_chain.to_dict()
            
            return jsonify(response), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Register with Flask
def register_diagnosis_routes(app, agent):
    controller = DiagnosisController(agent)
    app.add_url_rule('/api/diagnose', 'diagnose', 
                     controller.handle_diagnosis, methods=['POST'])
```

### Request/Response Contracts

**File**: `src/presentation/schemas/diagnosis_schema.py`

```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class DiagnosisRequest:
    input: str                           # Natural language or symptom list
    history: Optional[str] = None        # Patient history
    include_reasoning: bool = True       # Show reasoning chain
    exclude_conditions: Optional[List[str]] = None  # Exclude certain diseases

@dataclass
class DiagnosisResponse:
    status: str                          # 'success', 'error'
    data: dict                           # Diagnosis + treatments
    reasoning: Optional[dict] = None     # Reasoning chain
    metadata: dict = None                # Execution time, model used, etc.
```

---

## Layer 2: Orchestration

### Agent Orchestrator Pattern

**File**: `src/orchestration/agents/medical_ai_agent.py`

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentState:
    """Track agent execution state"""
    user_input: str = ""
    extracted_symptoms: List[str] = field(default_factory=list)
    matched_diseases: List[Dict] = field(default_factory=list)
    selected_diagnosis: Optional[Dict] = None
    reasoning_steps: List[Dict] = field(default_factory=list)
    execution_time_ms: float = 0.0
    llm_calls_made: int = 0

class MedicalAIAgent:
    """Orchestrates medical reasoning pipeline"""
    
    def __init__(self, nlp_service, ontology_service, 
                 inference_service, prompt_service, config):
        self.nlp = nlp_service
        self.ontology = ontology_service
        self.inference = inference_service
        self.prompts = prompt_service
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def reason(self, user_input: str) -> DiagnosisResult:
        """Main reasoning pipeline"""
        import time
        start_time = time.time()
        state = AgentState(user_input=user_input)
        
        try:
            # Step 1: Parse and extract symptoms
            state = self._step_symptom_extraction(state)
            
            # Step 2: Query ontology
            state = self._step_ontology_query(state)
            
            # Step 3: Perform inference
            state = self._step_inference(state)
            
            # Step 4: Get treatments
            state = self._step_treatment_lookup(state)
            
            # Step 5: Generate explanation
            state = self._step_explanation_generation(state)
            
            # Build final result
            state.execution_time_ms = (time.time() - start_time) * 1000
            return self._build_result(state)
        
        except Exception as e:
            self.logger.error(f"Reasoning loop failed: {e}", exc_info=True)
            raise
    
    def _step_symptom_extraction(self, state: AgentState) -> AgentState:
        """Step 1: Extract symptoms from user input"""
        step_num = len(state.reasoning_steps) + 1
        start = time.time()
        
        try:
            # Try keyword matching first (fast)
            extracted = self.nlp.extract_symptoms(state.user_input)
            state.extracted_symptoms = extracted.get('symptoms', [])
            
            reason = {
                'step': step_num,
                'name': 'Symptom Extraction',
                'status': 'success',
                'symptoms_found': state.extracted_symptoms,
                'confidence': extracted.get('confidence', 0.8),
                'duration_ms': (time.time() - start) * 1000
            }
        except Exception as e:
            reason = {
                'step': step_num,
                'name': 'Symptom Extraction',
                'status': 'partial',
                'error': str(e),
                'duration_ms': (time.time() - start) * 1000
            }
        
        state.reasoning_steps.append(reason)
        return state
    
    def _step_ontology_query(self, state: AgentState) -> AgentState:
        """Step 2: Look up symptoms in ontology"""
        step_num = len(state.reasoning_steps) + 1
        start = time.time()
        
        # Query ontology for all symptoms
        symptom_nodes = []
        for symptom_text in state.extracted_symptoms:
            nodes = self.ontology.lookup_symptoms([symptom_text])
            symptom_nodes.extend(nodes)
        
        state.reasoning_steps.append({
            'step': step_num,
            'name': 'Ontology Query',
            'status': 'success',
            'symptoms_matched': len(symptom_nodes),
            'details': {node.id: node.label for node in symptom_nodes},
            'duration_ms': (time.time() - start) * 1000
        })
        
        return state
    
    def _step_inference(self, state: AgentState) -> AgentState:
        """Step 3: Rank diseases using inference"""
        step_num = len(state.reasoning_steps) + 1
        start = time.time()
        
        # Call inference engine to rank diseases
        ranked_diseases = self.inference.rankBySymptoms(state.extracted_symptoms)
        state.matched_diseases = ranked_diseases[:10]  # Top 10
        state.selected_diagnosis = ranked_diseases[0] if ranked_diseases else None
        
        state.reasoning_steps.append({
            'step': step_num,
            'name': 'Disease Inference',
            'status': 'success',
            'top_diagnosis': {
                'disease': state.selected_diagnosis['name'],
                'confidence': state.selected_diagnosis['confidence']
            } if state.selected_diagnosis else None,
            'alternatives_found': len(ranked_diseases),
            'duration_ms': (time.time() - start) * 1000
        })
        
        return state
    
    def _step_treatment_lookup(self, state: AgentState) -> AgentState:
        """Step 4: Get treatments for diagnosis"""
        step_num = len(state.reasoning_steps) + 1
        start = time.time()
        
        treatments = []
        if state.selected_diagnosis:
            treatments = self.ontology.get_treatments(state.selected_diagnosis['id'])
        
        state.reasoning_steps.append({
            'step': step_num,
            'name': 'Treatment Lookup',
            'status': 'success',
            'treatments_found': len(treatments),
            'details': [t.to_dict() for t in treatments],
            'duration_ms': (time.time() - start) * 1000
        })
        
        return state
    
    def _step_explanation_generation(self, state: AgentState) -> AgentState:
        """Step 5: Generate natural language explanation"""
        step_num = len(state.reasoning_steps) + 1
        start = time.time()
        
        if not state.selected_diagnosis:
            state.reasoning_steps.append({
                'step': step_num,
                'name': 'Explanation',
                'status': 'skipped',
                'reason': 'No diagnosis found'
            })
            return state
        
        # Build prompt with context
        prompt = self.prompts.build_diagnosis_explanation_prompt(
            diagnosis=state.selected_diagnosis,
            symptoms=state.extracted_symptoms
        )
        
        try:
            explanation = self.nlp.llm_call(prompt)
            state.reasoning_steps.append({
                'step': step_num,
                'name': 'Explanation Generation',
                'status': 'success',
                'explanation': explanation,
                'duration_ms': (time.time() - start) * 1000
            })
            state.llm_calls_made += 1
        except Exception as e:
            state.reasoning_steps.append({
                'step': step_num,
                'name': 'Explanation Generation',
                'status': 'failed',
                'error': str(e),
                'duration_ms': (time.time() - start) * 1000
            })
        
        return state
    
    def _build_result(self, state: AgentState) -> DiagnosisResult:
        """Convert state to final result"""
        return DiagnosisResult(
            primary_diagnosis=state.selected_diagnosis,
            confidence_score=state.selected_diagnosis['confidence'] if state.selected_diagnosis else 0,
            alternative_diagnoses=state.matched_diseases[1:],
            treatments=[...],  # from state
            reasoning_chain=ReasoningChain(
                total_steps=len(state.reasoning_steps),
                steps=state.reasoning_steps,
                total_duration_ms=state.execution_time_ms,
                llm_calls_made=state.llm_calls_made
            ),
            warnings=self._generate_warnings(state)
        )
    
    def _generate_warnings(self, state: AgentState) -> List[str]:
        """Generate warnings if diagnosis confidence is low"""
        warnings = []
        if state.selected_diagnosis and state.selected_diagnosis['confidence'] < 0.6:
            warnings.append(
                f"Low confidence ({state.selected_diagnosis['confidence']:.0%}). "
                f"Recommend consulting with medical professional."
            )
        if len(state.extracted_symptoms) < 2:
            warnings.append("Few symptoms provided. More information would improve accuracy.")
        return warnings
```

### Reasoning Engine Pattern

**File**: `src/orchestration/reasoning/engine.py`

```python
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ReasoningEngine:
    """Core reasoning algorithms for diagnosis"""
    
    def __init__(self, ontology_service, config):
        self.ontology = ontology_service
        self.config = config
    
    def rankBySymptoms(self, symptom_ids: List[str], 
                      top_k: int = 10) -> List[Dict]:
        """
        Rank diseases by symptom match using weighted scoring.
        
        Algorithm:
        1. Load all diseases from ontology
        2. For each disease:
           a. symptom_score = Sum(weights of matched symptoms) / total_weight
           b. coverage_score = matched_count / required_count
           c. confidence = symptom_score * coverage_score
        3. Normalize confidence to 0-100
        4. Sort descending and return top_k
        
        Args:
            symptom_ids: List of extracted symptom identifiers
            top_k: Return top K results
        
        Returns:
            List of diseases with confidence scores
        """
        all_diseases = self.ontology.get_all_diseases()
        scores = []
        
        for disease in all_diseases:
            # Get disease symptom relationships (with weights)
            disease_symptoms = self.ontology.get_disease_symptoms(disease.id)
            
            # Calculate match score
            matched_weight = 0.0
            total_weight = sum(s['weight'] for s in disease_symptoms.values())
            
            for symptom_id, symptom_info in disease_symptoms.items():
                if symptom_id in symptom_ids:
                    matched_weight += symptom_info['weight']
            
            if total_weight == 0:
                symptom_score = 0.0
            else:
                symptom_score = matched_weight / total_weight
            
            # Calculate coverage (how many symptoms found)
            coverage_score = len([s for s in disease_symptoms if s in symptom_ids]) / len(disease_symptoms)
            
            # Combined confidence
            confidence = symptom_score * coverage_score
            
            scores.append({
                'id': disease.id,
                'name': disease.label,
                'confidence': confidence,
                'symptom_score': symptom_score,
                'coverage_score': coverage_score,
                'matched_symptoms': [s for s in disease_symptoms if s in symptom_ids],
                'total_symptoms': len(disease_symptoms)
            })
        
        # Normalize to 0-100
        if scores:
            max_confidence = max(s['confidence'] for s in scores)
            if max_confidence > 0:
                for s in scores:
                    s['confidence'] = (s['confidence'] / max_confidence) * 100
        
        # Sort and return
        return sorted(scores, key=lambda x: x['confidence'], reverse=True)[:top_k]
    
    def validateDiagnosis(self, disease_id: str, 
                         symptoms: List[str]) -> Dict[str, Any]:
        """
        Validate a diagnosis against medical rules.
        
        Returns:
        {
            'valid': bool,
            'confidence': float,
            'warnings': List[str],
            'contraindications': List[str]
        }
        """
        disease = self.ontology.get_disease(disease_id)
        validation = {
            'valid': True,
            'warnings': [],
            'contraindications': []
        }
        
        # Check if serious disease with missing critical symptoms
        if disease.severity == 'severe':
            critical_symptoms = [s for s in disease.symptoms if s.required]
            missing_critical = [s for s in critical_symptoms if s.id not in symptoms]
            
            if missing_critical:
                validation['warnings'].append(
                    f"Diagnosis of {disease.label} is unusual without "
                    f"symptoms: {[s.name for s in missing_critical]}"
                )
        
        return validation
    
    def explainReasoning(self, disease_id: str, 
                        symptoms: List[str]) -> str:
        """
        Generate plain-English explanation of reasoning.
        
        Returns: "Based on the presence of fever, cough, and chest pain..."
        """
        disease = self.ontology.get_disease(disease_id)
        disease_symptoms = self.ontology.get_disease_symptoms(disease_id)
        
        matched = [s for s in disease_symptoms if s in symptoms]
        symptom_names = [self.ontology.get_symptom(s).label for s in matched]
        
        explanation = (
            f"Based on the symptoms {', '.join(symptom_names[:-1])} "
            f"and {symptom_names[-1]}, the most likely diagnosis is {disease.label}. "
            f"This condition is characterized by the presence of "
            f"{', '.join([self.ontology.get_symptom(s).label for s in disease.symptoms[:3]])}. "
        )
        
        return explanation
```

---

## Layer 3: Services

### NLP Service Pattern

**File**: `src/services/nlp_service.py`

```python
from typing import Dict, List, Optional
from ..integrations.ollama_client import OllamaClient
import re
import logging

logger = logging.getLogger(__name__)

class NLPService:
    """Natural language processing with Ollama integration"""
    
    def __init__(self, ollama_client: OllamaClient, config):
        self.ollama = ollama_client
        self.config = config
        self.symptom_keywords = self._load_symptom_keywords()
    
    def extract_symptoms(self, text: str) -> Dict[str, any]:
        """
        Extract medical symptoms from text.
        
        Strategy:
        1. Fast path: Keyword matching (O(n) complexity)
        2. Accurate path: LLM extraction (higher accuracy)
        3. Combined approach for best results
        """
        results = {
            'symptoms': [],
            'method': None,
            'confidence': 0.0
        }
        
        # Fast path: keyword matching
        keyword_matches = self._extract_by_keywords(text)
        if keyword_matches:
            results['symptoms'] = keyword_matches['symptoms']
            results['method'] = 'keyword_matching'
            results['confidence'] = keyword_matches.get('confidence', 0.8)
            logger.info(f"Extracted {len(keyword_matches['symptoms'])} symptoms via keywords")
            return results
        
        # Accurate path: LLM extraction
        try:
            llm_matches = self._extract_by_llm(text)
            results['symptoms'] = llm_matches['symptoms']
            results['method'] = 'llm_extraction'
            results['confidence'] = llm_matches.get('confidence', 0.9)
            logger.info(f"Extracted {len(llm_matches['symptoms'])} symptoms via LLM")
        except Exception as e:
            logger.warning(f"LLM extraction failed: {e}, using keyword matching")
            results['symptoms'] = keyword_matches.get('symptoms', [])
            results['method'] = 'keyword_matching_fallback'
            results['confidence'] = 0.6
        
        return results
    
    def _extract_by_keywords(self, text: str) -> Dict[str, any]:
        """Fast keyword-based symptom extraction"""
        text_lower = text.lower()
        matched = []
        
        for symptom_id, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    matched.append(symptom_id)
                    break
        
        return {
            'symptoms': list(set(matched)),
            'confidence': 0.8
        }
    
    def _extract_by_llm(self, text: str) -> Dict[str, any]:
        """Use Ollama LLM for accurate symptom extraction"""
        prompt = f"""Extract all medical symptoms mentioned in this text:
'{text}'

Return ONLY a JSON array of symptom names, no explanations:
["symptom1", "symptom2", "symptom3"]"""
        
        response = self.ollama.generate(
            model=self.config.NLP_MODEL,
            prompt=prompt
        )
        
        try:
            # Parse JSON from response
            symptoms = json.loads(response)
            return {'symptoms': symptoms, 'confidence': 0.95}
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return {'symptoms': [], 'confidence': 0.0}
    
    def classify_intent(self, text: str) -> str:
        """Classify user intent: diagnose, explain, treat, etc."""
        intent_keywords = {
            'diagnose': ['what do i have', 'diagnose', 'what condition'],
            'explain': ['explain', 'why', 'how does'],
            'treat': ['how to treat', 'treatment', 'medication'],
            'query': ['list', 'show', 'symptoms of']
        }
        
        text_lower = text.lower()
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return 'diagnose'  # default
    
    def llm_call(self, prompt: str, model: Optional[str] = None) -> str:
        """Call Ollama LLM with given prompt"""
        model = model or self.config.PRIMARY_LLM
        
        try:
            response = self.ollama.generate(
                model=model,
                prompt=prompt,
                temperature=self.config.LLM_TEMPERATURE
            )
            return response.strip()
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _load_symptom_keywords(self) -> Dict[str, List[str]]:
        """Load symptom keywords from config/knowledge base"""
        return {
            'fever': ['fever', 'high temperature', 'hot', 'feverish'],
            'cough': ['cough', 'coughing', 'hacking cough'],
            'headache': ['headache', 'head pain', 'head ache'],
            # ... more symptoms
        }
```

### Prompt Service Pattern

**File**: `src/services/prompt_service.py`

```python
from typing import Dict, List, Optional

class PromptService:
    """Manage and build prompts for Ollama LLM"""
    
    def __init__(self, config):
        self.config = config
        self.templates = self._load_templates()
    
    def build_symptom_extraction_prompt(self, text: str) -> str:
        """Build prompt for symptom extraction"""
        return f"""You are a medical assistant. Extract all medical symptoms mentioned in the following text.

Text: "{text}"

Return ONLY a JSON array of symptom names. Example: ["fever", "cough", "fatigue"]

Symptoms:"""
    
    def build_diagnosis_explanation_prompt(self, disease: Dict, 
                                          symptoms: List[str]) -> str:
        """Build prompt to explain a diagnosis"""
        symptoms_str = ', '.join(symptoms)
        
        return f"""Explain in medical terms why the diagnosis of {disease['name']} is likely given these symptoms: {symptoms_str}

Keep the explanation brief (2-3 sentences) and mention:
1. Why these symptoms match the condition
2. Any important notes about the condition

Explanation:"""
    
    def build_treatment_recommendation_prompt(self, disease: Dict) -> str:
        """Build prompt for treatment recommendations"""
        return f"""Provide general treatment recommendations for {disease['name']}.

Include:
1. Over-the-counter options (if appropriate)
2. When to see a doctor
3. Prevention measures

Keep recommendations evidence-based and general (not specific medical advice).

Recommendations:"""
    
    def add_medical_context(self, prompt: str, 
                           ontology_context: Dict) -> str:
        """Add relevant medical context from ontology to prompt"""
        context = f"""You are a medical reasoning assistant. You have access to the following medical ontology:

Diseases: {ontology_context.get('diseases', [])}
Symptoms: {ontology_context.get('symptoms', [])}
Treatments: {ontology_context.get('treatments', [])}

Use this context to provide accurate medical information.

---

{prompt}"""
        return context
    
    def add_patient_history(self, prompt: str, 
                           history: Dict) -> str:
        """Add patient-specific context to prompt"""
        context = f"""Patient Information:
- Age: {history.get('age', 'unknown')}
- Gender: {history.get('gender', 'unknown')}
- Medical History: {history.get('conditions', [])}
- Current Medications: {history.get('medications', [])}
- Known Allergies: {history.get('allergies', [])}

---

{prompt}"""
        return context
```

---

## Layer 4: Data & Integration

### Ollama Client Pattern

**File**: `src/integrations/ollama_client.py`

```python
import requests
import logging
from typing import List, Dict, Iterator, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for Ollama local LLM server"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 300  # 5 minutes for long responses
    
    def is_healthy(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False
    
    def list_models(self) -> List[Dict]:
        """List available downloaded models"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise
    
    def generate(self, model: str, prompt: str, 
                stream: bool = False, **kwargs) -> str:
        """
        Generate text from prompt.
        
        Args:
            model: Model name (e.g., 'llama3.2:3b')
            prompt: Text prompt
            stream: Whether to stream response
            **kwargs: Additional options (temperature, top_p, etc.)
        
        Returns:
            Generated text
        """
        payload = {
            'model': model,
            'prompt': prompt,
            'stream': stream,
            'temperature': kwargs.get('temperature', 0.7),
            'top_p': kwargs.get('top_p', 0.9)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            if stream:
                text = ""
                for line in response.iter_lines():
                    if line:
                        text += json.loads(line).get('response', '')
                return text
            else:
                return response.json().get('response', '')
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise
    
    def stream_generate(self, model: str, prompt: str, 
                       **kwargs) -> Iterator[str]:
        """Stream generation response"""
        payload = {
            'model': model,
            'prompt': prompt,
            'stream': True,
            'temperature': kwargs.get('temperature', 0.7)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line).get('response', '')
                    if chunk:
                        yield chunk
        
        except Exception as e:
            logger.error(f"LLM streaming failed: {e}")
            raise
    
    def pull_model(self, model_name: str) -> None:
        """Download a new model"""
        logger.info(f"Downloading model {model_name}...")
        
        payload = {'name': model_name, 'stream': True}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=None,  # No timeout for downloads
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    status = json.loads(line)
                    if 'status' in status:
                        logger.info(f"  {status['status']}")
        
        except Exception as e:
            logger.error(f"Model download failed: {e}")
            raise
    
    def delete_model(self, model_name: str) -> None:
        """Remove a model"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={'name': model_name}
            )
            response.raise_for_status()
            logger.info(f"Model {model_name} deleted")
        except Exception as e:
            logger.error(f"Model deletion failed: {e}")
            raise
```

---

## Layer 5: Models & Knowledge

### Domain Models Pattern

**File**: `src/models/domain_models.py`

```python
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum

class Severity(Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

@dataclass
class Symptom:
    id: str                          # e.g., "symp:Fever"
    name: str                        # e.g., "Fever"
    description: str                 # Clinical description
    severity: Severity = Severity.MILD
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'severity': self.severity.value
        }

@dataclass
class Disease:
    id: str                          # e.g., "resp:Pneumonia"
    name: str                        # e.g., "Pneumonia"
    description: str
    severity: Severity
    symptom_ids: List[str]           # IDs of typical symptoms
    icd_code: Optional[str] = None   # ICD-10 code
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Treatment:
    id: str                          # e.g., "treat:Antibiotics"
    name: str
    type: str                        # 'medication', 'procedure', 'lifestyle'
    description: str
    contraindications: List[str] = None  # Drug IDs to avoid
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DiagnosisResult:
    primary_diagnosis: Disease
    confidence_score: float          # 0-100
    alternative_diagnoses: List[Disease]
    treatments: List[Treatment]
    reasoning_chain: 'ReasoningChain'
    warnings: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'primary_diagnosis': self.primary_diagnosis.to_dict(),
            'confidence_score': self.confidence_score,
            'alternatives': [d.to_dict() for d in self.alternative_diagnoses],
            'treatments': [t.to_dict() for t in self.treatments],
            'warnings': self.warnings or []
        }
```

---

## Testing Patterns

### Unit Test Pattern

**File**: `tests/unit/test_reasoning_engine.py`

```python
import pytest
from unittest.mock import Mock, MagicMock
from src.orchestration.reasoning.engine import ReasoningEngine

class TestReasoningEngine:
    
    @pytest.fixture
    def engine(self):
        """Create engine with mock ontology"""
        mock_ontology = Mock()
        config = Mock()
        return ReasoningEngine(mock_ontology, config)
    
    def test_rankBySymptoms_returns_sorted_list(self, engine):
        """Test that diseases are ranked by confidence"""
        # Setup mock data
        mock_diseases = [
            {'id': 'pneumonia', 'label': 'Pneumonia'},
            {'id': 'bronchitis', 'label': 'Bronchitis'},
            {'id': 'cold', 'label': 'Common Cold'}
        ]
        
        # Mock ontology methods
        engine.ontology.get_all_diseases.return_value = mock_diseases
        engine.ontology.get_disease_symptoms.side_effect = [
            {'fever': {'weight': 1.0}, 'cough': {'weight': 1.0}},
            {'cough': {'weight': 1.0}, 'mucus': {'weight': 0.5}},
            {'cough': {'weight': 0.5}, 'sore_throat': {'weight': 0.5}}
        ]
        
        # Test
        symptoms = ['fever', 'cough']
        results = engine.rankBySymptoms(symptoms)
        
        # Assert
        assert len(results) == 3
        assert results[0]['confidence'] >= results[1]['confidence']
        assert results[1]['confidence'] >= results[2]['confidence']
    
    def test_rankBySymptoms_with_no_matches(self, engine):
        """Test handling of no matching diseases"""
        engine.ontology.get_all_diseases.return_value = []
        
        results = engine.rankBySymptoms(['unknown_symptom'])
        
        assert results == []
```

### Integration Test Pattern

**File**: `tests/integration/test_agent_orchestrator.py`

```python
import pytest
from src.orchestration.agents.medical_ai_agent import MedicalAIAgent
from tests.fixtures.mock_services import (
    MockNLPService, MockOntologyService, 
    MockInferenceService, MockPromptService
)

class TestMedicalAIAgent:
    
    @pytest.fixture
    def agent(self):
        """Create agent with mock services"""
        return MedicalAIAgent(
            nlp_service=MockNLPService(),
            ontology_service=MockOntologyService(),
            inference_service=MockInferenceService(),
            prompt_service=MockPromptService(),
            config=Mock()
        )
    
    def test_full_diagnosis_flow(self, agent):
        """Test complete diagnosis reasoning"""
        result = agent.reason("I have fever, cough, and fatigue")
        
        assert result.primary_diagnosis is not None
        assert result.confidence_score > 0
        assert len(result.reasoning_chain.steps) == 5
        assert result.reasoning_chain.total_duration_ms > 0
    
    def test_reasoning_steps_all_complete(self, agent):
        """Test that all reasoning steps complete"""
        result = agent.reason("fever and cough")
        
        for step in result.reasoning_chain.steps:
            assert step['status'] in ['success', 'partial', 'skipped']
            assert 'duration_ms' in step
```

---

## Error Handling

### Graceful Degradation Strategy

```python
class ServiceWithFallback:
    """Service that degrades gracefully when dependencies fail"""
    
    def extract_symptoms(self, text: str) -> Dict:
        try:
            # Try primary method (LLM)
            return self._extract_with_llm(text)
        except OllamaNotAvailableError:
            logger.warning("Ollama unavailable, using keyword matching")
            try:
                # Fallback to keyword matching
                return self._extract_with_keywords(text)
            except Exception as e:
                logger.error(f"Symptom extraction failed completely: {e}")
                return {'symptoms': [], 'confidence': 0.0}
```

### Exception Hierarchy

```python
class MedicalAIException(Exception):
    """Base exception for medical AI system"""
    pass

class OllamaNotAvailableError(MedicalAIException):
    """Ollama server not running"""
    pass

class OllamaTimeoutError(MedicalAIException):
    """Ollama request timed out"""
    pass

class OntologyNotLoadedError(MedicalAIException):
    """Ontology not yet loaded"""
    pass

class InvalidDiagnosisError(MedicalAIException):
    """Diagnosis validation failed"""
    pass
```

---

## Performance Optimization

### Caching Strategy

```python
from functools import lru_cache
import hashlib

class CachingOntologyService:
    
    @lru_cache(maxsize=256)
    def lookup_symptoms(self, symptom_tuple: tuple):
        """Cache symptom lookups"""
        return super().lookup_symptoms(list(symptom_tuple))
    
    def rankBySymptoms(self, symptoms: List[str]):
        """Hash symptoms for cache key"""
        cache_key = hashlib.md5(
            ''.join(sorted(symptoms)).encode()
        ).hexdigest()
        
        if cache_key in self._rank_cache:
            return self._rank_cache[cache_key]
        
        result = self.inference.rankBySymptoms(symptoms)
        self._rank_cache[cache_key] = result
        return result
```

### Response Streaming

```python
def stream_diagnosis(self, user_input: str):
    """Stream reasoning steps as they complete"""
    yield json.dumps({'step': 'starting', 'status': 'in_progress'})
    
    state = AgentState(user_input=user_input)
    state = self._step_symptom_extraction(state)
    yield json.dumps(state.reasoning_steps[-1])
    
    state = self._step_ontology_query(state)
    yield json.dumps(state.reasoning_steps[-1])
    
    # ... continue for all steps
```

---

## Configuration Management

**File**: `src/config/settings.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    PRIMARY_LLM = os.getenv('OLLAMA_PRIMARY_MODEL', 'llama3.2:3b')
    REASONING_LLM = os.getenv('OLLAMA_REASONING_MODEL', 'phi3.5')
    DETAILED_LLM = os.getenv('OLLAMA_DETAILED_MODEL', 'mistral:7b')
    
    # NLP
    NLP_MODEL = PRIMARY_LLM
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///medical_ai.db')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Cache
    CACHE_SIZE = int(os.getenv('CACHE_SIZE', '256'))
    
    # Inference
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.5'))
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', '10'))

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    OLLAMA_BASE_URL = 'http://localhost:11434'  # Still use real server if available

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
```

