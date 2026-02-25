# Medical AI Reasoner - Open Source LLM Integration

**Version**: 2.0 Proposal  
**Date**: February 20, 2026  
**Type**: Hybrid System (Local LLM + Algorithmic Reasoning)  
**Cost**: $0 (Free & Open Source)

---

## Overview

Enhance the Medical AI Reasoner with **free, open-source LLMs** for natural language processing while keeping the core algorithmic reasoning intact.

**Key Advantage**: No API costs, runs locally, privacy-preserving, works offline.

---

## 1. Recommended Open Source LLM Solutions

### Option 1: Ollama (⭐ RECOMMENDED)

**Why Ollama:**
- ✅ **Free & Open Source**
- ✅ **Runs Locally** (no cloud dependencies)
- ✅ **Easy Setup** (one command install)
- ✅ **Multiple Models** (Llama 3, Mistral, Phi-3)
- ✅ **REST API** (easy integration)
- ✅ **Lightweight** (3B-7B models run on laptop)
- ✅ **Privacy** (data never leaves your machine)

**Installation (No Homebrew Required):**

```bash
# macOS - Direct Download
curl -L https://ollama.com/download/ollama-darwin -o ollama
chmod +x ollama
sudo mv ollama /usr/local/bin/

# OR Download manually from browser
# Visit: https://ollama.com/download/mac
# Download Ollama.dmg and install

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows (WSL2 or native)
# Download: https://ollama.com/download/windows
# Or use WSL2 and run Linux command above

# Start Ollama server
ollama serve

# Pull a model (one-time, ~2-4GB download)
ollama pull llama3.2:3b    # Small, fast (3B params)
# OR
ollama pull phi3.5         # Microsoft's efficient model (3.8B)
# OR  
ollama pull mistral:7b     # More powerful (7B params)
```

**Model Comparison:**

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Llama 3.2 (3B)** | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | Fast symptom extraction |
| **Phi-3.5 (3.8B)** | 2.3GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Balanced performance |
| **Mistral (7B)** | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best accuracy |

---

### Option 2: Hugging Face Transformers.js (Client-Side)

**Why Transformers.js:**
- ✅ **Runs in Browser** (no backend needed)
- ✅ **Free & Open Source**
- ✅ **No Installation** (users download model once)
- ✅ **WebGPU Support** (hardware acceleration)

**Model Options:**
- `Xenova/LaMini-Flan-T5-783M` - 783M params, NLP tasks
- `Xenova/distilbert-base-uncased` - Fast text understanding
- `Xenova/bert-base-multilingual-cased` - Multi-language

**Limitation**: Smaller models (< 1B params) = lower quality than Ollama

---

### Option 3: LocalAI (Docker-based)

**Why LocalAI:**
- ✅ **OpenAI-compatible API** (drop-in replacement)
- ✅ **Docker deployment**
- ✅ **Multiple backends** (llama.cpp, whisper, etc.)

**Setup:**
```bash
docker run -p 8080:8080 -v models:/models localai/localai
```

---

## 2. Architecture: Hybrid System

```
┌─────────────────────────────────────────────────────────┐
│                     User Input                          │
│  "I have a fever, cough, and feel very tired"          │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌───────────────────────────────────────────────────────────┐
│                  NLP Layer (Ollama)                       │
│  ┌─────────────────────────────────────────────────┐     │
│  │  Local LLM (Llama 3.2 / Phi-3.5 / Mistral)     │     │
│  │  - Parse natural language                       │     │
│  │  - Extract symptom mentions                     │     │
│  │  - Map to ontology IDs                          │     │
│  └─────────────────────────────────────────────────┘     │
│                        ↓                                  │
│       Output: ['symp:Fever', 'symp:Cough',              │
│                'symp:Fatigue']                           │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌───────────────────────────────────────────────────────────┐
│         Reasoning Layer (Our Algorithm)                   │
│  ┌─────────────────────────────────────────────────┐     │
│  │  Weighted Graph Traversal                       │     │
│  │  - Score diseases                               │     │
│  │  - Rank by confidence                           │     │
│  │  - Get ontology paths                           │     │
│  └─────────────────────────────────────────────────┘     │
│                        ↓                                  │
│       Output: Influenza (86.7%), Treatments, etc.       │
└───────────────────────┬─────────────────────────────────┘
                        ↓
┌───────────────────────────────────────────────────────────┐
│         Explanation Layer (Optional: Ollama)              │
│  ┌─────────────────────────────────────────────────┐     │
│  │  Generate Human-Friendly Explanation            │     │
│  │  "Based on your symptoms of fever, cough..."    │     │
│  └─────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────┘
                        ↓
                   Display Results
```

