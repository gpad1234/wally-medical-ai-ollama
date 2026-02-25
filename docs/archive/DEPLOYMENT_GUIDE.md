# Medical AI Reasoner - Deployment Guide

**Version**: 2.0 with Ollama LLM Integration  
**Date**: February 20, 2026  
**Status**: Production Ready

---

## 🎯 System Overview

```
┌─────────────────────────────────────────────────────────┐
│  React Frontend (Port 5173)                             │
│  - Medical AI UI                                        │
│  - Symptom input (click or NLP)                         │
│  - Results visualization                                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├─→ http://localhost:3001 (LLM Service)
                 └─→ http://localhost:5002 (Ontology API)
                 
┌─────────────────────────────────────────────────────────┐
│  Node.js Backend (Port 3001)                            │
│  - LLM symptom extraction service                       │
│  - Proxies requests to Ollama                           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Ollama Server (Port 11434)                             │
│  - Llama 3.2 (3B) model                                 │
│  - Local LLM processing                                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Flask Backend (Port 5002)                              │
│  - Ontology API (existing)                              │
│  - Graph operations                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### System Requirements
- macOS / Linux / Windows (WSL2)
- Node.js 18+ (`node --version`)
- Python 3.12+ (`python3 --version`)
- 8GB RAM minimum (for Llama 3.2 3B model)
- 5GB free disk space (for model)

### Port Requirements
- 5173: React dev server
- 3001: LLM service
- 5002: Flask ontology API
- 11434: Ollama server

---

## 🚀 Installation

### Step 1: Install Ollama

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Verify:**
```bash
ollama --version
# Should output: ollama version x.x.x
```

### Step 2: Pull LLM Model

```bash
# Start Ollama server (if not auto-started)
ollama serve &

# Pull Llama 3.2 3B model (~2GB download)
ollama pull llama3.2:3b

# Test it works
ollama run llama3.2:3b "Hello!"
# Press Ctrl+D to exit
```

**Alternative models:**
```bash
# Smaller and faster (1.3B, ~900MB)
ollama pull llama3.2:1b

# Better accuracy (7B, ~4GB)
ollama pull mistral:7b
```

### Step 3: Create LLM Backend Service

```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN
mkdir -p backend
cd backend
```

Create `package.json`:
```bash
cat > package.json << 'EOF'
{
  "name": "medical-ai-llm-service",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node llm-service.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  }
}
EOF
```

Install dependencies:
```bash
npm install
```

### Step 4: Install Frontend Dependencies

```bash
cd ../graph-ui
npm install @xenova/transformers
```

---

## 📝 Configuration Files

### File 1: `backend/llm-service.js`

See: `MEDICAL_AI_LLM_INTEGRATION.md` section 3.1 for full code.

Quick create:
```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN/backend
cat > llm-service.js << 'EOFJS'
# (Copy the Node.js code from MEDICAL_AI_LLM_INTEGRATION.md)
EOFJS
```

### File 2: Update `graph-ui/src/components/Ontology/MedicalDiagnosisAI.jsx`

Add NLP functionality - see implementation in `MEDICAL_AI_LLM_INTEGRATION.md` section 3.2.

---

## 🏃 Running the System

### Development Mode (4 Terminals)

**Terminal 1: Ollama Server**
```bash
ollama serve
```

**Terminal 2: LLM Service**
```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN/backend
npm start
```

**Terminal 3: Flask API**
```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN
python3 ontology_api.py
```

**Terminal 4: React Frontend**
```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN/graph-ui
npm run dev
```

### Quick Start Script

Create `start_all.sh`:
```bash
#!/bin/bash
# Save as: /Users/gp/claude-code/startup-one/WALLY-CLEAN/start_all.sh

cd "$(dirname "$0")"

echo "🚀 Starting Medical AI Reasoner..."

# Start Ollama in background
echo "📦 Starting Ollama..."
ollama serve > logs/ollama.log 2>&1 &
OLLAMA_PID=$!
sleep 2

# Start LLM service
echo "🤖 Starting LLM service..."
cd backend
npm start > ../logs/llm-service.log 2>&1 &
LLM_PID=$!
cd ..

# Start Flask API
echo "🔥 Starting Flask API..."
python3 ontology_api.py > logs/flask.log 2>&1 &
FLASK_PID=$!

