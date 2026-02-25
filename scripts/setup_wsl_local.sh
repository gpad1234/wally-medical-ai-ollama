#!/bin/bash

###############################################################################
# WSL2 Local Development Setup Script
# Version: 1.0
# Date: February 24, 2026
# Purpose: Initialize local development environment with Ollama + Medical AI
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    local missing=0

    # Check Python
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version | awk '{print $2}')
        print_success "Python 3 found: $python_version"
    else
        print_error "Python 3 not found"
        missing=1
    fi

    # Check Node.js
    if command -v node &> /dev/null; then
        node_version=$(node --version)
        print_success "Node.js found: $node_version"
    else
        print_error "Node.js not found"
        missing=1
    fi

    # Check npm
    if command -v npm &> /dev/null; then
        npm_version=$(npm --version)
        print_success "npm found: $npm_version"
    else
        print_error "npm not found"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        print_error "Missing prerequisites!"
        echo ""
        echo "Install on WSL2 Ubuntu:"
        echo "  sudo apt update && sudo apt install -y python3 python3-pip nodejs npm"
        exit 1
    fi

    echo ""
}

# Install Ollama on WSL2
install_ollama() {
    print_header "Ollama Setup"

    if command -v ollama &> /dev/null; then
        print_success "Ollama already installed: $(ollama --version 2>/dev/null || echo 'installed')"
        return
    fi

    print_info "Installing Ollama..."
    
    # WSL2-specific installation
    if ! command -v ollama &> /dev/null; then
        print_info "Downloading Ollama installer..."
        curl -fsSL https://ollama.ai/install.sh | bash
        
        if [ $? -eq 0 ]; then
            print_success "Ollama installed successfully"
        else
            print_error "Ollama installation failed"
            print_info "Manual installation: Visit https://ollama.ai"
            return 1
        fi
    fi
}

# Start Ollama service
start_ollama() {
    print_header "Starting Ollama Service"

    # Check if ollama is already running
    if pgrep -x "ollama" > /dev/null; then
        print_success "Ollama service already running"
        return
    fi

    print_info "Starting Ollama background service..."
    
    # Start Ollama in background
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    ollama_pid=$!
    
    # Wait for Ollama to be ready
    sleep 3
    
    if pgrep -x "ollama" > /dev/null; then
        print_success "Ollama started (PID: $ollama_pid)"
        print_info "Logs available at: /tmp/ollama.log"
    else
        print_error "Failed to start Ollama"
        cat /tmp/ollama.log
        exit 1
    fi
}

# Pull LLM model
pull_llm_model() {
    print_header "Pulling LLM Model"

    local model="llama3.2:1b"
    local model_alt="llama3.2:3b"
    
    print_info "Checking available models..."
    
    # Check which model to pull
    local choice="1"
    if [ -t 0 ]; then  # If interactive
        echo ""
        echo "Which model would you like?"
        echo "  1) llama3.2:1b (faster, ~1GB, lower quality)"
        echo "  2) llama3.2:3b (slower, ~2GB, better quality)"
        read -p "Enter choice (1 or 2): " choice
    fi

    if [ "$choice" = "2" ]; then
        model=$model_alt
    fi

    print_info "Pulling model: $model (this may take 5-10 minutes)..."
    
    if ollama pull $model; then
        print_success "Model $model pulled successfully"
    else
        print_error "Failed to pull model"
        exit 1
    fi
}

# Build C shared libraries
build_c_libraries() {
    print_header "Building C Shared Libraries"

    local simple_db_c="src/core/src/simple_db.c"
    local out_lib="src/core/build/lib/libsimpledb.so"

    if [ ! -f "$simple_db_c" ]; then
        print_warning "$simple_db_c not found — skipping C library build"
        return
    fi

    if ! command -v gcc &> /dev/null; then
        print_error "gcc not found. Install with: sudo apt install build-essential"
        exit 1
    fi

    mkdir -p src/core/build/lib
    gcc -shared -fPIC -Wall -O2 "$simple_db_c" -o "$out_lib"

    if [ $? -eq 0 ]; then
        print_success "Built: $out_lib ($(du -sh $out_lib | cut -f1))"
    else
        print_error "Failed to build $out_lib"
        exit 1
    fi
}

