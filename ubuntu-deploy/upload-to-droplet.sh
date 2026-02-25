#!/bin/bash
# Quick Upload Script - Upload deployment package to Ubuntu droplet
# Usage: ./upload-to-droplet.sh YOUR_DROPLET_IP

if [ -z "$1" ]; then
    echo "Usage: ./upload-to-droplet.sh DROPLET_IP"
    echo "Example: ./upload-to-droplet.sh 159.203.123.45"
    exit 1
fi

DROPLET_IP=$1

echo "🚀 Uploading Medical AI deployment package to $DROPLET_IP..."
echo ""

# Create directory on droplet
echo "📁 Creating deployment directory on droplet..."
ssh root@$DROPLET_IP "mkdir -p /tmp/medical-ai-deploy" || {
    echo "❌ Failed to connect to droplet. Check IP address and SSH access."
    exit 1
}

# Upload files
echo "📤 Uploading files..."
scp -r deploy.sh llm-service.js package.json README.md root@$DROPLET_IP:/tmp/medical-ai-deploy/ || {
    echo "❌ Failed to upload files."
    exit 1
}

echo ""
echo "✅ Upload complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. SSH into your droplet:"
echo "   ssh root@$DROPLET_IP"
echo ""
echo "2. Run the deployment script:"
echo "   cp -r /tmp/medical-ai-deploy ~/"
echo "   cd ~/medical-ai-deploy"
echo "   chmod +x deploy.sh"
echo "   ./deploy.sh"
echo ""
echo "3. Wait ~8 minutes for installation to complete"
echo ""
echo "4. Test from your local machine:"
echo "   curl http://$DROPLET_IP/health"
echo ""
