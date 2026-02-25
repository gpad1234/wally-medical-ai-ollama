#!/bin/bash
# Medical AI Ollama - Ubuntu Deployment Script
# Version: 1.0
# Date: February 20, 2026

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════"
echo "🚀 Medical AI Ollama Deployment"
echo "═══════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ Do not run this script as root${NC}"
   echo "Run as: ./deploy.sh"
   exit 1
fi

echo "📋 Step 1: System Update"
sudo apt update && sudo apt upgrade -y

echo ""
echo "📦 Step 2: Install Ollama"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama already installed${NC}"
    ollama --version
else
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
fi

echo ""
echo "🔥 Step 3: Pull LLM Model (llama3.2:3b)"
if ollama list | grep -q "llama3.2:3b"; then
    echo -e "${GREEN}✓ Model already downloaded${NC}"
else
    echo "Downloading model (this will take 2-5 minutes)..."
    ollama pull llama3.2:3b
    echo -e "${GREEN}✓ Model downloaded${NC}"
fi

echo ""
echo "📦 Step 4: Install Node.js"
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓ Node.js already installed${NC}"
    node --version
else
    echo "Installing Node.js 20.x LTS..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    echo -e "${GREEN}✓ Node.js installed${NC}"
fi

echo ""
echo "📁 Step 5: Setup Application Directory"
APP_DIR="$HOME/medical-ai-backend"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Copy files
cp /tmp/medical-ai-deploy/* . 2>/dev/null || echo "Files already in place"

echo ""
echo "📦 Step 6: Install Dependencies"
npm install

echo ""
echo "🔧 Step 7: Create systemd Service"
sudo tee /etc/systemd/system/medical-ai-llm.service > /dev/null <<EOF
[Unit]
Description=Medical AI LLM Service
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/node llm-service.js
Restart=always
RestartSec=10
StandardOutput=append:/var/log/medical-ai-llm.log
StandardError=append:/var/log/medical-ai-llm-error.log

Environment=NODE_ENV=production
Environment=PORT=3001
Environment=OLLAMA_URL=http://localhost:11434

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "🔧 Step 8: Create Log Files"
sudo touch /var/log/medical-ai-llm.log
sudo touch /var/log/medical-ai-llm-error.log
sudo chown $USER:$USER /var/log/medical-ai-llm*.log

echo ""
echo "🚀 Step 9: Enable and Start Services"
sudo systemctl daemon-reload
sudo systemctl enable ollama medical-ai-llm
sudo systemctl restart ollama
sleep 3
sudo systemctl restart medical-ai-llm

echo ""
echo "🌐 Step 10: Install and Configure nginx"
if command -v nginx &> /dev/null; then
    echo -e "${GREEN}✓ nginx already installed${NC}"
else
    sudo apt install -y nginx
fi

sudo tee /etc/nginx/sites-available/medical-ai > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

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
        
        # Handle preflight
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    # Health check
    location /health {
        proxy_pass http://localhost:3001/api/health;
        add_header 'Access-Control-Allow-Origin' '*' always;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/medical-ai /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo ""
echo "🔥 Step 11: Configure Firewall"
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable || true

echo ""
echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📊 Service Status:"
sudo systemctl status ollama --no-pager | grep "Active:" || true
sudo systemctl status medical-ai-llm --no-pager | grep "Active:" || true
sudo systemctl status nginx --no-pager | grep "Active:" || true

echo ""
echo "🧪 Testing Endpoints:"
echo ""

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "Unable to detect")

sleep 2

# Test health endpoint
if curl -s http://localhost:3001/api/health > /dev/null; then
    echo -e "${GREEN}✓ LLM Service: Running${NC}"
else
    echo -e "${RED}✗ LLM Service: Not responding${NC}"
fi

# Test nginx
if curl -s http://localhost/health > /dev/null; then
    echo -e "${GREEN}✓ nginx Proxy: Running${NC}"
else
    echo -e "${RED}✗ nginx Proxy: Not responding${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "📡 Access URLs:"
echo "═══════════════════════════════════════════════════════"
echo "Health Check: http://$PUBLIC_IP/health"
echo "API Endpoint: http://$PUBLIC_IP/api/extract-symptoms"
echo ""
echo "💡 Test from your local machine:"
echo ""
echo "curl http://$PUBLIC_IP/health"
echo ""
echo 'curl -X POST http://'"$PUBLIC_IP"'/api/extract-symptoms \\'
echo "  -H 'Content-Type: application/json' \\"
echo '  -d '"'"'{"text": "I have fever and cough"}'"'"
echo ""
echo "═══════════════════════════════════════════════════════"
echo "📋 Useful Commands:"
echo "═══════════════════════════════════════════════════════"
echo "View logs:     sudo journalctl -u medical-ai-llm -f"
echo "Restart:       sudo systemctl restart medical-ai-llm"
echo "Status:        sudo systemctl status medical-ai-llm"
echo "Test Ollama:   ollama run llama3.2:3b"
echo ""
echo "🎉 Your Medical AI LLM service is now running!"
echo "═══════════════════════════════════════════════════════"
