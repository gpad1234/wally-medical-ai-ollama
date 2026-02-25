#!/bin/bash
set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║    WALLY-CLEAN DigitalOcean Droplet Setup Script      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (or use sudo)"
    exit 1
fi

echo "📦 Step 1/10: Updating system packages..."
apt update && apt upgrade -y

echo "🔧 Step 2/10: Installing build essentials..."
apt install -y build-essential git curl wget ufw htop

echo "🐍 Step 3/10: Installing Python 3.12..."
apt install -y python3.12 python3.12-venv python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
python3 --version

echo "📦 Step 4/10: Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
node --version
npm --version

echo "🌐 Step 5/10: Installing and configuring nginx..."
apt install -y nginx
systemctl enable nginx

echo "👤 Step 6/10: Creating application user..."
if ! id -u wally > /dev/null 2>&1; then
    adduser --system --group --home /opt/wally wally
    echo "✅ User 'wally' created"
else
    echo "ℹ️  User 'wally' already exists"
fi

echo "📂 Step 7/10: Setting up application directory..."
mkdir -p /opt/wally-clean
mkdir -p /opt/wally-clean/logs

# Clone repository if not exists
if [ ! -d "/opt/wally-clean/.git" ]; then
    echo "📥 Cloning repository..."
    cd /opt
    git clone https://github.com/gpad1234/Startup-One-Wally-Clean.git wally-clean-temp
    mv wally-clean-temp/* wally-clean/
    mv wally-clean-temp/.git wally-clean/
    rm -rf wally-clean-temp
else
    echo "ℹ️  Repository already cloned, pulling latest..."
    cd /opt/wally-clean
    git pull origin main
fi

chown -R wally:wally /opt/wally-clean

echo "🔨 Step 8/10: Building application..."
cd /opt/wally-clean

# Build as wally user
su - wally -s /bin/bash << 'EOF'
cd /opt/wally-clean

# Python setup
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend build
cd graph-ui
npm install
npm run build
cd ..

echo "✅ Application built successfully"
EOF

echo "⚙️  Step 9/10: Configuring systemd services..."
cp /opt/wally-clean/deploy/systemd/*.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable wally-ontology-api
systemctl enable wally-frontend
systemctl start wally-ontology-api
systemctl start wally-frontend

echo "🌐 Step 10/10: Configuring nginx..."
cp /opt/wally-clean/deploy/nginx/wally-clean.conf /etc/nginx/sites-available/
ln -sf /etc/nginx/sites-available/wally-clean.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw status

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║              ✅ Setup Complete!                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 WALLY-CLEAN is now running!"
echo ""
echo "📊 Service Status:"
systemctl status wally-ontology-api --no-pager -l | head -3
systemctl status wally-frontend --no-pager -l | head -3
systemctl status nginx --no-pager -l | head -3
echo ""
echo "🌐 Access your application:"
echo "   http://$(curl -s ifconfig.me)"
echo ""
echo "📋 Useful commands:"
echo "   systemctl status wally-ontology-api  # Check API status"
echo "   systemctl status wally-frontend      # Check frontend status"
echo "   journalctl -u wally-ontology-api -f  # View API logs"
echo "   tail -f /opt/wally-clean/logs/*.log  # View application logs"
echo ""
echo "🔄 To update the application:"
echo "   /opt/wally-clean/scripts/update.sh"
echo ""