# Start React frontend
echo "⚛️  Starting React..."
cd graph-ui
npm run dev > ../logs/react.log 2>&1 &
REACT_PID=$!
cd ..

# Save PIDs
echo "$OLLAMA_PID $LLM_PID $FLASK_PID $REACT_PID" > .pids

echo ""
echo "✅ All services started!"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🤖 LLM Service: http://localhost:3001"
echo "🔥 Flask API: http://localhost:5002"
echo "📦 Ollama: http://localhost:11434"
echo ""
echo "📋 Logs are in ./logs/"
echo "🛑 To stop: ./stop_all.sh"
```

Make executable:
```bash
chmod +x start_all.sh
```

### Stop Script

Create `stop_all.sh`:
```bash
#!/bin/bash
# Save as: /Users/gp/claude-code/startup-one/WALLY-CLEAN/stop_all.sh

cd "$(dirname "$0")"

if [ -f .pids ]; then
  echo "🛑 Stopping all services..."
  read -r OLLAMA_PID LLM_PID FLASK_PID REACT_PID < .pids
  
  kill $OLLAMA_PID 2>/dev/null && echo "  ✓ Ollama stopped"
  kill $LLM_PID 2>/dev/null && echo "  ✓ LLM service stopped"
  kill $FLASK_PID 2>/dev/null && echo "  ✓ Flask stopped"
  kill $REACT_PID 2>/dev/null && echo "  ✓ React stopped"
  
  rm .pids
  echo "✅ All services stopped"
else
  echo "No running services found"
fi
```

Make executable:
```bash
chmod +x stop_all.sh
```

---

## 🧪 Testing

### 1. Health Checks

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check LLM service
curl http://localhost:3001/api/health

# Check Flask API
curl http://localhost:5002/api/ontology/health
```

### 2. Test Symptom Extraction

```bash
curl -X POST http://localhost:3001/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "I have a fever and bad cough"}'
```

Expected response:
```json
{
  "success": true,
  "extracted": ["Fever", "Cough"],
  "symptomIds": ["symp:Fever", "symp:Cough"],
  "llmModel": "llama3.2:3b"
}
```

### 3. End-to-End Test

1. Go to http://localhost:5173
2. Click "🏥 Medical AI Reasoner"
3. Click "💬 Describe in Natural Language"
4. Type: "I have a fever, bad cough, and feel exhausted"
5. Click "Extract Symptoms with AI"
6. Verify it extracts: Fever, Cough, Fatigue
7. Click "Analyze & Diagnose"
8. Should show: Influenza as top diagnosis

---

## 🐛 Troubleshooting

### Issue: Ollama not found

```bash
# Check if installed
which ollama

# Reinstall
curl -fsSL https://ollama.com/install.sh | sh
```

### Issue: Model not found

```bash
# List installed models
ollama list

# Pull if missing
ollama pull llama3.2:3b
```

### Issue: Port already in use

```bash
# Check what's using port
lsof -i :3001

# Kill process
kill -9 <PID>
```

### Issue: LLM service connection refused

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start if not running
ollama serve &
```

### Issue: Slow extraction (> 5 seconds)

Try faster model:
```bash
ollama pull llama3.2:1b
```

Update `backend/llm-service.js`:
```javascript
model: 'llama3.2:1b'  // Change from 3b to 1b
```

---

## 📊 Performance Tuning

### Model Selection

| Model | Size | Speed | Accuracy | RAM |
|-------|------|-------|----------|-----|
| llama3.2:1b | 900MB | ⚡⚡⚡ | ⭐⭐ | 2GB |
| llama3.2:3b | 2GB | ⚡⚡ | ⭐⭐⭐ | 4GB |
| mistral:7b | 4GB | ⚡ | ⭐⭐⭐⭐⭐ | 8GB |

### Optimization Settings

In `backend/llm-service.js`:

```javascript
// Faster, less accurate
{
  model: 'llama3.2:3b',
  temperature: 0.1,      // Lower = more deterministic
  num_predict: 50,       // Limit output tokens
  num_ctx: 512           // Smaller context window
}

