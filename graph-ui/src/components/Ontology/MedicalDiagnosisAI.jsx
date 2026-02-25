import React, { useState, useEffect } from 'react';
import './MedicalDiagnosisAI.css';

/**
 * MedicalDiagnosisAI - Medical Reasoning using Ontology
 * 
 * Demonstrates practical application of ontology in healthcare:
 * - Symptom analysis with AI reasoning
 * - Disease classification via ontology hierarchy
 * - Treatment recommendations based on relationships
 * - Explains reasoning path through knowledge graph
 */

// Fallback knowledge base used when the API is unreachable
const FALLBACK_ONTOLOGY = {
  diseases: {
    'resp:CommonCold': {
      label: 'Common Cold',
      parent: 'resp:UpperRespiratoryInfection',
      symptoms: ['symp:RunnyNose', 'symp:SoreThroat', 'symp:Cough', 'symp:Sneezing', 'symp:Fatigue'],
      severity: 'mild',
      treatments: ['treat:Rest', 'treat:Fluids', 'treat:OverTheCounterMeds'],
      description: 'Viral infection of upper respiratory tract'
    },
    'resp:Influenza': {
      label: 'Influenza (Flu)',
      parent: 'resp:ViralRespiratoryInfection',
      symptoms: ['symp:Fever', 'symp:Cough', 'symp:Fatigue', 'symp:BodyAches', 'symp:Headache', 'symp:SoreThroat'],
      severity: 'moderate',
      treatments: ['treat:AntiviralMeds', 'treat:Rest', 'treat:Fluids'],
      description: 'Acute viral respiratory infection with systemic symptoms'
    },
    'resp:Pneumonia': {
      label: 'Pneumonia',
      parent: 'resp:LowerRespiratoryInfection',
      symptoms: ['symp:Fever', 'symp:Cough', 'symp:ChestPain', 'symp:ShortnessOfBreath', 'symp:Fatigue'],
      severity: 'severe',
      treatments: ['treat:Antibiotics', 'treat:Hospitalization', 'treat:OxygenTherapy'],
      description: 'Inflammation of lung tissue, often bacterial'
    },
    'resp:Bronchitis': {
      label: 'Acute Bronchitis',
      parent: 'resp:LowerRespiratoryInfection',
      symptoms: ['symp:Cough', 'symp:Mucus', 'symp:ChestDiscomfort', 'symp:Fatigue', 'symp:SoreThroat'],
      severity: 'moderate',
      treatments: ['treat:Rest', 'treat:Fluids', 'treat:CoughMedicine'],
      description: 'Inflammation of bronchial tubes'
    },
    'gi:Gastroenteritis': {
      label: 'Gastroenteritis',
      parent: 'gi:DigestiveInfection',
      symptoms: ['symp:Nausea', 'symp:Vomiting', 'symp:Diarrhea', 'symp:AbdominalPain', 'symp:Fever'],
      severity: 'moderate',
      treatments: ['treat:Fluids', 'treat:Rest', 'treat:ElectrolyteReplacement'],
      description: 'Inflammation of stomach and intestines'
    },
    'neuro:Migraine': {
      label: 'Migraine',
      parent: 'neuro:PrimaryHeadache',
      symptoms: ['symp:SevereHeadache', 'symp:Nausea', 'symp:LightSensitivity', 'symp:SoundSensitivity'],
      severity: 'moderate',
      treatments: ['treat:PainRelievers', 'treat:DarkRoom', 'treat:Rest'],
      description: 'Recurrent severe headache disorder'
    },
    'cardio:Hypertension': {
      label: 'Hypertension',
      parent: 'cardio:CardiovascularDisorder',
      symptoms: ['symp:Headache', 'symp:Dizziness', 'symp:ChestPain'],
      severity: 'moderate',
      treatments: ['treat:BloodPressureMeds', 'treat:LifestyleChanges', 'treat:DietModification'],
      description: 'Persistently elevated blood pressure'
    }
  },
  
  symptoms: {
    'symp:Fever': { label: 'Fever', weights: { 'resp:Influenza': 0.9, 'resp:Pneumonia': 0.85, 'gi:Gastroenteritis': 0.7 } },
    'symp:Cough': { label: 'Cough', weights: { 'resp:CommonCold': 0.8, 'resp:Influenza': 0.85, 'resp:Bronchitis': 0.95, 'resp:Pneumonia': 0.9 } },
    'symp:RunnyNose': { label: 'Runny Nose', weights: { 'resp:CommonCold': 0.95 } },
    'symp:SoreThroat': { label: 'Sore Throat', weights: { 'resp:CommonCold': 0.85, 'resp:Influenza': 0.7, 'resp:Bronchitis': 0.6 } },
    'symp:Sneezing': { label: 'Sneezing', weights: { 'resp:CommonCold': 0.9 } },
    'symp:Fatigue': { label: 'Fatigue', weights: { 'resp:CommonCold': 0.7, 'resp:Influenza': 0.85, 'resp:Pneumonia': 0.8, 'resp:Bronchitis': 0.75 } },
    'symp:BodyAches': { label: 'Body Aches', weights: { 'resp:Influenza': 0.9 } },
    'symp:Headache': { label: 'Headache', weights: { 'resp:Influenza': 0.75, 'neuro:Migraine': 0.5, 'cardio:Hypertension': 0.6 } },
    'symp:ChestPain': { label: 'Chest Pain', weights: { 'resp:Pneumonia': 0.8, 'cardio:Hypertension': 0.65 } },
    'symp:ShortnessOfBreath': { label: 'Shortness of Breath', weights: { 'resp:Pneumonia': 0.85 } },
    'symp:ChestDiscomfort': { label: 'Chest Discomfort', weights: { 'resp:Bronchitis': 0.7 } },
    'symp:Mucus': { label: 'Mucus Production', weights: { 'resp:Bronchitis': 0.85 } },
    'symp:Nausea': { label: 'Nausea', weights: { 'gi:Gastroenteritis': 0.9, 'neuro:Migraine': 0.7 } },
    'symp:Vomiting': { label: 'Vomiting', weights: { 'gi:Gastroenteritis': 0.85 } },
    'symp:Diarrhea': { label: 'Diarrhea', weights: { 'gi:Gastroenteritis': 0.9 } },
    'symp:AbdominalPain': { label: 'Abdominal Pain', weights: { 'gi:Gastroenteritis': 0.8 } },
    'symp:SevereHeadache': { label: 'Severe Headache', weights: { 'neuro:Migraine': 0.95 } },
    'symp:LightSensitivity': { label: 'Light Sensitivity', weights: { 'neuro:Migraine': 0.85 } },
    'symp:SoundSensitivity': { label: 'Sound Sensitivity', weights: { 'neuro:Migraine': 0.8 } },
    'symp:Dizziness': { label: 'Dizziness', weights: { 'cardio:Hypertension': 0.7 } }
  },

  treatments: {
    'treat:Rest': { label: 'Rest and Sleep', type: 'general' },
    'treat:Fluids': { label: 'Increase Fluid Intake', type: 'general' },
    'treat:OverTheCounterMeds': { label: 'Over-the-Counter Medications', type: 'medication' },
    'treat:AntiviralMeds': { label: 'Antiviral Medications', type: 'prescription' },
    'treat:Antibiotics': { label: 'Antibiotics', type: 'prescription' },
    'treat:Hospitalization': { label: 'Hospital Admission', type: 'urgent' },
    'treat:OxygenTherapy': { label: 'Oxygen Therapy', type: 'urgent' },
    'treat:CoughMedicine': { label: 'Cough Suppressants', type: 'medication' },
    'treat:ElectrolyteReplacement': { label: 'Electrolyte Replacement', type: 'general' },
    'treat:PainRelievers': { label: 'Pain Relief Medication', type: 'medication' },
    'treat:DarkRoom': { label: 'Dark, Quiet Room', type: 'general' },
    'treat:BloodPressureMeds': { label: 'Blood Pressure Medication', type: 'prescription' },
    'treat:LifestyleChanges': { label: 'Lifestyle Modifications', type: 'general' },
    'treat:DietModification': { label: 'Dietary Changes', type: 'general' }
  },

  hierarchy: {
    'resp:UpperRespiratoryInfection': { label: 'Upper Respiratory Infection', parent: 'resp:RespiratoryInfection' },
    'resp:LowerRespiratoryInfection': { label: 'Lower Respiratory Infection', parent: 'resp:RespiratoryInfection' },
    'resp:ViralRespiratoryInfection': { label: 'Viral Respiratory Infection', parent: 'resp:RespiratoryInfection' },
    'resp:RespiratoryInfection': { label: 'Respiratory Infection', parent: 'owl:Disease' },
    'gi:DigestiveInfection': { label: 'Digestive System Infection', parent: 'owl:Disease' },
    'neuro:PrimaryHeadache': { label: 'Primary Headache Disorder', parent: 'neuro:NeurologicalDisorder' },
    'neuro:NeurologicalDisorder': { label: 'Neurological Disorder', parent: 'owl:Disease' },
    'cardio:CardiovascularDisorder': { label: 'Cardiovascular Disorder', parent: 'owl:Disease' }
  }
};

