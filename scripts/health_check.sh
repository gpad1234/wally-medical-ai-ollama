#!/bin/bash
# Health Check Script - Verify all services are running correctly

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     WALLY-CLEAN Health Check                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

ERRORS=0

# Check QC Dashboard
echo -ne "QC Dashboard (5001)... "
if curl -s http://localhost:5001/api/qc/status > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not responding${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check Ontology API
echo -ne "Ontology API (5002)... "
if curl -s http://localhost:5002/api/ontology/statistics > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⊘ Not running (optional)${NC}"
fi

# Check Frontend
echo -ne "Frontend (5173)...     "
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⊘ Not running (optional)${NC}"
fi

echo ""

# Check Python environment
echo -ne "Python venv...         "
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓ Present${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check C library
echo -ne "C library build...     "
if [ -f "src/core/build/libgraph.a" ] || [ -f "src/core/build/libgraph.so" ] || [ -f "src/core/build/libgraph.dylib" ]; then
    echo -e "${GREEN}✓ Built${NC}"
else
    echo -e "${YELLOW}⚠ Not found${NC}"
fi

# Check frontend build
echo -ne "Frontend build...      "
if [ -d "graph-ui/dist" ]; then
    echo -e "${GREEN}✓ Built${NC}"
else
    echo -e "${YELLOW}⚠ Not built${NC}"
fi

echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✨ System healthy!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  $ERRORS critical component(s) missing${NC}"
    echo ""
    echo "Run: ./build_local.sh && ./deploy_local.sh"
    exit 1
fi
