#!/bin/bash
# Run both Flask and React servers in one command

# Detect project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

echo "🚀 Starting Graph UI Application"
echo "================================"
echo ""

# Kill any existing Flask/React processes
echo "Cleaning up old processes..."
pkill -f "graph_web_ui.py" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
sleep 2

# Kill processes by port as backup
lsof -i :5001 2>/dev/null | tail -n +2 | awk '{print $2}' | xargs kill -9 2>/dev/null || true
lsof -i :5173 2>/dev/null | tail -n +2 | awk '{print $2}' | xargs kill -9 2>/dev/null || true
sleep 1

# Start Flask backend
echo "🟦 Starting Flask API on http://127.0.0.1:5001..."
cd "$PROJECT_DIR"
$VENV_PYTHON graph_web_ui.py &
FLASK_PID=$!
echo "   (PID: $FLASK_PID)"
sleep 3

# Verify Flask started
if ! kill -0 $FLASK_PID 2>/dev/null; then
    echo "❌ Flask failed to start (PID $FLASK_PID not found)"
    exit 1
fi

# Quick API test
if ! curl -s http://127.0.0.1:5001/api/graph/stats > /dev/null 2>&1; then
    echo "⚠️  Flask started but API not responding yet, waiting..."
    sleep 2
fi
echo "✅ Flask running"
echo ""

# Start React frontend
echo "⚛️  Starting React UI on http://localhost:5173..."
cd "$PROJECT_DIR/graph-ui"
## Start React (Vite) detached and capture logs; redirect stdin to avoid suspension
nohup npm run dev </dev/null > /tmp/react_nohup.log 2>&1 &
REACT_PID=$!
echo "   (PID: $REACT_PID)"
sleep 3

# Verify React started
if ! kill -0 $REACT_PID 2>/dev/null; then
    echo "❌ React failed to start (PID $REACT_PID not found)"
    kill $FLASK_PID 2>/dev/null || true
    echo "--- React log ---"
    tail -n 100 /tmp/react_nohup.log 2>/dev/null || true
    exit 1
fi

# Try to extract the actual local URL (Vite may pick a different port)
REACT_URL="$(grep -m1 'Local:' /tmp/react_nohup.log | sed -E 's/.*Local:[[:space:]]*([^ ]+).*/\1/' 2>/dev/null || true)"
if [ -n "$REACT_URL" ]; then
    echo "✅ React running at $REACT_URL"
else
    echo "✅ React running (see /tmp/react_nohup.log for details)"
fi
echo ""

echo "================================"
echo "✅ All services running!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔌 API:      http://127.0.0.1:5001"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $FLASK_PID 2>/dev/null || true
    kill $REACT_PID 2>/dev/null || true
    sleep 1
    pkill -f "graph_web_ui.py" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    echo "✅ Services stopped"
    exit 0
}

trap cleanup INT TERM

# Wait indefinitely - cleanup will be called on Ctrl+C or termination signal
wait
