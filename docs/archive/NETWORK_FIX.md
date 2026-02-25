# Network Error Fix - CORS & API Configuration

## Problem
React frontend on port 5173 was unable to communicate with Flask backend on port 5000, resulting in "network error response" messages.

## Root Cause
**Missing CORS (Cross-Origin Resource Sharing) Headers**

When a browser makes a request from one origin (http://localhost:5173) to a different origin (http://127.0.0.1:5000), browsers block it by default for security reasons. Flask wasn't configured to allow cross-origin requests.

## Solution Implemented

### 1. Flask Backend Changes (`graph_web_ui.py`)

**Added CORS Support:**
```python
from flask_cors import CORS

# Enable CORS for React frontend on port 5173
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

**Install Flask-CORS:**
```bash
pip install flask-cors
```

### 2. React API Service Improvements (`graph-ui/src/services/api.js`)

**Added Request/Response Logging:**
```javascript
// Request interceptor for logging
api.interceptors.request.use((config) => {
  console.log('🔵 API Request:', config.method.toUpperCase(), config.url);
  return config;
});

// Response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.message);
    if (error.code === 'ECONNREFUSED') {
      console.error('⚠️  Cannot connect to API. Is Flask running on port 5000?');
    }
    return Promise.reject(error);
  }
);
```

## How to Debug API Issues

### In Browser Console (F12 or Cmd+Option+I)

You'll now see detailed logs:
```
🔵 API Request: GET /api/graph/stats
✅ API Response: 200 /api/graph/stats
🔵 API Request: GET /api/graph/visualization
✅ API Response: 200 /api/graph/visualization
```

### If Connection Fails:
```
❌ API Response Error: Network Error
⚠️  Cannot connect to API. Is Flask running on port 5000?
```

## Verify Everything is Running

### Check Flask
```bash
curl http://127.0.0.1:5000/api/graph/stats
# Should return JSON with graph statistics
```

### Check React
```bash
# Browser should load http://localhost:5173
# Console (F12) should show green checkmarks (✅)
```

### Check Servers
```bash
# Terminal 1: React running?
lsof -i :5173

# Terminal 2: Flask running?
lsof -i :5000
```

## Complete Setup

| Component | Port | URL | Status |
|-----------|------|-----|--------|
| Flask API | 5000 | http://127.0.0.1:5000 | ✅ Running with CORS |
| React UI | 5173 | http://localhost:5173 | ✅ With API logging |
| GraphDB | Memory | - | ✅ 6 nodes, 8 edges |

## Key Files Modified

1. **graph_web_ui.py** (Flask backend)
   - Added `from flask_cors import CORS`
   - Added CORS configuration for port 5173
   - Changed debug mode to False

2. **graph-ui/src/services/api.js** (React API client)
   - Added request interceptor logging
   - Added response interceptor logging
   - Added helpful error messages

## Testing the Fix

1. Open http://localhost:5173 in browser
2. Open DevTools (F12 or Cmd+Option+I)
3. Go to Console tab
4. Watch for API calls:
   - Blue (🔵) = Request sent
   - Green (✅) = Response received
   - Red (❌) = Error

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot connect to API" | Flask not running: `python3 graph_web_ui.py` |
| Still getting CORS errors | Restart Flask after CORS changes |
| React page won't load | React dev server not running: `cd graph-ui && npm run dev` |
| Port already in use | Kill process: `lsof -i :PORT` then `kill -9 PID` |

## Prevention

✅ CORS now properly configured
✅ Detailed logging for debugging
✅ Both servers communicate successfully
✅ Natural language queries work end-to-end

---

**Status**: ✅ Fixed - Network communication restored
**Last Updated**: November 18, 2025
