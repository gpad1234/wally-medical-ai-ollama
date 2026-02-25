#!/bin/bash
# Quick Start Script - Build and Deploy WALLY-CLEAN in one command

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     WALLY-CLEAN Quick Start                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Build
echo -e "${GREEN}Step 1: Building...${NC}"
./build_local.sh

if [ $? -ne 0 ]; then
    echo "Build failed. Please check errors above."
    exit 1
fi

echo ""
echo -e "${GREEN}Step 2: Deploying...${NC}"
echo ""
sleep 2

# Step 2: Deploy
./deploy_local.sh
