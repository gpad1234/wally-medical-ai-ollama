# Local Build & Deployment Guide

Complete guide for building and deploying WALLY-CLEAN locally.

---

## 🚀 Quick Start

### First Time Setup

```bash
# 1. Build everything
./build_local.sh

# 2. Deploy all services
./deploy_local.sh
```

That's it! All services will be running.

---

## 📦 What Gets Built

### 1. C Library (GraphDB Core)
- **Source:** `src/core/`
- **Output:** `src/core/build/libgraph.{a,so,dylib}`
- **Build tool:** Make + GCC/Clang

### 2. Python Environment
- **Virtual env:** `.venv/`
- **Dependencies:** From `requirements.txt`
- **Packages:** Flask, pytest, etc.

### 3. React Frontend
- **Source:** `graph-ui/src/`
- **Output:** `graph-ui/dist/`
- **Build tool:** Vite + npm

---

## 🔧 Build Script Details

### `./build_local.sh`

**What it does:**
1. ✅ Check prerequisites (Python, Node.js, GCC)
2. 🔨 Build C library (`make` in `src/core/`)
3. 🐍 Setup Python venv and install dependencies
4. 🧪 Run test suite
5. ⚛️ Build React frontend (`npm run build`)

**Time:** ~2-3 minutes (first time)

**Output:**
```
✓ C Library
✓ Python Environment
✓ Tests
✓ Frontend
```

---

## 🚁 Deployment Script Details

### `./deploy_local.sh`

**What it does:**
1. Start QC Dashboard (port 5001)
2. Start Ontology API (port 5002)
3. Start React dev server (port 5173)
4. Monitor all services
5. Graceful shutdown on Ctrl+C

**Services:**

| Service | Port | URL |
|---------|------|-----|
| QC Dashboard | 5001 | http://localhost:5001 |
| Ontology API | 5002 | http://localhost:5002 |
| React Frontend | 5173 | http://localhost:5173 |

**Logs:**
- `logs/qc_dashboard.log`
- `logs/ontology_api.log`
- `logs/frontend.log`

---

## 📋 Prerequisites

### Required

- **Python 3.8+** (3.12+ recommended)
- **Make** (included with Xcode tools)
- **GCC or Clang** (for C library)

### Optional

- **Node.js 18+** (for frontend)
- **npm** (comes with Node.js)

### macOS Installation

```bash
# Install Xcode Command Line Tools (for GCC/make)
xcode-select --install

# Install Python (if not present)
# Download from: https://www.python.org/downloads/
# Or use system Python 3

# Install Node.js (optional, for frontend)
# Download from: https://nodejs.org/
# Or check if already installed: node --version
```

---

## 🔍 Build Components Individually

### C Library Only

```bash
cd src/core
make clean
make
cd ../..
```

**Check output:**
```bash
ls -lh src/core/build/
```

### Python Environment Only

```bash
./setup_venv.sh
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend Only

```bash
cd graph-ui
npm install
npm run build
# Output in dist/
```

---

## 🧪 Testing

### Run All Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

### Run Specific Test Layer

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Service layer only
pytest tests/unit/services/ -v
```

### With Coverage

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## 🏃 Running Services Manually

### QC Dashboard

```bash
source .venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 qc_dashboard.py
```

Open: http://localhost:5001

### Ontology API

```bash
source .venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 ontology_api.py
```

Open: http://localhost:5002

### Frontend Dev Server

```bash
cd graph-ui
npm run dev
```

Open: http://localhost:5173

---

## 🐛 Troubleshooting

### Build Fails: "make: command not found"

**Fix:**
```bash
xcode-select --install
```

### Build Fails: "C compiler not found"

**Fix:**
```bash
# Install Xcode Command Line Tools (recommended)
xcode-select --install

# Wait for installation to complete, then verify:
gcc --version  # or clang --version
```

### Python Import Errors

**Fix:**
```bash
source .venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### Port Already in Use

**Fix:**
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or use deployment script (auto-kills)
./deploy_local.sh
```

### Frontend Build Fails

