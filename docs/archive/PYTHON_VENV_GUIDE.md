# Python Virtual Environment Guide

## Quick Start

### 1. Setup Virtual Environment (First Time Only)

```bash
./setup_venv.sh
```

This will:
- Create `.venv` directory
- Install all dependencies from `requirements.txt`
- Activate the environment

### 2. Activate Virtual Environment (Each Terminal Session)

```bash
source .venv/bin/activate
```

You'll see `(.venv)` prefix in your terminal prompt when activated.

### 3. Deactivate Virtual Environment

```bash
deactivate
```

---

## Why Use Virtual Environment?

✅ **Isolated Dependencies** - Each project has its own packages  
✅ **Version Control** - Avoid conflicts between project requirements  
✅ **Clean System** - Don't pollute global Python installation  
✅ **Reproducible** - Easy to replicate environment on other machines  

---

## Project Structure

```
WALLY-CLEAN/
├── .venv/                 # Virtual environment (excluded from git)
├── requirements.txt       # Python dependencies
├── setup_venv.sh         # Setup script
├── start_qc.sh           # Auto-activates venv if available
├── start_ontology.sh     # Auto-activates venv if available
└── ...
```

---

## Python Version

**Required:** Python 3.8+  
**Recommended:** Python 3.12+

Check your version:
```bash
python3 --version
```

---

## Managing Dependencies

### Install New Package

```bash
# Activate venv first
source .venv/bin/activate

# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Install from requirements.txt

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### List Installed Packages

```bash
source .venv/bin/activate
pip list
```

### Upgrade Package

```bash
source .venv/bin/activate
pip install --upgrade package-name
```

---

## Automatic Activation

The startup scripts (`start_qc.sh`, `start_ontology.sh`) automatically activate the virtual environment if `.venv` exists.

**Manual scripts:**

```bash
# Run demo
source .venv/bin/activate
python3 ontology_demo.py

# Run tests
source .venv/bin/activate
pytest tests/
```

---

## Troubleshooting

### Issue: `command not found: python3`

**Solution:** Install Python 3
```bash
# macOS - Download from https://www.python.org/downloads/
# Or check if already installed:
python3 --version

# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv
```

### Issue: `No module named 'flask'`

**Solution:** Install dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Virtual environment broken

**Solution:** Recreate it
```bash
rm -rf .venv
./setup_venv.sh
```

### Issue: Wrong Python version in venv

**Solution:** Specify Python version
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'

- name: Create virtual environment
  run: |
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

- name: Run tests
  run: |
    source .venv/bin/activate
    pytest tests/
```

---

## Best Practices

1. **Always activate venv** before installing packages
2. **Keep requirements.txt updated** when adding dependencies
3. **Add .venv to .gitignore** (already done)
4. **Document Python version** in README
5. **Use pip freeze** to capture exact versions

---

## Current Project Dependencies

See `requirements.txt` for full list:

**Core:**
- flask - Web framework
- flask-cors - CORS support
- pytest - Testing framework
- pytest-cov - Coverage reports

**Optional:**
- pytest-json-report - JSON test results (if using QC dashboard)

---

## Quick Commands Reference

```bash
# Setup
./setup_venv.sh

# Activate
source .venv/bin/activate

# Deactivate
deactivate

# Install packages
pip install package-name

# Save dependencies
pip freeze > requirements.txt

# Run tests (with venv)
source .venv/bin/activate && pytest tests/

# Start QC Dashboard (auto-activates venv)
./start_qc.sh

# Start Ontology API (auto-activates venv)
./start_ontology.sh
```

---

## Environment Variables

Set in shell or `.env` file:

```bash
# Example .env
PYTHONPATH=/Users/gp/claude-code/startup-one/WALLY-CLEAN:$PYTHONPATH
FLASK_ENV=development
FLASK_DEBUG=1
```

Load with:
```bash
source .venv/bin/activate
export $(cat .env | xargs)
```

---

**Note:** The startup scripts automatically handle PYTHONPATH and virtual environment activation!