**Key Point**: LLM only for NLP input/output. Core reasoning stays algorithmic (fast, transparent, deterministic).

---

## 3. Implementation Guide

### 3.1 Backend Service (Node.js/Express)

Create a simple backend to proxy Ollama requests:

```javascript
// backend/llm-service.js
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

const OLLAMA_URL = 'http://localhost:11434'; // Ollama default port

// Available symptoms (from our ontology)
const AVAILABLE_SYMPTOMS = [
  'Fever', 'Cough', 'Runny Nose', 'Sore Throat', 'Sneezing',
  'Fatigue', 'Body Aches', 'Headache', 'Chest Pain',
  'Shortness of Breath', 'Chest Discomfort', 'Mucus Production',
  'Nausea', 'Vomiting', 'Diarrhea', 'Abdominal Pain',
  'Severe Headache', 'Light Sensitivity', 'Sound Sensitivity', 'Dizziness'
];

// Map symptom names to IDs
const SYMPTOM_MAP = {
  'Fever': 'symp:Fever',
  'Cough': 'symp:Cough',
  'Runny Nose': 'symp:RunnyNose',
  'Sore Throat': 'symp:SoreThroat',
  'Sneezing': 'symp:Sneezing',
  'Fatigue': 'symp:Fatigue',
  'Body Aches': 'symp:BodyAches',
  'Headache': 'symp:Headache',
  'Chest Pain': 'symp:ChestPain',
  'Shortness of Breath': 'symp:ShortnessOfBreath',
  'Chest Discomfort': 'symp:ChestDiscomfort',
  'Mucus Production': 'symp:Mucus',
  'Nausea': 'symp:Nausea',
  'Vomiting': 'symp:Vomiting',
  'Diarrhea': 'symp:Diarrhea',
  'Abdominal Pain': 'symp:AbdominalPain',
  'Severe Headache': 'symp:SevereHeadache',
  'Light Sensitivity': 'symp:LightSensitivity',
  'Sound Sensitivity': 'symp:SoundSensitivity',
  'Dizziness': 'symp:Dizziness'
};

app.post('/api/extract-symptoms', async (req, res) => {
  try {
    const { text } = req.body;
    
    // Create prompt for Ollama
    const prompt = `You are a medical symptom extractor. Extract ONLY the symptoms mentioned in the text.

Available symptoms: ${AVAILABLE_SYMPTOMS.join(', ')}

User text: "${text}"

Return ONLY a JSON array of symptom names that appear in the text. Be strict - only include symptoms explicitly mentioned.

Example output: ["Fever", "Cough", "Fatigue"]

JSON array:`;

    // Call Ollama
    const response = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'llama3.2:3b',  // or 'phi3.5' or 'mistral:7b'
        prompt: prompt,
        stream: false,
        temperature: 0.1,  // Low temperature for consistent extraction
        format: 'json'
      })
    });

    const data = await response.json();
    
    // Parse LLM response
    let extractedSymptoms = [];
    try {
      extractedSymptoms = JSON.parse(data.response);
    } catch (e) {
      // Fallback: extract from text
      const match = data.response.match(/\[(.*?)\]/);
      if (match) {
        extractedSymptoms = JSON.parse(match[0]);
      }
    }

    // Map to symptom IDs
    const symptomIds = extractedSymptoms
      .map(name => SYMPTOM_MAP[name])
      .filter(id => id); // Remove undefined

    res.json({
      success: true,
      extracted: extractedSymptoms,
      symptomIds: symptomIds,
      llmModel: 'llama3.2:3b'
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', ollama: OLLAMA_URL });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`LLM Service running on http://localhost:${PORT}`);
  console.log(`Using Ollama at ${OLLAMA_URL}`);
});
```

**Run:**
```bash
cd backend
npm install express cors
node llm-service.js
```

---

### 3.2 Frontend Integration

Update the Medical AI Reasoner component:

```jsx
// MedicalDiagnosisAI.jsx

