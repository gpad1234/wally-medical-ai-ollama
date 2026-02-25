import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3001;
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';

// CORS configuration for remote access
app.use(cors({
  origin: '*',  // In production, specify your frontend domain
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'X-API-Key']
}));

app.use(express.json({ limit: '1mb' }));

// Request logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'Medical AI LLM Service',
    model: 'llama3.2:3b',
    ollamaUrl: OLLAMA_URL,
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Symptom extraction endpoint
app.post('/api/extract-symptoms', async (req, res) => {
  const { text } = req.body;
  
  if (!text || typeof text !== 'string') {
    return res.status(400).json({ 
      success: false, 
      error: 'Missing or invalid "text" field. Expected: {"text": "symptom description"}' 
    });
  }

  if (text.length > 500) {
    return res.status(400).json({
      success: false,
      error: 'Text too long. Maximum 500 characters.'
    });
  }

  console.log(`[${new Date().toISOString()}] Extracting symptoms from: "${text}"`);

  try {
    const prompt = `You are a medical symptom extraction assistant. Extract ONLY the symptom names from the following text. Return ONLY a comma-separated list of symptoms, nothing else.

Valid symptoms include: Fever, Cough, Fatigue, Shortness of Breath, Headache, Sore Throat, Runny Nose, Body Aches, Nausea, Vomiting, Diarrhea, Chest Pain, Wheezing, Loss of Taste or Smell, Rash, Joint Pain, Confusion, Seizures, Sensitivity to Light, Stiff Neck

Text: "${text}"

Extracted symptoms (comma-separated):`;

    const response = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'llama3.2:3b',
        prompt: prompt,
        stream: false,
        options: {
          temperature: 0.1,
          num_predict: 100,
          stop: ['\n\n', 'Text:', 'Note:', 'Explanation:']
        }
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Ollama API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    const extractedText = data.response.trim();
    
    // Parse comma-separated symptoms
    const symptoms = extractedText
      .split(/[,\n]/)
      .map(s => s.trim())
      .filter(s => s.length > 0 && s.length < 50)
      .map(s => s.replace(/^(and|or|\d+\.|\-|\*)\s+/gi, ''))
      .map(s => {
        // Capitalize first letter of each word
        return s.split(' ')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ');
      })
      .filter((s, idx, arr) => arr.indexOf(s) === idx); // Remove duplicates

    // Convert to standardized symptom IDs
    const symptomIds = symptoms.map(name => `symp:${name.replace(/\s+/g, '')}`);

    console.log(`[${new Date().toISOString()}] Extracted: ${symptoms.join(', ')}`);

    res.json({
      success: true,
      extracted: symptoms,
      symptomIds: symptomIds,
      llmModel: 'llama3.2:3b',
      rawResponse: extractedText,
      processingTime: data.total_duration ? `${(data.total_duration / 1000000000).toFixed(2)}s` : 'N/A'
    });

  } catch (error) {
    console.error('LLM extraction error:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      fallback: 'Please try manual symptom selection or restart Ollama service'
    });
  }
});

// Test endpoint for quick verification
app.get('/api/test', async (req, res) => {
  try {
    const response = await fetch(`${OLLAMA_URL}/api/tags`);
    const data = await response.json();
    
    res.json({
      success: true,
      message: 'Ollama connection successful',
      models: data.models || []
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Cannot connect to Ollama',
      details: error.message
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.method} ${req.path} does not exist`,
    availableEndpoints: [
      'GET /api/health',
      'POST /api/extract-symptoms',
      'GET /api/test'
    ]
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log('═══════════════════════════════════════════════════════');
  console.log('🤖 Medical AI LLM Service');
  console.log('═══════════════════════════════════════════════════════');
  console.log(`📡 Server: http://0.0.0.0:${PORT}`);
  console.log(`🔗 Ollama: ${OLLAMA_URL}`);
  console.log(`📋 Health: http://localhost:${PORT}/api/health`);
  console.log(`🧪 Test: http://localhost:${PORT}/api/test`);
  console.log('═══════════════════════════════════════════════════════');
  console.log('🏥 Ready to extract symptoms!');
  console.log('═══════════════════════════════════════════════════════');
});
