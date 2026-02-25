# DigitalOcean Deployment Guide

Complete guide for deploying WALLY-CLEAN to a DigitalOcean droplet.

---

## 🚀 Quick Deployment

### 1. Create Droplet

**Recommended specs:**
- **OS:** Ubuntu 24.04 LTS (or 22.04)
- **Plan:** Basic ($12/mo minimum)
  - 2 GB RAM / 1 CPU
  - 50 GB SSD
  - 2 TB transfer
- **Datacenter:** Choose closest to your users
- **Authentication:** SSH key (more secure than password)

### 2. Initial Droplet Setup

SSH into your new droplet:

```bash
ssh root@YOUR_DROPLET_IP
```

Run the automated setup script:

```bash
# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/gpad1234/Startup-One-Wally-Clean/main/scripts/setup_droplet.sh | bash

# OR if you already have the code:
cd /opt/wally-clean
chmod +x scripts/setup_droplet.sh
./scripts/setup_droplet.sh
```

**What the setup script does:**
- ✅ Updates system packages
- ✅ Installs dependencies (Python 3.12, Node.js 20, nginx)
- ✅ Creates app user and directories
- ✅ Clones repository
- ✅ Builds application
- ✅ Configures systemd services
- ✅ Sets up nginx reverse proxy
- ✅ Configures firewall

**Time:** ~5-10 minutes

### 3. Manual Deployment (Alternative)

If you prefer manual control, follow the detailed steps below.

---

## 📋 Manual Setup Steps

### Step 1: Update System

```bash
apt update && apt upgrade -y
apt install -y build-essential git curl
```

### Step 2: Install Python 3.12

```bash
apt install -y python3.12 python3.12-venv python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
python3 --version  # Should show 3.12.x
```

### Step 3: Install Node.js 20

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
node --version  # Should show v20.x
npm --version
```

### Step 4: Install nginx

```bash
apt install -y nginx
systemctl enable nginx
```

### Step 5: Create App User

```bash
adduser --system --group --home /opt/wally wally
mkdir -p /opt/wally-clean
chown wally:wally /opt/wally-clean
```

### Step 6: Clone Repository

```bash
cd /opt
git clone https://github.com/gpad1234/Startup-One-Wally-Clean.git wally-clean
cd wally-clean
chown -R wally:wally /opt/wally-clean
```

### Step 7: Build Application

```bash
su - wally -s /bin/bash
cd /opt/wally-clean

# Build
./build_local.sh

