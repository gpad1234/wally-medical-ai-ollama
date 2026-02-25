#!/bin/bash
# Start Ontology Editor API Server

echo "🧠 Starting Ontology Editor API..."
echo "=================================="
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "ℹ️  No virtual environment found (run ./setup_venv.sh to create one)"
fi
echo ""

# Check if port 5002 is already in use
if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5002 is already in use"
    read -p "Kill existing process and restart? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Killing process on port 5002..."
        lsof -ti:5002 | xargs kill -9 2>/dev/null
        sleep 2
    else
        echo "Exiting..."
        exit 1
    fi
fi

# Set Python path
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Start the server
echo "Starting server on http://localhost:5002..."
echo ""
python3 ontology_api.py
