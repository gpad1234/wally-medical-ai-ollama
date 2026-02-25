#!/bin/bash

# QC Dashboard Startup Script
# Starts the Quality Control dashboard for automated testing

set -e

echo "🧪 WALLY-CLEAN Quality Control Dashboard"
echo "=========================================="
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "ℹ️  No virtual environment found (run ./setup_venv.sh to create one)"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check dependencies
echo "📦 Checking dependencies..."
pip3 show flask flask-cors pytest > /dev/null 2>&1 || {
    echo "⚠️  Missing dependencies. Installing..."
    pip3 install -r requirements.txt
}

# Install pytest-json-report if not present
pip3 show pytest-json-report > /dev/null 2>&1 || {
    echo "📊 Installing pytest-json-report..."
    pip3 install pytest-json-report
}

echo "✓ All dependencies installed"
echo ""

# Create necessary directories
mkdir -p test_results
mkdir -p templates

echo "✓ Directories created"
echo ""

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export QC_PORT="${QC_PORT:-5001}"
export QC_DEBUG="${QC_DEBUG:-false}"

# Display startup info
echo "📍 Working directory: $(pwd)"
echo "🌐 Dashboard will be available at: http://localhost:${QC_PORT}"
echo "🔧 Debug mode: ${QC_DEBUG}"
echo ""
echo "🚀 Starting QC Dashboard..."
echo ""

# Start the dashboard
python3 qc_dashboard.py

# If the dashboard stops, show why
echo ""
echo "⚠️  QC Dashboard stopped"
