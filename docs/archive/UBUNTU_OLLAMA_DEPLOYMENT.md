# Ubuntu Linux Ollama Deployment Guide

**Target**: DigitalOcean Droplet (or any Ubuntu Linux server)  
**Purpose**: Deploy Ollama LLM service for Medical AI Reasoner  
**Date**: February 20, 2026

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Local Development Machine (macOS 12.7.6)              │
│  - React Frontend (localhost:5173)                     │
│  - Flask API (localhost:5002)                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTPS/HTTP
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Ubuntu Droplet (your-server.com)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  nginx Reverse Proxy (Port 80/443)              │  │
│  └────────────┬─────────────────────────────────────┘  │
│               ↓                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Node.js LLM Service (Port 3001)                │  │
│  └────────────┬─────────────────────────────────────┘  │
│               ↓                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Ollama Server (Port 11434)                     │  │
│  │  Model: llama3.2:3b (2GB)                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### DigitalOcean Droplet Requirements

**Minimum Specs:**
- **OS**: Ubuntu 22.04 LTS (64-bit)
- **RAM**: 4GB (for llama3.2:3b model)
- **Storage**: 10GB SSD
- **CPU**: 2 vCPUs
- **Price**: ~$24/month (Basic Droplet)

**Recommended Specs:**
- **RAM**: 8GB (for faster inference)
- **Storage**: 20GB SSD
- **CPU**: 4 vCPUs
- **Price**: ~$48/month (Better performance)

### What You'll Need
- DigitalOcean account
- SSH key for authentication
- Domain name (optional, can use IP address)

---

## 🚀 Step-by-Step Deployment

### Step 1: Create Ubuntu Droplet

#### Via DigitalOcean Web UI:

1. Log in to [DigitalOcean](https://cloud.digitalocean.com/)
2. Click "Create" → "Droplets"
3. Choose:
   - **Image**: Ubuntu 22.04 (LTS) x64
   - **Plan**: Basic
   - **CPU**: Regular Intel ($24/mo for 4GB RAM)
   - **Datacenter**: Closest to your location
   - **Authentication**: SSH key (recommended) or password
   - **Hostname**: `medical-ai-llm`
4. Click "Create Droplet"
5. Wait 1-2 minutes for creation
6. Note your droplet's IP address (e.g., `159.203.123.45`)

#### Via DigitalOcean CLI (doctl):

```bash
# Install doctl
brew install doctl  # On another machine with Homebrew

# Authenticate
doctl auth init

# Create droplet
doctl compute droplet create medical-ai-llm \
  --image ubuntu-22-04-x64 \
  --size s-2vcpu-4gb \
  --region nyc3 \
  --ssh-keys YOUR_SSH_KEY_ID
```

---

### Step 2: Initial Server Setup

#### SSH into your droplet:

```bash
# Replace with your droplet IP
ssh root@159.203.123.45
```

#### Update system:

```bash
apt update && apt upgrade -y
```

#### Create non-root user:

```bash
adduser deployer
usermod -aG sudo deployer
su - deployer
```

#### Install Docker (alternative to direct install):

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker deployer
```

---

### Step 3: Install Ollama on Ubuntu

```bash
# Method 1: Official installation script (recommended)
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Start Ollama service (auto-starts on boot)
sudo systemctl status ollama

# If not running, start it
sudo systemctl start ollama
sudo systemctl enable ollama
```

#### Test Ollama:

```bash
# Pull the model (this will take 2-5 minutes)
ollama pull llama3.2:3b

# Test it works
ollama run llama3.2:3b "Hello, extract symptoms from: fever and cough"

# Press Ctrl+D to exit
```

Expected output:
```
Based on the input, I extracted the following symptoms:
- Fever
- Cough
```

---

### Step 4: Install Node.js

```bash
# Install Node.js 20.x LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x
```

---

### Step 5: Deploy LLM Service

#### Create project directory:

```bash
mkdir -p ~/medical-ai-backend
cd ~/medical-ai-backend
```

#### Create `package.json`:

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

#### Create `llm-service.js`:

```bash
cat > llm-service.js << 'EOFJS'
import express from 'express';
import cors from 'cors';

const app = express();
const PORT = 3001;
const OLLAMA_URL = 'http://localhost:11434';

// CORS configuration for remote access
app.use(cors({
  origin: '*',  // In production, specify your frontend domain
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

app.use(express.json());

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'Medical AI LLM Service',
    model: 'llama3.2:3b',
    timestamp: new Date().toISOString()
  });
});