# Setup Python virtual environment
setup_python_env() {
    print_header "Python Dependencies"

    local venv_dir=".venv"

    # Create virtual environment if it doesn't exist
    if [ ! -d "$venv_dir" ]; then
        print_info "Creating Python virtual environment in .venv/ ..."
        python3 -m venv "$venv_dir"
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi

    # Activate virtual environment
    source "$venv_dir/bin/activate"
    print_success "Virtual environment activated"

    # Upgrade pip silently
    pip install --upgrade pip --quiet

    if [ -f "requirements.txt" ]; then
        print_info "Installing Python requirements..."
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found"
    fi

    # Write an activate helper script for convenience
    cat > activate_venv.sh << 'VENVEOF'
#!/bin/bash
source .venv/bin/activate
echo "Python venv activated. To deactivate: deactivate"
VENVEOF
    chmod +x activate_venv.sh
}

# Setup Node.js dependencies
setup_node_env() {
    print_header "Node.js Dependencies"

    # Setup React frontend
    if [ -d "graph-ui" ]; then
        print_info "Installing React UI dependencies..."
        cd graph-ui
        npm install
        cd ..
        print_success "React UI dependencies installed"
    fi

    # Setup LLM service
    if [ -d "ubuntu-deploy" ]; then
        print_info "Installing LLM service dependencies..."
        cd ubuntu-deploy
        npm install
        cd ..
        print_success "LLM service dependencies installed"
    fi
}

# Create startup script
create_startup_script() {
    print_header "Creating Startup Scripts"

    # Main startup script
    cat > start_local_dev.sh << 'EOF'
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
EOF

    chmod +x start_local_dev.sh
    print_success "Created: start_local_dev.sh"

    # Individual service startup scripts
    cat > start_flask.sh << 'EOF'
#!/bin/bash
echo "Starting Flask Ontology API on http://localhost:5002"
source .venv/bin/activate
python3 ontology_api.py
EOF

    chmod +x start_flask.sh
    print_success "Created: start_flask.sh"

    cat > start_react.sh << 'EOF'
#!/bin/bash
echo "Starting React UI on http://localhost:5173"
cd graph-ui
npm run dev
EOF

    chmod +x start_react.sh
    print_success "Created: start_react.sh"

    cat > start_llm.sh << 'EOF'
#!/bin/bash
echo "Starting LLM Service on http://localhost:3001"
cd ubuntu-deploy
node llm-service.js
EOF

    chmod +x start_llm.sh
    print_success "Created: start_llm.sh"
}

# Summary and next steps
print_summary() {
    print_header "Setup Complete! 🎉"

    echo ""
    echo "Next Steps:"
    echo ""
    echo "1. Quick Start (easiest):"
    echo "   ./start_local_dev.sh"
    echo ""
    echo "2. Or start services manually in separate terminals:"
    echo ""
    echo "   TERMINAL 1:"
    echo "   ./start_flask.sh"
    echo ""
    echo "   TERMINAL 2:"
    echo "   ./start_react.sh"
    echo ""
    echo "   TERMINAL 3:"
    echo "   ./start_llm.sh"
    echo ""
    echo "3. Then open in browser:"
    echo "   http://localhost:5173"
    echo ""
    echo "Useful Commands:"
    echo "  • Activate Python venv: source .venv/bin/activate  (or ./activate_venv.sh)"
    echo "  • Check Ollama status:  pgrep ollama"
    echo "  • Check services:       curl http://localhost:5002/api/ontology/health"
    echo "  • View Ollama logs:     tail -f /tmp/ollama.log"
    echo "  • Kill Ollama:          pkill ollama"
    echo ""
}

# Main execution
main() {
    print_header "WSL2 Medical AI Local Setup"
    echo "Workspace: $(pwd)"
    echo "Date: $(date)"
    echo ""

    check_prerequisites
    build_c_libraries
    install_ollama
    start_ollama
    pull_llm_model
    setup_python_env
    setup_node_env
    create_startup_script
    print_summary
}

# Run main function
main
