# Web UI Access Guide

## ✅ Server is Running!

The Graph Database Web UI is now accessible at:

### **Local Access (Same Computer)**
```
http://127.0.0.1:5001
```
lsof -ti:5001 | xargs kill -9

### **Network Access (Other Devices)**
```
http://192.168.1.67:5001
```

## 🔧 Port Changed to 5001

**Why?** macOS uses port 5000 for AirPlay Receiver by default, which prevented our server from starting.

**Solution:** Changed server to run on port 5001 instead.

## 🌐 How to Access

### From Your Mac
Open any of these URLs in your browser:
- `http://127.0.0.1:5001`
- `http://localhost:5001`
- `http://192.168.1.67:5001`

### From Another Device on Your Network
Use your Mac's IP address:
```
http://192.168.1.67:5001
```

To find your IP address:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## ⚠️ Important Notes

### Firewall
If you can't access from another device:
1. Open **System Preferences** → **Security & Privacy** → **Firewall**
2. Ensure Python or the application is allowed

### AirPlay Alternative
If you want to use port 5000, disable AirPlay Receiver:
1. **System Preferences** → **General** → **AirDrop & Handoff**
2. Turn off **AirPlay Receiver**
3. Change port back to 5000 in `graph_web_ui.py`

## 🔍 Troubleshooting

### "Connection Refused" or "Can't Connect"

**Check if server is running:**
```bash
curl http://127.0.0.1:5001
```

Should return HTML content. If not, restart server:
```bash
python3 graph_web_ui.py
```

### "Access Denied" Error

**Option 1: Use 127.0.0.1**
```
http://127.0.0.1:5001
```

**Option 2: Check browser settings**
- Clear browser cache
- Try incognito/private mode
- Try a different browser

**Option 3: Check macOS security**
- System Preferences → Security & Privacy
- Allow incoming connections for Python

### Port Already in Use

Kill the process and restart:
```bash
lsof -ti:5001 | xargs kill -9
python3 graph_web_ui.py
```

## 📊 Verify Server Status

### Check if server is running
```bash
lsof -i:5001
```

Should show Python process listening on port 5001.

### View server logs
```bash
tail -f graph_web_ui.log
```

### Test API endpoint
```bash
curl http://127.0.0.1:5001/api/graph/stats
```

Should return JSON with graph statistics.

## 🎯 Quick Start

1. **Start the server:**
   ```bash
   python3 graph_web_ui.py
   ```

2. **Open in browser:**
   ```
   http://127.0.0.1:5001
   ```

3. **You should see:**
   - Graph visualization with nodes (Alice, Bob, Charlie, etc.)
   - Query interface on the left
   - Interactive graph display

## 🔗 Useful URLs

| Purpose | URL |
|---------|-----|
| Main UI | http://127.0.0.1:5001/ |
| Graph Stats | http://127.0.0.1:5001/api/graph/stats |
| All Nodes | http://127.0.0.1:5001/api/graph/nodes |
| Visualization Data | http://127.0.0.1:5001/api/graph/visualization |
| Export JSON | http://127.0.0.1:5001/api/graph/export/json |

## 📝 Logs Location

Server logs are written to:
```
graph_web_ui.log
```

View errors:
```bash
grep ERROR graph_web_ui.log
```

Monitor in real-time:
```bash
tail -f graph_web_ui.log
```

---

**Server Status**: ✅ Running on port 5001  
**Access**: http://127.0.0.1:5001  
**Logs**: graph_web_ui.log  