const MedicalDiagnosisAI = () => {
  // Ontology loaded from Flask API (falls back to hardcoded if API is down)
  const [medicalOntology, setMedicalOntology] = useState(FALLBACK_ONTOLOGY);
  const [ontologySource, setOntologySource] = useState('built-in');

  useEffect(() => {
    fetch('/api/ontology/medical')
      .then(r => r.json())
      .then(json => {
        if (json.data) {
          setMedicalOntology(json.data);
          setOntologySource(json.data.source || 'api');
          console.log('[MedicalAI] Ontology loaded from API:', Object.keys(json.data.diseases).length, 'diseases');
        }
      })
      .catch(err => {
        console.warn('[MedicalAI] API unavailable, using built-in ontology:', err.message);
      });
  }, []);

  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [diagnosis, setDiagnosis] = useState(null);
  const [reasoning, setReasoning] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  // Ollama LLM state (Sprint 1)
  const [aiResult, setAiResult] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState(null);

  const allSymptoms = Object.entries(medicalOntology.symptoms).map(([id, data]) => ({
    id,
    label: data.label
  }));

  const toggleSymptom = (symptomId) => {
    setSelectedSymptoms(prev => 
      prev.includes(symptomId) 
        ? prev.filter(s => s !== symptomId)
        : [...prev, symptomId]
    );
  };

  const performDiagnosis = () => {
    if (selectedSymptoms.length === 0) {
      alert('Please select at least one symptom');
      return;
    }

    setAnalyzing(true);
    setDiagnosis(null);
    setReasoning(null);

    // Simulate AI processing delay
    setTimeout(() => {
      const result = runDiagnosticReasoning(selectedSymptoms);
      setDiagnosis(result.diagnosis);
      setReasoning(result.reasoning);
      setAnalyzing(false);
    }, 1500);
  };

  const runDiagnosticReasoning = (symptoms) => {
    // Calculate match scores for each disease
    const diseaseScores = {};
    const matchDetails = {};

    Object.entries(medicalOntology.diseases).forEach(([diseaseId, disease]) => {
      let score = 0;
      let matchedSymptoms = [];
      let totalWeight = 0;

      symptoms.forEach(symptomId => {
        const symptomData = medicalOntology.symptoms[symptomId];
        if (symptomData.weights[diseaseId]) {
          const weight = symptomData.weights[diseaseId];
          score += weight;
          totalWeight += 1;
          matchedSymptoms.push({
            symptom: symptomData.label,
            weight: weight
          });
        }
      });

      // Normalize score
      if (totalWeight > 0) {
        const normalizedScore = (score / symptoms.length) * 100;
        diseaseScores[diseaseId] = normalizedScore;
        matchDetails[diseaseId] = {
          matchedSymptoms,
          matchCount: matchedSymptoms.length,
          totalSymptoms: disease.symptoms.length,
          coverage: (matchedSymptoms.length / disease.symptoms.length) * 100
        };
      }
    });

    // Sort by score
    const sortedDiseases = Object.entries(diseaseScores)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 3);

    // Build reasoning explanation
    const topDisease = sortedDiseases[0];
    const diseaseData = medicalOntology.diseases[topDisease[0]];
    
    // Get inheritance chain
    const inheritanceChain = getInheritanceChain(diseaseData.parent);

    const reasoningSteps = [
      {
        step: 1,
        title: 'Symptom Analysis',
        description: `Analyzed ${symptoms.length} reported symptoms against medical ontology database`
      },
      {
        step: 2,
        title: 'Pattern Matching',
        description: `Matched symptoms to ${sortedDiseases.length} potential conditions using weighted scoring algorithm`
      },
      {
        step: 3,
        title: 'Ontology Reasoning',
        description: `Applied hierarchical classification: ${inheritanceChain.join(' → ')}`
      },
      {
        step: 4,
        title: 'Confidence Calculation',
        description: `Computed match confidence: ${topDisease[1].toFixed(1)}% based on symptom weights and coverage`
      }
    ];

    return {
      diagnosis: sortedDiseases.map(([diseaseId, score]) => ({
        id: diseaseId,
        ...medicalOntology.diseases[diseaseId],
        confidence: score,
        matchDetails: matchDetails[diseaseId]
      })),
      reasoning: {
        steps: reasoningSteps,
        inheritanceChain,
        symptomsAnalyzed: symptoms.length,
        matchedConditions: sortedDiseases.length
      }
    };
  };

  const getInheritanceChain = (parentId) => {
    const chain = [];
    let currentId = parentId;
    
    while (currentId && currentId !== 'owl:Disease') {
      const parent = medicalOntology.hierarchy[currentId];
      if (parent) {
        chain.push(parent.label);
        currentId = parent.parent;
      } else {
        break;
      }
    }
    
    chain.push('Disease');
    return chain.reverse();
  };

  const askAI = async () => {
    if (selectedSymptoms.length === 0) {
      alert('Please select at least one symptom');
      return;
    }
    setAiLoading(true);
    setAiResult(null);
    setAiError(null);

    // Convert symptom IDs to human-readable labels for the LLM
    const symptomLabels = selectedSymptoms.map(
      id => medicalOntology.symptoms[id]?.label || id
    );

    try {
      const res = await fetch('/api/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms: symptomLabels }),
      });
      const json = await res.json();
      if (!res.ok || json.error) {
        throw new Error(json.error || `HTTP ${res.status}`);
      }
      setAiResult(json.data);
    } catch (err) {
      setAiError(err.message);
    } finally {
      setAiLoading(false);
    }
  };

  const reset = () => {
    setSelectedSymptoms([]);
    setDiagnosis(null);
    setReasoning(null);
    setAiResult(null);
    setAiError(null);
  };

  return (
    <div className="medical-ai-container">
      <div className="medical-header">
        <h1>🏥 Medical Reasoner</h1>
        <p className="medical-subtitle">
          Symptom-based diagnostic reasoning using ontology structures
        </p>
        <div className="disclaimer">
          ⚠️ Educational demonstration only - Not for actual medical diagnosis
        </div>
        <div className="ontology-source">
          📂 Knowledge source: <code>{ontologySource}</code> &nbsp;·&nbsp;
          {Object.keys(medicalOntology.diseases).length} diseases &nbsp;·&nbsp;
          {Object.keys(medicalOntology.symptoms).length} symptoms &nbsp;·&nbsp;
          {Object.keys(medicalOntology.treatments).length} treatments
        </div>
      </div>

      <div className="medical-content">
        {/* Symptom Selection */}
        <div className="symptom-panel">
          <div className="symptom-panel-header">
            <h2>Select Symptoms</h2>
          </div>

          <div className="symptom-grid">
            {allSymptoms.map(symptom => (
              <button
                key={symptom.id}
                className={`symptom-chip ${selectedSymptoms.includes(symptom.id) ? 'selected' : ''}`}
                onClick={() => toggleSymptom(symptom.id)}
              >
                {symptom.label}
                {selectedSymptoms.includes(symptom.id) && <span className="check">✓</span>}
              </button>
            ))}
          </div>

          <div className="action-bar">
            <div className="selected-count">
              {selectedSymptoms.length} symptom{selectedSymptoms.length !== 1 ? 's' : ''} selected
            </div>
            <div className="action-buttons">
              <button className="btn-reset" onClick={reset} disabled={selectedSymptoms.length === 0}>
                Clear All
              </button>
              <button 
                className="btn-analyze" 
                onClick={performDiagnosis}
                disabled={selectedSymptoms.length === 0 || analyzing}
              >
                {analyzing ? '🤖 Analyzing...' : '🔍 Analyze Symptoms'}
              </button>
              <button
                className="btn-ask-ai"
                onClick={askAI}
                disabled={selectedSymptoms.length === 0 || aiLoading}
              >
                {aiLoading ? '⏳ Asking Ollama...' : '🦙 Ask AI (Ollama)'}
              </button>
            </div>
          </div>
        </div>

        {/* Ollama LLM Response Panel (Sprint 1) */}
        {aiLoading && (
          <div className="reasoning-process">
            <div className="ai-thinking">
              <div className="spinner"></div>
              <p>Asking Ollama llama3.2:3b… this may take a moment.</p>
            </div>
          </div>
        )}

        {aiError && (
          <div className="ai-error-panel">
            <h2>⚠️ Ollama Error</h2>
            <p>{aiError}</p>
            <p className="ai-error-hint">Make sure Ollama is running: <code>./start_llm.sh</code> and <code>ollama list</code> shows <code>llama3.2:3b</code>.</p>
          </div>
        )}

        {aiResult && (
          <div className="ai-result-panel">
            <div className="ai-result-header">
              <h2>🦙 Ollama Diagnosis</h2>
              <span className="ai-model-badge">{aiResult.model_used}</span>
            </div>
            <div className="ai-symptoms-line">
              Symptoms: {aiResult.symptoms_received?.join(', ')}
            </div>
            <div className="ai-result-body">
              {aiResult.diagnosis.split('\n').map((line, i) => (
                line.trim() ? <p key={i}>{line}</p> : <br key={i} />
              ))}
            </div>
            <div className="ai-reasoning-note">ℹ️ {aiResult.reasoning}</div>
            <div className="ai-disclaimer">⚠️ Educational only — not for real medical decisions.</div>
          </div>
        )}

        {/* AI Reasoning Process */}
        {analyzing && (
          <div className="reasoning-process">
            <div className="ai-thinking">
              <div className="spinner"></div>
              <p>AI is reasoning through medical ontology...</p>
            </div>
          </div>
        )}

        {/* Results */}
        {diagnosis && reasoning && (
          <div className="results-panel">
            {/* Reasoning Steps */}
            <div className="reasoning-steps">
              <h2>🧠 AI Reasoning Process</h2>
              <div className="steps-container">
                {reasoning.steps.map(step => (
                  <div key={step.step} className="reasoning-step">
                    <div className="step-number">{step.step}</div>
                    <div className="step-content">
                      <h3>{step.title}</h3>
                      <p>{step.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Diagnosis Results */}
            <div className="diagnosis-results">
              <h2>📋 Diagnostic Suggestions</h2>
              {diagnosis.map((disease, idx) => (
                <div key={disease.id} className={`diagnosis-card ${idx === 0 ? 'primary' : 'secondary'}`}>
                  <div className="diagnosis-header">
                    <div className="diagnosis-rank">#{idx + 1}</div>
                    <div className="diagnosis-info">
                      <h3>
                        {disease.label}
                        {disease.doid && (
                          <a
                            className="doid-badge"
                            href={`https://disease-ontology.org/do#${disease.doid.replace('DOID:','DOID_')}`}
                            target="_blank"
                            rel="noreferrer"
                            title="View in Disease Ontology"
                          >
                            {disease.doid}
                          </a>
                        )}
                        {disease.icd10Refs?.length > 0 && (
                          <span className="icd10-badge" title="ICD-10-CM code">
                            ICD-10: {disease.icd10Refs[0]}
                          </span>
                        )}
                      </h3>
                      <p className="disease-description">{disease.description}</p>
                      {disease.officialDef && disease.officialDef !== disease.description && (
                        <p className="official-definition">
                          <span className="do-label">📖 DO:</span> {disease.officialDef}
                        </p>
                      )}
                      {disease.synonyms?.length > 0 && (
                        <div className="synonym-row">
                          <span className="synonym-label">Also known as:</span>
                          {disease.synonyms.slice(0, 3).map((syn, i) => (
                            <span key={i} className="synonym-chip">{syn}</span>
                          ))}
                        </div>
                      )}
                    </div>
                    <div className="confidence-badge">
                      <div className="confidence-value">{disease.confidence.toFixed(1)}%</div>
                      <div className="confidence-label">Confidence</div>
                    </div>
                  </div>

                  <div className="diagnosis-body">
                    <div className="match-info">
                      <div className="info-item">
                        <strong>Matched Symptoms:</strong> {disease.matchDetails.matchCount} / {disease.matchDetails.totalSymptoms}
                      </div>
                      <div className="info-item">
                        <strong>Severity:</strong> 
                        <span className={`severity-badge ${disease.severity}`}>
                          {disease.severity.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    <div className="treatment-section">
                      <strong>Recommended Actions:</strong>
                      <ul className="treatment-list">
                        {disease.treatments.map(treatmentId => {
                          const treatment = medicalOntology.treatments[treatmentId];
                          return (
                            <li key={treatmentId} className={`treatment-item ${treatment.type}`}>
                              {treatment.label}
                              <span className="treatment-type">{treatment.type}</span>
                            </li>
                          );
                        })}
                      </ul>
                    </div>

                    {idx === 0 && (
                      <div className="ontology-path">
                        <strong>Ontology Classification:</strong>
                        <div className="inheritance-chain">
                          {reasoning.inheritanceChain.map((node, i) => (
                            <React.Fragment key={i}>
                              <span className="chain-node">{node}</span>
                              {i < reasoning.inheritanceChain.length - 1 && (
                                <span className="chain-arrow">→</span>
                              )}
                            </React.Fragment>
                          ))}
                          <span className="chain-arrow">→</span>
                          <span className="chain-node primary-node">{disease.label}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MedicalDiagnosisAI;