// Slower, more accurate
{
  model: 'mistral:7b',
  temperature: 0.3,
  num_predict: 200,
  num_ctx: 2048
}
```

---

## 🚢 Production Deployment

### Option 1: Docker Deployment

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    command: serve
    
  llm-service:
    build: ./backend
    ports:
      - "3001:3001"
    depends_on:
      - ollama
    environment:
      - OLLAMA_URL=http://ollama:11434
      
  flask-api:
    build: .
    ports:
      - "5002:5002"
    command: python3 ontology_api.py
    
  frontend:
    build: ./graph-ui
    ports:
      - "80:80"
    depends_on:
      - llm-service
      - flask-api

volumes:
  ollama-data:
```

Deploy:
```bash
docker-compose up -d
```

### Option 2: systemd Services (Linux)

Create service files in `/etc/systemd/system/`:

**ollama.service:**
```ini
[Unit]
Description=Ollama LLM Server
After=network.target

[Service]
Type=simple
User=gp
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
```

**medical-ai-llm.service:**
```ini
[Unit]
Description=Medical AI LLM Service
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=gp
WorkingDirectory=/path/to/WALLY-CLEAN/backend
ExecStart=/usr/bin/node llm-service.js
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ollama medical-ai-llm
sudo systemctl start ollama medical-ai-llm
```

### Option 3: PM2 (Process Manager)

```bash
npm install -g pm2

# Start all services
pm2 start ecosystem.config.js

# View status
pm2 status

# View logs
pm2 logs

# Stop all
pm2 stop all
```

Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [
    {
      name: 'ollama',
      script: 'ollama',
      args: 'serve'
    },
    {
      name: 'llm-service',
      script: './backend/llm-service.js',
      cwd: '/path/to/WALLY-CLEAN'
    },
    {
      name: 'flask-api',
      script: 'python3',
      args: 'ontology_api.py',
      cwd: '/path/to/WALLY-CLEAN'
    }
  ]
};
```

---

## 📈 Monitoring

### Logs Directory Structure

```
WALLY-CLEAN/logs/
├── ollama.log          # Ollama server logs
├── llm-service.log     # LLM service logs
├── flask.log           # Flask API logs
└── react.log           # React dev server logs
```

### Log Rotation

Create `logrotate.conf`:
```
/path/to/WALLY-CLEAN/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### Health Check Script

Create `health_check.sh`:
```bash
#!/bin/bash

echo "🏥 Medical AI System Health Check"
echo "=================================="

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null; then
  echo "✅ Ollama: Running"
else
  echo "❌ Ollama: Down"
fi

# Check LLM Service
if curl -s http://localhost:3001/api/health > /dev/null; then
  echo "✅ LLM Service: Running"
else
  echo "❌ LLM Service: Down"
fi

# Check Flask
if curl -s http://localhost:5002/api/ontology/health > /dev/null; then
  echo "✅ Flask API: Running"
else
  echo "❌ Flask API: Down"
fi

# Check React
if curl -s http://localhost:5173 > /dev/null; then
  echo "✅ React Frontend: Running"
else
  echo "❌ React Frontend: Down"
fi
```

---

## 🔐 Security Considerations

### Production Checklist

- [ ] Run services as non-root user
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for specific origins
- [ ] Add rate limiting to LLM service
- [ ] Implement API authentication
- [ ] Use HTTPS (nginx reverse proxy)
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor resource usage
- [ ] Backup model data

### Example: Rate Limiting

Add to `backend/llm-service.js`:
```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/extract-symptoms', limiter);
```

---

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Llama 3.2 Model Card](https://ollama.com/library/llama3.2)
- [Express.js Guide](https://expressjs.com/)
- [Medical AI Tech Spec](./MEDICAL_AI_TECH_SPEC.md)
- [LLM Integration Guide](./MEDICAL_AI_LLM_INTEGRATION.md)

---

## 🆘 Support

### Getting Help

1. Check logs: `tail -f logs/*.log`
2. Verify services: `./health_check.sh`
3. Review documentation in `/WALLY-CLEAN/*.md`
4. Check GitHub issues

### Common Commands

```bash
# Restart everything
./stop_all.sh && ./start_all.sh

# Check service status
ps aux | grep -E "(ollama|node|python|vite)"

# View realtime logs
tail -f logs/*.log

# Test extraction
curl -X POST http://localhost:3001/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "fever and cough"}'
```

---

**Last Updated**: February 20, 2026  
**Version**: 2.0  
**Status**: Production Ready  
**Maintainer**: GitHub Copilot