# If build script doesn't exist, manual build:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd graph-ui
npm install
npm run build
```

### Step 8: Configure Services

Copy systemd service files:

```bash
cp /opt/wally-clean/deploy/systemd/*.service /etc/systemd/system/
systemctl daemon-reload
```

Enable and start services:

```bash
systemctl enable wally-ontology-api
systemctl enable wally-frontend
systemctl start wally-ontology-api
systemctl start wally-frontend
```

### Step 9: Configure nginx

```bash
cp /opt/wally-clean/deploy/nginx/wally-clean.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/wally-clean.conf /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default  # Remove default site
nginx -t  # Test configuration
systemctl restart nginx
```

### Step 10: Configure Firewall

```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
ufw status
```

---

## 🔧 Service Management

### Check Service Status

```bash
systemctl status wally-ontology-api
systemctl status wally-frontend
systemctl status nginx
```

### View Logs

```bash
# Application logs
journalctl -u wally-ontology-api -f
journalctl -u wally-frontend -f

# nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Application file logs
tail -f /opt/wally-clean/logs/ontology_api.log
```

### Restart Services

```bash
systemctl restart wally-ontology-api
systemctl restart wally-frontend
systemctl restart nginx
```

### Stop Services

```bash
systemctl stop wally-ontology-api
systemctl stop wally-frontend
```

---

## 🌐 Domain Setup (Optional)

### 1. Point Domain to Droplet

In your domain registrar (GoDaddy, Namecheap, etc.):

- Create **A record**: `yourdomain.com` → `YOUR_DROPLET_IP`
- Create **A record**: `www.yourdomain.com` → `YOUR_DROPLET_IP`

DNS propagation: 5 minutes to 48 hours

### 2. Update nginx Configuration

Edit `/etc/nginx/sites-available/wally-clean.conf`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    # ... rest of config
}
```

Reload nginx:
```bash
nginx -t && systemctl reload nginx
```

### 3. Enable HTTPS with Let's Encrypt

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically:
- Obtain SSL certificate
- Configure nginx for HTTPS
- Set up auto-renewal

Test auto-renewal:
```bash
certbot renew --dry-run
```

---

## 🔄 Updating Application

### Pull Latest Code

```bash
cd /opt/wally-clean
git pull origin main
```

### Rebuild and Restart

```bash
# As wally user
su - wally -s /bin/bash
cd /opt/wally-clean

# Rebuild
source .venv/bin/activate
pip install -r requirements.txt
cd graph-ui && npm install && npm run build && cd ..

# Restart services
exit  # Back to root
systemctl restart wally-ontology-api
systemctl restart wally-frontend
```

### Quick Update Script

Create `/opt/wally-clean/update.sh`:

```bash
#!/bin/bash
set -e
cd /opt/wally-clean
git pull origin main
su - wally -s /bin/bash -c "cd /opt/wally-clean && source .venv/bin/activate && pip install -r requirements.txt"
su - wally -s /bin/bash -c "cd /opt/wally-clean/graph-ui && npm install && npm run build"
systemctl restart wally-ontology-api
systemctl restart wally-frontend
echo "✅ Update complete!"
```

Make executable:
```bash
chmod +x /opt/wally-clean/update.sh
```

Run updates:
```bash
/opt/wally-clean/update.sh
```

---

## 🔍 Health Checks

### API Health

```bash
curl http://localhost:5002/api/ontology/graph/nodes?skip=0&limit=5
```

Expected: JSON response with node data

### Frontend Health

```bash
curl -I http://YOUR_DROPLET_IP
```

Expected: `200 OK` with HTML

### Service URLs

- **Frontend:** http://YOUR_DROPLET_IP
- **API (internal):** http://localhost:5002
- **nginx:** Proxies external → internal services

---

## 📊 Monitoring

### Resource Usage

```bash
# CPU/Memory
htop

# Disk space
df -h

# Service memory
systemctl status wally-ontology-api | grep Memory
```

### Log Rotation

nginx logs auto-rotate. For app logs, create `/etc/logrotate.d/wally-clean`:

```
/opt/wally-clean/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifexist
    create 0640 wally wally
    sharedscripts
    postrotate
        systemctl reload wally-ontology-api > /dev/null 2>&1 || true
    endscript
}
```

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
journalctl -u wally-ontology-api -n 50 --no-pager
# Check for Python errors, missing dependencies
```

### nginx 502 Bad Gateway

Backend service not running:
```bash
systemctl status wally-ontology-api
systemctl start wally-ontology-api
```

### Port Already in Use

```bash
lsof -i :5002
# Kill process or change port in systemd service file
```

### Permission Errors

```bash
chown -R wally:wally /opt/wally-clean
chmod +x /opt/wally-clean/*.sh
```

---

## 🔐 Security Hardening

### 1. Disable Root Login

Edit `/etc/ssh/sshd_config`:
```
PermitRootLogin no
```

Restart SSH:
```bash
systemctl restart sshd
```

### 2. Create Admin User

```bash
adduser admin
usermod -aG sudo admin
# Copy SSH keys to admin user
```

### 3. Configure fail2ban

```bash
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

### 4. Enable Automatic Updates

```bash
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

---

## 📦 Backup Strategy

### Application Data

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backups/wally-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR
cp -r /opt/wally-clean/logs $BACKUP_DIR/
cp -r /opt/wally-clean/sample_data $BACKUP_DIR/
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
# Upload to DigitalOcean Spaces or S3
```

### DigitalOcean Snapshots

Enable weekly automated snapshots in DigitalOcean control panel:
- Droplet → Settings → Backups
- Cost: 20% of droplet price

---

## 📈 Scaling

### Upgrade Droplet Size

DigitalOcean control panel → Resize → Choose larger plan

**Recommended for production:**
- 4 GB RAM / 2 CPU ($24/mo)
- 8 GB RAM / 4 CPU ($48/mo)

### Add CDN (Optional)

For static assets:
- Enable DigitalOcean Spaces + CDN
- Serve `graph-ui/dist/` from CDN

---

## ✅ Post-Deployment Checklist

- [ ] Services running (ontology-api, frontend, nginx)
- [ ] Firewall configured (UFW)
- [ ] Domain DNS pointed (if using custom domain)
- [ ] SSL certificate installed (if using domain)
- [ ] Health checks passing
- [ ] Logs readable and rotating
- [ ] Backups configured
- [ ] Monitoring set up
- [ ] Security hardening applied

---

## 📞 Support

- **Repository:** https://github.com/gpad1234/Startup-One-Wally-Clean
- **Issues:** Create GitHub issue
- **DigitalOcean Docs:** https://docs.digitalocean.com

---

**Status:** ✅ Ready for DigitalOcean Deployment  
**Last Updated:** February 18, 2026
