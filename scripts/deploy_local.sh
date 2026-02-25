#!/bin/bash
# Local Deployment Script for WALLY-CLEAN
# Starts all services for local development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     WALLY-CLEAN Local Deployment              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if build was run
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo "Run ./build_local.sh first to build the project"
    exit 1
fi

# Activate venv
source .venv/bin/activate

# Function to check if port is in use
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Function to kill process on port
kill_port() {
    echo -e "${YELLOW}  → Killing process on port $1...${NC}"
    lsof -ti:$1 | xargs kill -9 2>/dev/null || true
    sleep 1
}

# PID tracking
PIDS=()

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"
    
    for pid in "${PIDS[@]}"; do
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null || true
        fi
    done
    
    # Kill by port as backup
    kill_port 5001
    kill_port 5002
    kill_port 5173
    
    echo -e "${GREEN}✓${NC} All services stopped"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# ============================================
# Service 1: QC Dashboard (Port 5001)
# ============================================
echo -e "${CYAN}[1/3] Starting QC Dashboard...${NC}"

if check_port 5001; then
    echo -e "${YELLOW}⚠️  Port 5001 already in use${NC}"
    kill_port 5001
fi

export PYTHONPATH="$(pwd):$PYTHONPATH"

echo -e "${GREEN}  → Starting on http://localhost:5001${NC}"
python3 qc_dashboard.py > logs/qc_dashboard.log 2>&1 &
PIDS+=($!)
QC_PID=$!

# Wait for service to start
sleep 2

if check_port 5001; then
    echo -e "${GREEN}✓${NC} QC Dashboard running (PID: $QC_PID)"
else
    echo -e "${RED}✗${NC} QC Dashboard failed to start"
    echo "Check logs/qc_dashboard.log for details"
fi

echo ""

# ============================================
# Service 2: Ontology API (Port 5002)
# ============================================
echo -e "${CYAN}[2/3] Starting Ontology Editor API...${NC}"

if check_port 5002; then
    echo -e "${YELLOW}⚠️  Port 5002 already in use${NC}"
    kill_port 5002
fi

if [ -f "ontology_api.py" ]; then
    echo -e "${GREEN}  → Starting on http://localhost:5002${NC}"
    python3 ontology_api.py > logs/ontology_api.log 2>&1 &
    PIDS+=($!)
    ONTO_PID=$!
    
    # Wait for service to start
    sleep 2
    
    if check_port 5002; then
        echo -e "${GREEN}✓${NC} Ontology API running (PID: $ONTO_PID)"
    else
        echo -e "${RED}✗${NC} Ontology API failed to start"
        echo "Check logs/ontology_api.log for details"
    fi
else
    echo -e "${YELLOW}⚠️  ontology_api.py not found, skipping${NC}"
fi

echo ""

# ============================================
# Service 3: React Frontend (Port 5173)
# ============================================
echo -e "${CYAN}[3/3] Starting React Frontend...${NC}"

if [ -d "graph-ui" ]; then
    cd graph-ui
    
    if check_port 5173; then
        echo -e "${YELLOW}⚠️  Port 5173 already in use${NC}"
        cd ..
        kill_port 5173
        cd graph-ui
    fi
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}  → Installing dependencies...${NC}"
        npm install --quiet
    fi
    
    echo -e "${GREEN}  → Starting on http://localhost:5173${NC}"
    npm run dev > ../logs/frontend.log 2>&1 &
    PIDS+=($!)
    FRONTEND_PID=$!
    
    cd ..
    
    # Wait for service to start
    sleep 3
    
    if check_port 5173; then
        echo -e "${GREEN}✓${NC} React Frontend running (PID: $FRONTEND_PID)"
    else
        echo -e "${RED}✗${NC} Frontend failed to start"
        echo "Check logs/frontend.log for details"
    fi
else
    echo -e "${YELLOW}⚠️  graph-ui directory not found, skipping${NC}"
fi

echo ""

# ============================================
# Deployment Summary
# ============================================
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Services Running                           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

SERVICES_OK=true

if check_port 5001; then
    echo -e "${GREEN}✓${NC} QC Dashboard:      ${CYAN}http://localhost:5001${NC}"
else
    echo -e "${RED}✗${NC} QC Dashboard:      Not running"
    SERVICES_OK=false
fi

if check_port 5002; then
    echo -e "${GREEN}✓${NC} Ontology API:      ${CYAN}http://localhost:5002${NC}"
else
    echo -e "${YELLOW}⊘${NC} Ontology API:      Not running"
fi

if check_port 5173; then
    echo -e "${GREEN}✓${NC} React Frontend:    ${CYAN}http://localhost:5173${NC}"
else
    echo -e "${YELLOW}⊘${NC} React Frontend:    Not running"
fi

echo ""

if [ "$SERVICES_OK" = true ]; then
    echo -e "${GREEN}✨ Deployment successful!${NC}"
else
    echo -e "${YELLOW}⚠️  Some services failed to start${NC}"
fi

echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  QC Dashboard:    logs/qc_dashboard.log"
echo -e "  Ontology API:    logs/ontology_api.log"
echo -e "  Frontend:        logs/frontend.log"
echo ""

echo -e "${BLUE}Quick Tests:${NC}"
echo -e "  curl http://localhost:5001/api/qc/status"
echo -e "  curl http://localhost:5002/api/ontology/classes"
echo ""

echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Keep script running
wait