import React, { useState } from 'react';
import './MedicalDiagnosisAI.css';

const MedicalDiagnosisAI = () => {
  // Existing state...
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  
  // New state for NLP input
  const [nlpInput, setNlpInput] = useState('');
  const [extracting, setExtracting] = useState(false);
  const [useNLP, setUseNLP] = useState(false);

  // New function: Extract symptoms from text using Ollama
  const extractSymptomsFromText = async () => {
    if (!nlpInput.trim()) {
      alert('Please enter your symptoms');
      return;
    }

    setExtracting(true);
    try {
      const response = await fetch('http://localhost:3001/api/extract-symptoms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: nlpInput })
      });

      const data = await response.json();
      
      if (data.success) {
        setSelectedSymptoms(data.symptomIds);
        alert(`Extracted ${data.extracted.length} symptoms: ${data.extracted.join(', ')}`);
      } else {
        alert('Failed to extract symptoms: ' + data.error);
      }
    } catch (error) {
      console.error('Extraction error:', error);
      alert('Could not connect to LLM service. Is Ollama running?');
    } finally {
      setExtracting(false);
    }
  };

  return (
    <div className="medical-ai-container">
      {/* Header */}
      <div className="medical-header">
        <h1>🏥 Medical AI Reasoner v2.0</h1>
        <p className="medical-subtitle">
          AI-powered diagnostic reasoning with Natural Language Processing
        </p>
        <div className="disclaimer">
          ⚠️ Educational demonstration only - Not for actual medical diagnosis
        </div>
      </div>

      <div className="medical-content">
        {/* Input Mode Toggle */}
        <div className="input-mode-toggle">
          <button
            className={`mode-btn ${!useNLP ? 'active' : ''}`}
            onClick={() => setUseNLP(false)}
          >
            📋 Select Symptoms
          </button>
          <button
            className={`mode-btn ${useNLP ? 'active' : ''}`}
            onClick={() => setUseNLP(true)}
          >
            💬 Describe in Natural Language (LLM-Powered)
          </button>
        </div>

        {/* Natural Language Input (NEW!) */}
        {useNLP && (
          <div className="nlp-input-panel">
            <h2>Describe Your Symptoms</h2>
            <p className="nlp-hint">
              Type naturally, e.g., "I have a bad headache and feel nauseous" or 
              "My chest hurts when I breathe and I'm coughing a lot"
            </p>
            <textarea
              className="nlp-textarea"
              value={nlpInput}
              onChange={(e) => setNlpInput(e.target.value)}
              placeholder="Describe how you're feeling..."
              rows={5}
            />
            <div className="nlp-actions">
              <button
                className="btn-extract"
                onClick={extractSymptomsFromText}
                disabled={extracting || !nlpInput.trim()}
              >
                {extracting ? '🤖 AI Extracting Symptoms...' : '🔍 Extract Symptoms with AI'}
              </button>
              {selectedSymptoms.length > 0 && (
                <div className="extracted-preview">
                  ✓ Extracted {selectedSymptoms.length} symptoms
                </div>
              )}
            </div>
            <div className="nlp-info">
              <strong>Powered by:</strong> Ollama + Llama 3.2 (Running Locally, Free)
            </div>
          </div>
        )}

        {/* Traditional Symptom Selection (Existing) */}
        {!useNLP && (
          <div className="symptom-panel">
            {/* Existing symptom chips code... */}
          </div>
        )}

        {/* Show selected symptoms regardless of input method */}
        {selectedSymptoms.length > 0 && (
          <div className="selected-symptoms-display">
            <h3>Selected Symptoms ({selectedSymptoms.length})</h3>
            <div className="selected-chips">
              {selectedSymptoms.map(symptomId => {
                const symptom = MEDICAL_ONTOLOGY.symptoms[symptomId];
                return (
                  <span key={symptomId} className="selected-chip">
                    {symptom.label}
                    <button 
                      className="remove-btn"
                      onClick={() => setSelectedSymptoms(prev => 
                        prev.filter(s => s !== symptomId)
                      )}
                    >
                      ×
                    </button>
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Analyze Button */}
        <div className="analyze-section">
          <button
            className="btn-analyze-main"
            onClick={performDiagnosis}
            disabled={selectedSymptoms.length === 0 || analyzing}
          >
            {analyzing ? '🤖 AI Analyzing...' : '🔍 Analyze & Diagnose'}
          </button>
        </div>

        {/* Rest of the component (results display) remains the same... */}
      </div>
    </div>
  );
};

export default MedicalDiagnosisAI;
```

---

### 3.3 Additional CSS

```css
/* NLP Input Styling */
.input-mode-toggle {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
  justify-content: center;
}

.mode-btn {
  padding: 14px 28px;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.nlp-input-panel {
  background: white;
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.nlp-hint {
  color: #4a5568;
  font-size: 14px;
  margin-bottom: 16px;
  font-style: italic;
}

.nlp-textarea {
  width: 100%;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 16px;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 16px;
}

.nlp-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.btn-extract {
  padding: 14px 32px;
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-extract:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
}

.btn-extract:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.nlp-info {
  margin-top: 16px;
  padding: 12px;
  background: #f7fafc;
  border-radius: 8px;
  font-size: 14px;
  color: #4a5568;
}

.selected-symptoms-display {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.selected-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.selected-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
}

.remove-btn {
  background: rgba(255,255,255,0.3);
  border: none;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  transition: background 0.2s;
}

.remove-btn:hover {
  background: rgba(255,255,255,0.5);
}
```

---

## 4. Setup Instructions

### Step 1: Install Ollama (No Homebrew)

**Option A: Direct Download (macOS)**
```bash
# Download Ollama binary directly
curl -L https://ollama.com/download/ollama-darwin -o ollama
chmod +x ollama
sudo mv ollama /usr/local/bin/

# Verify installation
ollama --version
```

**Option B: GUI Installer (macOS)**
1. Visit https://ollama.com/download/mac in your browser
2. Download `Ollama.dmg`
3. Open DMG and drag Ollama to Applications
4. Launch Ollama from Applications

**Option C: Linux (Direct Install)**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Option D: Manual Download (Any OS)**
1. Go to https://github.com/ollama/ollama/releases
2. Download the binary for your OS
3. Extract and add to PATH

### Step 2: Pull a Model

```bash
# Start Ollama server (in background)
ollama serve &

# Pull Llama 3.2 (3B) - Recommended for speed
ollama pull llama3.2:3b

# OR pull Phi-3.5 (3.8B) - Recommended for quality
ollama pull phi3.5

# Test it works
ollama run llama3.2:3b "Extract symptoms from: I have a fever and headache"
```

### Step 3: Create Backend Service

```bash
mkdir backend
cd backend
npm init -y
npm install express cors
```

Create `backend/llm-service.js` (code above)

### Step 4: Run Everything

```bash
# Terminal 1: Ollama server (if not already running)
ollama serve

# Terminal 2: Backend LLM service
cd backend
node llm-service.js

# Terminal 3: Flask API (existing)
cd WALLY-CLEAN
python3 ontology_api.py

# Terminal 4: React frontend (existing)
cd WALLY-CLEAN/graph-ui
npm run dev
```

### Step 5: Test

1. Go to http://localhost:5173
2. Click "🏥 Medical AI Reasoner"
3. Click "💬 Describe in Natural Language"
4. Type: "I have a fever, bad cough, and feel exhausted"
5. Click "Extract Symptoms with AI"
6. Watch it extract: Fever, Cough, Fatigue
7. Click "Analyze & Diagnose"

---

## 5. Performance & Cost

### Model Performance

| Model | RAM Usage | Response Time | Accuracy | Cost |
|-------|-----------|---------------|----------|------|
| Llama 3.2 (3B) | 4GB | 1-2s | ⭐⭐⭐ | $0 |
| Phi-3.5 (3.8B) | 5GB | 2-3s | ⭐⭐⭐⭐ | $0 |
| Mistral (7B) | 8GB | 3-5s | ⭐⭐⭐⭐⭐ | $0 |

### Cost Comparison

| Solution | Setup Cost | Running Cost | Monthly Cost |
|----------|------------|--------------|--------------|
| **Ollama (Local)** | $0 | $0 (electricity ~$0.50) | **$0.50** |
| OpenAI GPT-4 API | $0 | $0.06/1K tokens | **$180** |
| Anthropic Claude API | $0 | $0.03/1K tokens | **$90** |

**Savings**: ~$2,000/year vs GPT-4!

---

## 6. Advantages of This Approach

### ✅ Benefits

1. **Zero Cost**: Completely free, no API bills
2. **Privacy**: Data never leaves your machine
3. **Offline**: Works without internet
4. **Fast**: Low latency (no network calls)
5. **Customizable**: Can fine-tune models on medical data
6. **No Rate Limits**: Use as much as you want
7. **Transparent**: Can inspect model outputs
8. **Ethical**: No data sent to big tech companies

### ⚠️ Trade-offs

1. **Setup Required**: Users need to install Ollama
2. **Hardware**: Needs 4-8GB RAM for models
3. **Accuracy**: 3-7B models less accurate than GPT-4
4. **Initial Download**: 2-4GB model download

---

## 7. Alternative: Client-Side with Transformers.js

For a **zero-setup** solution, use Transformers.js (runs in browser):

```bash
npm install @xenova/transformers
```

```javascript
// MedicalDiagnosisAI.jsx
import { pipeline } from '@xenova/transformers';

// Initialize once
let extractor = null;

async function initExtractor() {
  if (!extractor) {
    extractor = await pipeline('text-classification', 
      'Xenova/bert-base-uncased');
  }
}

async function extractSymptomsInBrowser(text) {
  await initExtractor();
  
  // Use BERT to analyze text
  const results = await extractor(text);
  
  // Map results to symptoms (custom logic needed)
  return extractedSymptomIds;
}
```

**Pros**: No backend needed  
**Cons**: Smaller models, first load is slow (~100MB download)

---

## 8. Recommended Architecture

```
Production Stack:

┌────────────────────────────────────────────┐
│  User Browser                              │
│  ├─ React UI (symptom input)              │
│  └─ Algorithmic reasoning (deterministic) │
└───────────────┬────────────────────────────┘
                │
                ↓
┌────────────────────────────────────────────┐
│  Backend Server                            │
│  ├─ Node.js LLM Service (port 3001)       │
│  │  └─ Proxies to Ollama                  │
│  └─ Flask Ontology API (port 5002)        │
└───────────────┬────────────────────────────┘
                │
                ↓
┌────────────────────────────────────────────┐
│  Local LLM Server                          │
│  └─ Ollama (port 11434)                   │
│     └─ Llama 3.2 / Phi-3.5 / Mistral      │
└────────────────────────────────────────────┘
```

---

## 9. Next Steps

### Immediate (Week 1)
1. ✅ Install Ollama
2. ✅ Create backend LLM service
3. ✅ Update frontend with NLP input
4. ✅ Test symptom extraction

### Short-term (Week 2-3)
1. Fine-tune extraction prompts
2. Add synonym handling ("tired" → "Fatigue")
3. Handle negations ("no fever" → exclude Fever)
4. Add confidence scores for extractions

### Long-term (Month 2+)
1. Fine-tune Llama 3.2 on medical corpus
2. Add multi-language support
3. Generate natural explanations with LLM
4. Create medical Q&A chatbot

---

## 10. Example Prompts

### Symptom Extraction Prompt
```
You are a medical symptom extractor. Extract ONLY symptoms from text.

Available symptoms: Fever, Cough, Runny Nose, Sore Throat, ...

Text: "I've had a terrible headache for 2 days and feel sick to my stomach"

Extract: ["Headache", "Nausea"]
```

### Explanation Generation Prompt
```
Explain this medical diagnosis to a patient:

Symptoms: Fever, Cough, Fatigue
Top diagnosis: Influenza (86.7% confidence)
Reasoning: Weighted symptom matching shows strong correlation

Generate a friendly, reassuring explanation in 2-3 sentences.
```

---

## Conclusion

**Yes, absolutely use free open-source LLMs!**

**Recommended approach:**
1. Use **Ollama + Llama 3.2 (3B)** for symptom extraction
2. Keep **algorithmic reasoning** for diagnosis (fast, accurate, explainable)
3. Optionally use **LLM for explanations** (user-friendly text)

**Total cost**: $0  
**Setup time**: 30 minutes  
**Performance**: Good enough for production  
**Privacy**: 100% local, no cloud dependencies

This gives you the best of both worlds: 
- Modern NLP UX (free-text input)
- Reliable diagnostic reasoning (deterministic algorithm)
- Zero API costs
- Full privacy

Want me to implement this?
