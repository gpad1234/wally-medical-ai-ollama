#!/bin/bash
set -e

echo "🔄 Updating WALLY-CLEAN..."

if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (or use sudo)"
    exit 1
fi

cd /opt/wally-clean

echo "📥 Pulling latest code..."
git pull origin main

echo "🔨 Rebuilding application..."
su - wally -s /bin/bash << 'EOF'
cd /opt/wally-clean

# Update Python dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Rebuild frontend
cd graph-ui
npm install
npm run build
cd ..

echo "✅ Build complete"
EOF

echo "🔄 Restarting services..."
systemctl restart wally-ontology-api
systemctl restart wally-frontend
systemctl reload nginx

echo ""
echo "✅ Update complete!"
echo ""
echo "📊 Service Status:"
systemctl status wally-ontology-api --no-pager -l | head -3
systemctl status wally-frontend --no-pager -l | head -3
echo ""
