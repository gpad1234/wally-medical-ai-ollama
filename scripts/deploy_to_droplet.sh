#!/bin/bash
# Deploy WALLY-CLEAN to DigitalOcean Droplet
# Usage: ./deploy_to_droplet.sh [DROPLET_IP] [SSH_KEY_PATH]

set -e

# Configuration
DROPLET_IP="${1:-161.35.239.151}"
SSH_KEY="${2:-$HOME/.ssh/fisheye_rsa}"
DROPLET_USER="root"

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Deploy WALLY-CLEAN to DigitalOcean Droplet        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Target: $DROPLET_USER@$DROPLET_IP"
echo "🔑 SSH Key: $SSH_KEY"
echo ""

# Check if SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    echo "   Please create your droplet and download the SSH key"
    exit 1
fi

# Set correct permissions on SSH key
chmod 600 "$SSH_KEY"

# Test SSH connection
echo "🔌 Testing SSH connection..."
if ! ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$DROPLET_USER@$DROPLET_IP" "echo 'Connection successful'" > /dev/null 2>&1; then
    echo "❌ Cannot connect to droplet. Please check:"
    echo "   - Droplet IP: $DROPLET_IP"
    echo "   - SSH key: $SSH_KEY"
    echo "   - Droplet is running"
    exit 1
fi
echo "✅ SSH connection successful"
echo ""

# Create deployment package
echo "📦 Creating deployment package..."
TEMP_DIR=$(mktemp -d)
tar czf "$TEMP_DIR/wally-clean.tar.gz" \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='logs/*.log' \
    --exclude='graph-ui/dist' \
    -C "$(dirname "$0")/.." .

echo "📤 Uploading to droplet..."
scp -i "$SSH_KEY" "$TEMP_DIR/wally-clean.tar.gz" "$DROPLET_USER@$DROPLET_IP:/tmp/"

echo "🚀 Running setup script on droplet..."
ssh -i "$SSH_KEY" "$DROPLET_USER@$DROPLET_IP" << 'ENDSSH'
set -e

# Extract application
mkdir -p /opt/wally-clean
cd /opt/wally-clean
tar xzf /tmp/wally-clean.tar.gz
rm /tmp/wally-clean.tar.gz

# Make scripts executable
chmod +x /opt/wally-clean/scripts/*.sh

# Run setup
bash /opt/wally-clean/scripts/setup_droplet.sh

echo ""
echo "✅ Deployment complete!"

ENDSSH

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║           🎉 Deployment Successful!                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Your application is live at:"
echo "   http://$DROPLET_IP"
echo ""
echo "🔐 SSH into your droplet:"
echo "   ssh -i $SSH_KEY $DROPLET_USER@$DROPLET_IP"
echo ""
echo "📊 Check service status:"
echo "   ssh -i $SSH_KEY $DROPLET_USER@$DROPLET_IP 'systemctl status wally-ontology-api'"
echo ""
echo "📋 View logs:"
echo "   ssh -i $SSH_KEY $DROPLET_USER@$DROPLET_IP 'journalctl -u wally-ontology-api -f'"
echo ""
