---
layout: default
title: Deployment
---

# 🚀 Deployment Guide

Complete guide for deploying WALLY to production. Covers DigitalOcean deployment, automated scripts, and multi-platform options.

---

## Quick Deploy to DigitalOcean

### Prerequisites

- DigitalOcean account
- SSH key configured
- Domain name (optional)

### Deploy via Git Pull

On the server, after initial setup (see Manual Deployment below):

```bash
cd /opt/wally-clean
git pull
source .venv/bin/activate && pip install -r requirements.txt
cd graph-ui && npm run build && cd ..
sudo systemctl restart wally-frontend wally-ontology-api medical-ai-llm
```

All four systemd services restart automatically on server reboot.

---

## Manual DigitalOcean Deployment

### Step 1: Create Droplet

1. Visit [DigitalOcean](https://www.digitalocean.com/)
2. Create new droplet:
   - **Image:** Ubuntu 24.04 LTS
   - **Plan:** Basic ($12–18/month — **minimum 2GB RAM** required for Ollama/Llama 3.2; 4GB recommended)
   - **Datacenter:** Choose closest to your users
   - **Authentication:** SSH key (recommended)
   - **Hostname:** wally-production

   > ⚠️ **RAM note**: Ollama with `llama3.2:1b` needs ~1.3GB RAM + swap. A 1GB droplet will OOM. The live server at 161.35.239.151 uses a 2GB droplet with 2GB swap configured.

3. Note your droplet's IP address (e.g., `161.35.239.151`)

### Step 2: Initial Server Setup

```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-pip python3-venv nodejs npm nginx gcc make git

# Create application user
useradd -m -s /bin/bash wally
usermod -aG sudo wally
```

### Step 3: Clone and Build

```bash
# Switch to wally user
su - wally

# Clone repository
cd /opt
git clone https://github.com/gpad1234/Startup-One-Wally-Clean.git wally-clean
cd wally-clean

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build C libraries
cd src/core
make
cd ../..

# Build frontend
cd graph-ui
npm install
npm run build
cd ..
```

### Step 4: Configure systemd Services

Create API service:

```bash
sudo nano /etc/systemd/system/wally-ontology-api.service
```

```ini
[Unit]
Description=WALLY Ontology API Service
After=network.target

[Service]
Type=simple
User=wally
WorkingDirectory=/opt/wally-clean
Environment="PATH=/opt/wally-clean/.venv/bin"
ExecStart=/opt/wally-clean/.venv/bin/python3 /opt/wally-clean/ontology_api.py
Restart=on-failure
RestartSec=10s
StandardOutput=append:/opt/wally-clean/logs/ontology_api.log
StandardError=append:/opt/wally-clean/logs/ontology_api_error.log

[Install]
WantedBy=multi-user.target
```

Create frontend service:

```bash
sudo nano /etc/systemd/system/wally-frontend.service
```

```ini
[Unit]
Description=WALLY Frontend Preview Server
After=network.target

[Service]
Type=simple
User=wally
WorkingDirectory=/opt/wally-clean/graph-ui
ExecStart=/usr/bin/npm run preview -- --host 0.0.0.0 --port 5173
Restart=on-failure
RestartSec=10s
StandardOutput=append:/opt/wally-clean/logs/frontend.log
StandardError=append:/opt/wally-clean/logs/frontend_error.log

[Install]
WantedBy=multi-user.target
```

Enable and start services:

```bash
sudo systemctl daemon-reload
sudo systemctl enable wally-ontology-api
sudo systemctl enable wally-frontend
sudo systemctl start wally-ontology-api
sudo systemctl start wally-frontend
```

### Step 5: Configure nginx

```bash
sudo nano /etc/nginx/sites-available/wally-clean.conf
```

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:5002/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/wally-clean.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Verify Deployment

```bash
# Check services
sudo systemctl status wally-ontology-api
sudo systemctl status wally-frontend
sudo systemctl status nginx

# Test API
curl http://localhost:5002/api/ontology/graph/nodes?skip=0&limit=3

# Test from external
curl http://YOUR_DROPLET_IP/api/ontology/graph/nodes?skip=0&limit=3

# Visit in browser
# http://YOUR_DROPLET_IP
```

---

## Automated Deployment Scripts

WALLY includes three powerful deployment scripts:

### deploy_to_droplet.sh

**Purpose:** One-command deployment from local machine to droplet

```bash
#!/bin/bash
# Usage: ./scripts/deploy_to_droplet.sh

DROPLET_IP="YOUR_IP"
SSH_KEY="~/.ssh/your_key"

echo "🚀 Deploying to $DROPLET_IP..."

# Upload code
rsync -avz --exclude 'node_modules' --exclude '.venv' \
  -e "ssh -i $SSH_KEY" \
  ./ root@$DROPLET_IP:/opt/wally-clean/

# SSH and build
ssh -i $SSH_KEY root@$DROPLET_IP << 'EOF'
cd /opt/wally-clean
source .venv/bin/activate
pip install -r requirements.txt
cd src/core && make && cd ../..
cd graph-ui && npm install && npm run build && cd ..
sudo systemctl restart wally-ontology-api
sudo systemctl restart wally-frontend
EOF

echo "✅ Deployment complete!"
```

### setup_droplet.sh

**Purpose:** Initial droplet setup (run once)

```bash
# Usage: ssh into droplet first, then:
cd /opt/wally-clean
./scripts/setup_droplet.sh
```

Sets up:
- System dependencies
- Application user
- Directory structure
- systemd services
- nginx configuration

### update.sh

**Purpose:** Quick application updates on droplet

```bash
# On droplet:
cd /opt/wally-clean
./scripts/update.sh
```

Updates:
- Git pull latest code
- Install new dependencies
- Rebuild C libraries
- Rebuild frontend
- Restart services

---

## SSL/HTTPS Setup

### Option 1: Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### Option 2: Cloudflare (Recommended)

1. Add domain to Cloudflare
2. Enable "Full" SSL mode
3. Use Cloudflare's SSL certificate
4. Point DNS A record to droplet IP
5. Cloudflare handles HTTPS automatically

---

## Environment Variables

### Backend Configuration

Create `.env` file:

```bash
# /opt/wally-clean/.env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5002
CORS_ORIGINS=http://your-domain.com,https://your-domain.com
LOG_LEVEL=INFO
```

Load in ontology_api.py:

```python
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv('PORT', 5002))
DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
```

### Frontend Configuration

Edit `graph-ui/.env.production`:

```bash
VITE_API_BASE_URL=/api
VITE_APP_TITLE=WALLY Ontology Editor
```

---

## Monitoring & Maintenance

### View Logs

```bash
# API logs
sudo journalctl -u wally-ontology-api -f

# Frontend logs
sudo journalctl -u wally-frontend -f

# nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application logs
tail -f /opt/wally-clean/logs/ontology_api.log
tail -f /opt/wally-clean/logs/ontology_api_error.log
```

### Restart Services

```bash
# Restart API
sudo systemctl restart wally-ontology-api

# Restart frontend
sudo systemctl restart wally-frontend

# Restart nginx
sudo systemctl restart nginx

# Restart all
sudo systemctl restart wally-ontology-api wally-frontend nginx
```

### Check Service Status

```bash
# All services
sudo systemctl status wally-ontology-api
sudo systemctl status wally-frontend
sudo systemctl status nginx

# Resource usage
top
htop  # More user-friendly
```

### Database Backup

```bash
# Backup RDF data (if using persistent storage)
cp /opt/wally-clean/data/ontology.owl /backup/ontology-$(date +%Y%m%d).owl

# Automate with cron
crontab -e
# Add: 0 2 * * * cp /opt/wally-clean/data/ontology.owl /backup/ontology-$(date +\%Y\%m\%d).owl
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u wally-ontology-api -n 50

# Check permissions
ls -la /opt/wally-clean
sudo chown -R wally:wally /opt/wally-clean

# Check ports
sudo lsof -i :5002
sudo lsof -i :5173
```

### C Library Errors

```bash
# Rebuild libraries
cd /opt/wally-clean/src/core
make clean
make

# Check if library exists
ls -lh libsimpledb.so

# Test loading
python3 -c "import ctypes; ctypes.cdll.LoadLibrary('./libsimpledb.so')"
```

### nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check if running
sudo systemctl status nginx

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Frontend Not Loading

```bash
# Check if built
ls -lh /opt/wally-clean/graph-ui/dist/

# Rebuild
cd /opt/wally-clean/graph-ui
npm run build

# Check service
sudo systemctl status wally-frontend
```

---

## Alternative Deployment Platforms

### AWS EC2

Similar to DigitalOcean:
1. Launch EC2 instance (Ubuntu 24.04)
2. Configure security groups (ports 80, 443, 22)
3. Follow manual deployment steps above

### Heroku

```bash
# Install Heroku CLI
# Create Procfile:
web: python3 ontology_api.py

# Deploy
heroku create wally-ontology
git push heroku main
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.12

# Backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN cd src/core && make

# Frontend
RUN apt-get update && apt-get install -y nodejs npm
WORKDIR /app/graph-ui
RUN npm install && npm run build

EXPOSE 5002
CMD ["python3", "ontology_api.py"]
```

Build and run:

```bash
docker build -t wally-ontology .
docker run -p 5002:5002 wally-ontology
```

---

## Performance Tuning

### Backend Optimization

```python
# Use gunicorn instead of Flask dev server
pip install gunicorn

# Run with workers
gunicorn -w 4 -b 0.0.0.0:5002 ontology_api:app
```

Update systemd service:

```ini
ExecStart=/opt/wally-clean/.venv/bin/gunicorn -w 4 -b 0.0.0.0:5002 ontology_api:app
```

### nginx Caching

```nginx
# Add to nginx config
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m;

location /api/ {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_key "$request_uri";
    # ... rest of config
}
```

### Resource Limits

```ini
[Service]
# In systemd service files
MemoryLimit=512M
CPUQuota=50%
```

---

## Security Best Practices

### Firewall Setup

```bash
# Enable UFW
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### Application Security

```python
# Rate limiting (install flask-limiter)
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/ontology/graph/viewport')
@limiter.limit("10 per minute")
def viewport():
    pass
```

### Regular Updates

```bash
# System updates
sudo apt update && sudo apt upgrade -y

# Python packages
pip install --upgrade -r requirements.txt

# Node packages
cd graph-ui && npm update && cd ..
```

---

## Production Checklist

Before going live:

- [ ] Domain configured and DNS updated
- [ ] SSL certificate installed (HTTPS)
- [ ] Firewall enabled and configured
- [ ] Services set to auto-start on boot
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Error tracking set up
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team trained on deployment process

---

## Detailed Documentation

For complete deployment documentation, see:

📖 **[DIGITALOCEAN_DEPLOY.md](../DIGITALOCEAN_DEPLOY.md)** (923 lines)
- Step-by-step deployment guide
- Troubleshooting section
- Configuration examples
- Performance tuning tips

---

[← Back to Home](./) | [Development →](development)
