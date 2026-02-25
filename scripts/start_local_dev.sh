#!/bin/bash
# Local Development Startup Script

echo "Starting WALLY Medical AI Local Development..."
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi

# Create terminal multiplexer instruction
echo "=========================================="
echo "Starting Services (3 terminals needed):"
echo "=========================================="
echo ""
echo "TERMINAL 1 - Flask API:"
echo "  python3 ontology_api.py"
echo "  → http://localhost:5002"
echo ""
echo "TERMINAL 2 - React UI:"
echo "  cd graph-ui && npm run dev"
echo "  → http://localhost:5173"
echo ""
echo "TERMINAL 3 - LLM Service:"
echo "  cd ubuntu-deploy && node llm-service.js"
echo "  → http://localhost:3001"
echo ""
echo "Test the system:"
echo "  → Open http://localhost:5173 in browser"
echo ""
echo "=========================================="
