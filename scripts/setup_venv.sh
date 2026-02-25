#!/bin/bash
# Setup Python Virtual Environment for WALLY-CLEAN

echo "🐍 Setting up Python Virtual Environment"
echo "========================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python version: $PYTHON_VERSION"
echo ""

# Check if venv already exists
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists at .venv"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing old venv..."
        rm -rf .venv
    else
        echo "Using existing venv"
        source .venv/bin/activate
        echo "✅ Activated existing virtual environment"
        echo ""
        echo "Python: $(which python3)"
        echo "Pip: $(which pip3)"
        exit 0
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate it
source .venv/bin/activate

echo "✅ Virtual environment created and activated!"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo ""
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed!"
else
    echo ""
    echo "⚠️  No requirements.txt found"
    echo "Installing basic dependencies..."
    pip install flask flask-cors pytest pytest-cov
fi

echo ""
echo "========================================"
echo "✨ Setup Complete!"
echo "========================================"
echo ""
echo "Virtual environment location: .venv"
echo "Python: $(which python3)"
echo "Pip: $(which pip3)"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "Installed packages:"
pip list