// Symptom extraction endpoint
app.post('/api/extract-symptoms', async (req, res) => {
  const { text } = req.body;
  
  if (!text || typeof text !== 'string') {
    return res.status(400).json({ 
      success: false, 
      error: 'Missing or invalid "text" field' 
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
          stop: ['\n\n', 'Text:', 'Note:']
        }
      })
    });

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.status}`);
    }

    const data = await response.json();
    const extractedText = data.response.trim();
    
    // Parse comma-separated symptoms
    const symptoms = extractedText
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0)
      .map(s => s.replace(/^(and|or)\s+/i, ''))
      .map(s => s.charAt(0).toUpperCase() + s.slice(1).toLowerCase());

    // Convert to standardized symptom IDs
    const symptomIds = symptoms.map(name => `symp:${name}`);

    console.log(`[${new Date().toISOString()}] Extracted: ${symptoms.join(', ')}`);

    res.json({
      success: true,
      extracted: symptoms,
      symptomIds: symptomIds,
      llmModel: 'llama3.2:3b',
      rawResponse: extractedText
    });

  } catch (error) {
    console.error('LLM extraction error:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      fallback: 'Please try manual symptom selection'
    });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🤖 Medical AI LLM Service running on port ${PORT}`);
  console.log(`📡 Ollama URL: ${OLLAMA_URL}`);
  console.log(`🏥 Ready to extract symptoms!`);
});
EOFJS
```

#### Install dependencies:

```bash
npm install
```

#### Test the service:

```bash
# Start the service
node llm-service.js &

# Test it
curl -X POST http://localhost:3001/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "I have a fever and cough"}'

# Should return:
# {"success":true,"extracted":["Fever","Cough"],...}
```

---

### Step 6: Setup systemd Service (Auto-start on Boot)

#### Create systemd service file:

```bash
sudo nano /etc/systemd/system/medical-ai-llm.service
```

Paste this configuration:

```ini
[Unit]
Description=Medical AI LLM Service
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=deployer
WorkingDirectory=/home/deployer/medical-ai-backend
ExecStart=/usr/bin/node llm-service.js
Restart=always
RestartSec=10
StandardOutput=append:/var/log/medical-ai-llm.log
StandardError=append:/var/log/medical-ai-llm-error.log

# Environment variables
Environment=NODE_ENV=production
Environment=PORT=3001

[Install]
WantedBy=multi-user.target
```

#### Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable medical-ai-llm
sudo systemctl start medical-ai-llm

# Check status
sudo systemctl status medical-ai-llm

# View logs
sudo journalctl -u medical-ai-llm -f
```

---

### Step 7: Setup nginx Reverse Proxy (Optional but Recommended)

This allows HTTPS and cleaner URLs.

#### Install nginx:

```bash
sudo apt install -y nginx
```

#### Create nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/medical-ai
```

Paste this:

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;  # Replace with your domain or IP

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # LLM API endpoint
    location /api/ {
        proxy_pass http://localhost:3001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type' always;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:3001/api/health;
    }
}
```

#### Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/medical-ai /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

---

### Step 8: Configure Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

### Step 9: Test Remote Access

From your **local machine** (macOS):

```bash
# Replace with your droplet IP
export DROPLET_IP="159.203.123.45"

# Test health endpoint
curl http://${DROPLET_IP}/health

# Test symptom extraction
curl -X POST http://${DROPLET_IP}/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "I have fever and cough"}'
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

---

### Step 10: Update Local React Frontend

On your **local macOS machine**, update the frontend to use the remote LLM service.

#### Create environment configuration:

```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN/graph-ui
```

Create `.env.local`:

```bash
cat > .env.local << 'EOF'
# LLM Service Configuration
VITE_LLM_SERVICE_URL=http://YOUR_DROPLET_IP/api
# Example: VITE_LLM_SERVICE_URL=http://159.203.123.45/api
EOF
```

Replace `YOUR_DROPLET_IP` with your actual droplet IP address.

#### Update `MedicalDiagnosisAI.jsx`:

Add this configuration at the top of the file:

```javascript
// LLM Service configuration
const LLM_SERVICE_URL = import.meta.env.VITE_LLM_SERVICE_URL || 'http://localhost:3001/api';
```

Then in the `extractSymptomsFromText` function, use:

```javascript
const response = await fetch(`${LLM_SERVICE_URL}/extract-symptoms`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: inputText })
});
```

---

## 🔒 Security Enhancements (Production)

### 1. Setup HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (requires domain name)
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### 2. Restrict CORS to Your Domain

Edit `/home/deployer/medical-ai-backend/llm-service.js`:

```javascript
app.use(cors({
  origin: ['http://localhost:5173', 'https://yourdomain.com'],
  methods: ['GET', 'POST'],
  credentials: true
}));
```

### 3. Add Rate Limiting

```bash
cd ~/medical-ai-backend
npm install express-rate-limit
```

Update `llm-service.js`:

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later'
});

app.use('/api/extract-symptoms', limiter);
```

### 4. API Authentication (Optional)

Add API key authentication:

```javascript
const API_KEY = process.env.API_KEY || 'your-secret-key';

app.use('/api/', (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  if (apiKey !== API_KEY) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
});
```

---

## 📊 Monitoring & Maintenance

### View Logs

```bash
# Ollama logs
sudo journalctl -u ollama -f

# LLM service logs
sudo journalctl -u medical-ai-llm -f

# nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### System Resource Monitoring

```bash
# Install htop
sudo apt install htop

# Monitor resources
htop

# Check Ollama memory usage
ps aux | grep ollama

# Check disk space
df -h
```

### Performance Tuning

#### Optimize Ollama for your hardware:

Edit Ollama systemd service:

```bash
sudo nano /etc/systemd/system/ollama.service
```

Add environment variables:

```ini
[Service]
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_FLASH_ATTENTION=1"
```

Restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

## 🧪 End-to-End Testing

### 1. Test from Droplet (SSH)

```bash
# Health check
curl http://localhost:3001/api/health

# Symptom extraction
curl -X POST http://localhost:3001/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "fever cough headache"}'
```

### 2. Test from Local Machine

```bash
# Replace with your IP
export IP="159.203.123.45"

curl http://${IP}/health
curl -X POST http://${IP}/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel sick with fever"}'
```

### 3. Test from React Frontend

1. Start your local frontend: `npm run dev`
2. Go to http://localhost:5173
3. Click "🏥 Medical AI Reasoner"
4. Click "💬 Describe in Natural Language"
5. Type: "I have fever, cough, and fatigue"
6. Click "Extract Symptoms with AI"
7. Should extract: Fever, Cough, Fatigue
8. Click "Analyze & Diagnose"

---

## 💰 Cost Breakdown

### DigitalOcean Pricing (as of 2026)

| Plan | RAM | CPU | Storage | Price/mo | Suitable For |
|------|-----|-----|---------|----------|--------------|
| Basic | 4GB | 2 vCPU | 80GB | $24 | Development/Testing |
| Basic | 8GB | 4 vCPU | 160GB | $48 | Production (Recommended) |
| General Purpose | 16GB | 4 vCPU | 100GB | $84 | High Traffic |

**vs Cloud LLM APIs:**
- OpenAI GPT-4: ~$0.03 per 1K tokens = ~$180/mo for 150K requests
- Anthropic Claude: ~$0.015 per 1K tokens = ~$90/mo for 150K requests
- **Self-hosted Ollama**: $24-48/mo fixed cost, unlimited requests

**Break-even point**: ~100 API calls per day

---

## 🔧 Troubleshooting

### Ollama Not Responding

```bash
# Check if running
sudo systemctl status ollama

# Restart
sudo systemctl restart ollama

# Check logs
sudo journalctl -u ollama --no-pager | tail -50
```

### LLM Service Not Starting

```bash
# Check status
sudo systemctl status medical-ai-llm

# Check logs
sudo journalctl -u medical-ai-llm --no-pager | tail -50

# Test manually
cd ~/medical-ai-backend
node llm-service.js
```

### Port Already in Use

```bash
# Find what's using port 3001
sudo lsof -i :3001

# Kill process
sudo kill -9 <PID>
```

### CORS Errors from Frontend

Check nginx logs:

```bash
sudo tail -f /var/log/nginx/error.log
```

Verify CORS headers:

```bash
curl -I http://YOUR_IP/api/health
```

Should see:
```
Access-Control-Allow-Origin: *
```

### Slow Response Times

```bash
# Check CPU usage
htop

# Check if model is loaded
ollama list

# Try smaller model
ollama pull llama3.2:1b
```

Update `llm-service.js` to use `llama3.2:1b` instead.

---

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/linux.md)
- [DigitalOcean Ubuntu Guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04)
- [nginx Configuration](https://nginx.org/en/docs/beginners_guide.html)
- [systemd Service Guide](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

---

## 🚀 Quick Reference Commands

```bash
# SSH to droplet
ssh root@YOUR_DROPLET_IP

# Check all services
sudo systemctl status ollama medical-ai-llm nginx

# Restart everything
sudo systemctl restart ollama medical-ai-llm nginx

# View logs (all services)
sudo journalctl -u ollama -u medical-ai-llm -f

# Update system
sudo apt update && sudo apt upgrade -y

# Check disk space
df -h

# Monitor resources
htop
```

---

**Deployment Complete!** 🎉

Your Medical AI Reasoner now has NLP capabilities running on Ubuntu Linux with zero licensing costs.

**Next Steps:**
1. Deploy to production droplet
2. Configure domain name (optional)
3. Setup HTTPS with Let's Encrypt
4. Enable monitoring
5. Test end-to-end functionality

---

**Last Updated**: February 20, 2026  
**Version**: 1.0  
**Status**: Production Ready  
**Platform**: Ubuntu 22.04 LTS on DigitalOcean