**Fix:**
```bash
cd graph-ui
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Tests Failing

**Check:**
1. Is C library built? `ls src/core/build/`
2. Is venv activated? `echo $VIRTUAL_ENV`
3. Are dependencies installed? `pip list | grep flask`

**Fix:**
```bash
./build_local.sh  # Rebuild everything
```

---

## 📁 Directory Structure

```
WALLY-CLEAN/
├── build_local.sh          # Build script
├── deploy_local.sh         # Deployment script
├── setup_venv.sh           # Python venv setup
├── .venv/                  # Python virtual environment
├── requirements.txt        # Python dependencies
│
├── src/
│   ├── core/               # C library
│   │   ├── Makefile
│   │   ├── build/          # Compiled output
│   │   ├── include/        # Header files
│   │   └── src/            # C source files
│   │
│   ├── services/           # Python services
│   ├── adapters/           # Database adapters
│   └── api/                # API routes
│
├── graph-ui/               # React frontend
│   ├── package.json
│   ├── src/
│   ├── dist/               # Build output
│   └── node_modules/
│
├── tests/                  # Test suite
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── logs/                   # Runtime logs
│   ├── qc_dashboard.log
│   ├── ontology_api.log
│   └── frontend.log
│
└── docs/                   # Documentation
```

---

## 🔄 Development Workflow

### 1. Initial Setup (Once)

```bash
./build_local.sh
```

### 2. Start Development (Daily)

```bash
./deploy_local.sh
```

### 3. Make Changes

Edit code in:
- Python: `src/`
- C: `src/core/src/`
- React: `graph-ui/src/`

### 4. Rebuild After Changes

**Python changes:** Just restart service (auto-reloads)

**C changes:**
```bash
cd src/core && make && cd ../..
# Then restart Python services
```

**Frontend changes:**
```bash
# Dev server auto-reloads
# OR rebuild for production:
cd graph-ui && npm run build
```

### 5. Run Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

### 6. Commit

```bash
git add .
git commit -m "Description"
git push
```

---

## 🚀 Production Build

For production deployment (not local dev):

```bash
# Build everything optimized
./build_local.sh

# Check outputs
ls -lh src/core/build/        # C library
ls -lh graph-ui/dist/          # Frontend static files
source .venv/bin/activate && pip list  # Python packages

# Deploy to server (example)
rsync -av . user@server:/app/wally-clean/
ssh user@server 'cd /app/wally-clean && ./deploy_local.sh'
```

---

## 📊 Verification

### Check Build Status

```bash
# C library
ls -lh src/core/build/

# Python environment
source .venv/bin/activate && pip list

# Frontend
ls -lh graph-ui/dist/

# Tests
pytest tests/ --co  # List all tests
```

### Check Deployment Status

```bash
# Services running?
lsof -i :5001  # QC Dashboard
lsof -i :5002  # Ontology API
lsof -i :5173  # Frontend

# API health checks
curl http://localhost:5001/api/qc/status
curl http://localhost:5002/api/ontology/classes
curl http://localhost:5173/
```

---

## 🎯 Environment Variables

Optional configuration:

```bash
# .env file
PYTHONPATH=/path/to/WALLY-CLEAN
FLASK_ENV=development
FLASK_DEBUG=1

# API ports (if you want to change)
QC_PORT=5001
ONTOLOGY_PORT=5002
FRONTEND_PORT=5173
```

Load with:
```bash
export $(cat .env | xargs)
```

---

## 📚 Additional Resources

- [PYTHON_VENV_GUIDE.md](PYTHON_VENV_GUIDE.md) - Virtual environment details
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Testing approach
- [README.md](README.md) - Project overview
- [ONTOLOGY_EDITOR_PRODUCT.md](ONTOLOGY_EDITOR_PRODUCT.md) - Product spec

---

## ⚡ Quick Commands Reference

```bash
# Full build and deploy
./build_local.sh && ./deploy_local.sh

# Rebuild C library only
cd src/core && make clean && make && cd ../..

# Rebuild frontend only
cd graph-ui && npm run build && cd ..

# Run tests
source .venv/bin/activate && pytest tests/ -v

# Check what's running
lsof -i :5001 && lsof -i :5002 && lsof -i :5173

# Stop all services
lsof -ti:5001,5002,5173 | xargs kill -9

# View logs
tail -f logs/*.log
```

---

**Status:** ✅ Production Ready  
**Last Updated:** February 15, 2026  
**Tested on:** macOS (Apple Silicon & Intel)
