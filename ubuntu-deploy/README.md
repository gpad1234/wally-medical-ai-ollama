# Ubuntu Deployment Package

This package contains everything needed to deploy the Medical AI LLM service on Ubuntu Linux.

## 📦 Package Contents

- `deploy.sh` - Automated deployment script
- `llm-service.js` - Node.js LLM service
- `package.json` - Node.js dependencies
- `README.md` - This file

## 🚀 Quick Deploy (1 Command)

### Step 1: Upload to Ubuntu Server

From your local machine:

```bash
# Replace with your droplet IP
export DROPLET_IP="159.203.123.45"

# Upload deployment package
scp -r ubuntu-deploy/* root@$DROPLET_IP:/tmp/medical-ai-deploy/
```

### Step 2: SSH and Deploy

```bash
# SSH into server
ssh root@$DROPLET_IP

# Copy files to home directory
cp -r /tmp/medical-ai-deploy ~/ 
cd ~/medical-ai-deploy

# Make script executable
chmod +x deploy.sh

# Run deployment (takes 5-10 minutes)
./deploy.sh
```

That's it! The script will:
- Install Ollama and pull llama3.2:3b model
- Install Node.js 20.x
- Setup LLM service with systemd
- Configure nginx reverse proxy
- Configure firewall
- Start all services

## ✅ Verify Deployment

After deployment completes:

```bash
# Check services
sudo systemctl status ollama medical-ai-llm nginx

# Test locally on server
curl http://localhost:3001/api/health

curl -X POST http://localhost:3001/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "fever and cough"}'
```

## 🌐 Test from Your Local Machine

```bash
# Replace with your droplet IP
export DROPLET_IP="159.203.123.45"

# Test health
curl http://$DROPLET_IP/health

# Test symptom extraction
curl -X POST http://$DROPLET_IP/api/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{"text": "I have fever, cough, and headache"}'
```

Expected response:
```json
{
  "success": true,
  "extracted": ["Fever", "Cough", "Headache"],
  "symptomIds": ["symp:Fever", "symp:Cough", "symp:Headache"],
  "llmModel": "llama3.2:3b"
}
```

## 🔧 Update Local React Frontend

On your local macOS machine:

```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN/graph-ui

# Create .env.local file
cat > .env.local << EOF
VITE_LLM_SERVICE_URL=http://YOUR_DROPLET_IP/api
EOF
```

Replace `YOUR_DROPLET_IP` with your actual IP address.

Then restart your React dev server:

```bash
npm run dev
```

## 📊 Monitoring

```bash
# View real-time logs
sudo journalctl -u medical-ai-llm -f

# Check Ollama
sudo systemctl status ollama

# Check nginx
sudo systemctl status nginx

# Monitor resources
htop
```

## 🐛 Troubleshooting

### Service not starting

```bash
# Check logs
sudo journalctl -u medical-ai-llm --no-pager | tail -50

# Restart services
sudo systemctl restart ollama medical-ai-llm nginx
```

### Ollama not responding

```bash
# Check if running
sudo systemctl status ollama

# Restart Ollama
sudo systemctl restart ollama

# Wait 5 seconds then restart LLM service
sleep 5
sudo systemctl restart medical-ai-llm
```

### Port issues

```bash
# Check what's using port 3001
sudo lsof -i :3001

# Kill process if needed
sudo systemctl stop medical-ai-llm
```

## 🔒 Security (Production)

### Add HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate (requires domain name)
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

### Restrict CORS

Edit `~/medical-ai-backend/llm-service.js`:

```javascript
app.use(cors({
  origin: ['http://localhost:5173', 'https://yourdomain.com'],
  methods: ['GET', 'POST']
}));
```

Then restart:

```bash
sudo systemctl restart medical-ai-llm
```

## 📚 Additional Documentation

See `UBUNTU_OLLAMA_DEPLOYMENT.md` for detailed information.

## ✨ System Requirements

- Ubuntu 22.04 LTS (64-bit)
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Public IP address

## 💰 Cost

- DigitalOcean Basic Droplet (4GB): $24/month
- DigitalOcean Basic Droplet (8GB): $48/month
- No additional API costs!

---

**Ready to deploy?** Run `./deploy.sh` and you're done! 🚀
