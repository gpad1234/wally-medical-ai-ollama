#!/bin/bash
# Complete Local Build Script for WALLY-CLEAN
# Builds C library, sets up Python, and builds React frontend

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     WALLY-CLEAN Local Build System            ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo ""

# Track build status
BUILD_STATUS=()

# ============================================
# Step 1: Check Prerequisites
# ============================================
echo -e "${YELLOW}[1/5] Checking Prerequisites...${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Python: $PYTHON_VERSION"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js not found (needed for frontend)${NC}"
    echo "  Download from: https://nodejs.org/"
    NODE_OK=false
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js: $NODE_VERSION"
    NODE_OK=true
fi

# Check GCC/Clang
if ! command -v gcc &> /dev/null && ! command -v clang &> /dev/null; then
    echo -e "${YELLOW}⚠️  GCC/Clang not found (needed for C library)${NC}"
    echo "  Install with: xcode-select --install"
    CC_OK=false
else
    if command -v gcc &> /dev/null; then
        CC_VERSION=$(gcc --version | head -n1)
        echo -e "${GREEN}✓${NC} GCC: $CC_VERSION"
    else
        CC_VERSION=$(clang --version | head -n1)
        echo -e "${GREEN}✓${NC} Clang: $CC_VERSION"
    fi
    CC_OK=true
fi

# Check make
if ! command -v make &> /dev/null; then
    echo -e "${RED}❌ make not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} make: $(make --version | head -n1)"

echo ""

# ============================================
# Step 2: Build C Library
# ============================================
echo -e "${YELLOW}[2/5] Building C Library (GraphDB Core)...${NC}"
echo ""

if [ "$CC_OK" = true ]; then
    cd src/core
    
    # Clean previous build
    if [ -f "Makefile" ]; then
        echo "Cleaning previous build..."
        make clean 2>/dev/null || true
        
        echo "Compiling C library..."
        if make; then
            echo -e "${GREEN}✓${NC} C library built successfully"
            BUILD_STATUS+=("✓ C Library")
            
            # Check if library was created
            if [ -f "build/libgraph.a" ] || [ -f "build/libgraph.so" ] || [ -f "build/libgraph.dylib" ]; then
                echo -e "${GREEN}  → Library file created in build/${NC}"
            fi
        else
            echo -e "${RED}✗${NC} C library build failed"
            BUILD_STATUS+=("✗ C Library")
        fi
    else
        echo -e "${YELLOW}⚠️  No Makefile found in src/core${NC}"
        BUILD_STATUS+=("⚠ C Library (no Makefile)")
    fi
    
    cd ../..
else
    echo -e "${YELLOW}⚠️  Skipping C library build (no compiler)${NC}"
    BUILD_STATUS+=("⊘ C Library (skipped)")
fi

echo ""

# ============================================
# Step 3: Setup Python Environment
# ============================================
echo -e "${YELLOW}[3/5] Setting up Python Environment...${NC}"
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate venv
source .venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    if pip install -r requirements.txt --quiet; then
        echo -e "${GREEN}✓${NC} Python dependencies installed"
        BUILD_STATUS+=("✓ Python Environment")
    else
        echo -e "${RED}✗${NC} Failed to install Python dependencies"
        BUILD_STATUS+=("✗ Python Environment")
    fi
else
    echo -e "${YELLOW}⚠️  No requirements.txt found${NC}"
    BUILD_STATUS+=("⚠ Python Environment")
fi

# Show installed packages
PACKAGE_COUNT=$(pip list --format=freeze | wc -l | tr -d ' ')
echo -e "${GREEN}  → $PACKAGE_COUNT packages installed${NC}"

echo ""

# ============================================
# Step 4: Run Python Tests
# ============================================
echo -e "${YELLOW}[4/5] Running Python Tests...${NC}"
echo ""

if command -v pytest &> /dev/null; then
    echo "Running test suite..."
    if pytest tests/ -v --tb=short 2>&1 | tail -20; then
        echo -e "${GREEN}✓${NC} All tests passed"
        BUILD_STATUS+=("✓ Tests")
    else
        echo -e "${YELLOW}⚠️  Some tests failed${NC}"
        BUILD_STATUS+=("⚠ Tests")
    fi
else
    echo -e "${YELLOW}⚠️  pytest not found, skipping tests${NC}"
    BUILD_STATUS+=("⊘ Tests (skipped)")
fi

echo ""

# ============================================
# Step 5: Build React Frontend
# ============================================
echo -e "${YELLOW}[5/5] Building React Frontend...${NC}"
echo ""

if [ "$NODE_OK" = true ] && [ -d "graph-ui" ]; then
    cd graph-ui
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        if npm install --quiet; then
            echo -e "${GREEN}✓${NC} npm dependencies installed"
        else
            echo -e "${RED}✗${NC} npm install failed"
            BUILD_STATUS+=("✗ Frontend")
            cd ..
            exit 1
        fi
    else
        echo -e "${GREEN}✓${NC} npm dependencies already installed"
    fi
    
    # Build for production
    echo "Building React app for production..."
    if npm run build; then
        echo -e "${GREEN}✓${NC} React frontend built successfully"
        BUILD_STATUS+=("✓ Frontend")
        
        # Check dist directory
        if [ -d "dist" ]; then
            DIST_SIZE=$(du -sh dist | cut -f1)
            echo -e "${GREEN}  → Build output: dist/ ($DIST_SIZE)${NC}"
        fi
    else
        echo -e "${RED}✗${NC} Frontend build failed"
        BUILD_STATUS+=("✗ Frontend")
    fi
    
    cd ..
else
    if [ "$NODE_OK" = false ]; then
        echo -e "${YELLOW}⚠️  Skipping frontend build (Node.js not found)${NC}"
    else
        echo -e "${YELLOW}⚠️  Skipping frontend build (graph-ui not found)${NC}"
    fi
    BUILD_STATUS+=("⊘ Frontend (skipped)")
fi

echo ""

# ============================================
# Build Summary
# ============================================
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Build Summary                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

for status in "${BUILD_STATUS[@]}"; do
    echo -e "  $status"
done

echo ""

# Check if all critical components built successfully
if [[ " ${BUILD_STATUS[@]} " =~ " ✗ " ]]; then
    echo -e "${RED}⚠️  Build completed with errors${NC}"
    exit 1
else
    echo -e "${GREEN}✨ Build completed successfully!${NC}"
fi

echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Deploy locally: ${GREEN}./deploy_local.sh${NC}"
echo -e "  2. Start QC Dashboard: ${GREEN}./start_qc.sh${NC}"
echo -e "  3. Start Ontology API: ${GREEN}./start_ontology.sh${NC}"
echo -e "  4. Run frontend dev server: ${GREEN}cd graph-ui && npm run dev${NC}"
echo ""
