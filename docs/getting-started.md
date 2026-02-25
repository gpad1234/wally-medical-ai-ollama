---
layout: default
title: Getting Started
---

# 🚀 Getting Started

Get up and running with WALLY in minutes! This guide covers local development setup and basic usage.

---

## Prerequisites

### Required Software

- **Python 3.12+** - Core runtime  
- **Node.js 18+** - Frontend build tooling  
- **npm 10+** - Package manager  
- **Git** - Version control  

### Optional (for C libraries)

- **gcc** - C compiler (if rebuilding core libraries)
- **make** - Build automation

---

## Quick Start (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/gpad1234/Startup-One-Wally-Clean.git
cd Startup-One-Wally-Clean
```

### 2. Set Up Backend

```bash
# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# Start API server
python3 ontology_api.py
```

The API will start on **http://localhost:5002**

### 3. Set Up Frontend

In a new terminal:

```bash
cd graph-ui
npm install
npm run dev
```

The frontend will start on **http://localhost:5173**

### 4. Start the LLM Service *(for NLP symptom extraction)*

In a third terminal (requires [Ollama](https://ollama.com/) installed):

```bash
ollama pull llama3.2:1b
cd ubuntu-deploy && npm install && node llm-service.js
# Running on http://localhost:3001
```

> Skip this step to use **Click Mode** only — NLP mode will show a connection error but the rest of the app works fine.

### 5. Open Your Browser

Visit **http://localhost:5173** and you'll see:

✅ Fish-eye graph visualization  
✅ Interactive MiniMap in bottom-right  
✅ Radius control slider  
✅ Medical AI Reasoner tab (🏥)  
✅ DOID badges, ICD-10 codes, and MeSH references on each disease card

---

## First Steps with WALLY

### Explore the Demo Ontology

The default demo includes a simple class hierarchy:

```
owl:Thing (root)
├── demo:Person
│   ├── demo:Employee
│   ├── demo:Professor
│   └── demo:Student
├── demo:name (property)
└── demo:email (property)
```

### Try the Ontology Editor

1. **Click any node** — Watch the graph recenter with fish-eye effect
2. **Adjust radius slider** — Change viewport depth (1-5 hops)
3. **Use MiniMap** — Click, drag, or scroll to navigate
4. **Observe scaling** — Notice how node sizes change with distance

### Try the Medical AI Reasoner

1. Click the **🏥 Medical AI Reasoner** tab
2. **Click Mode** — Select symptoms from the visual panel, click **Diagnose**
3. **NLP Mode** — Click "💬 Describe with AI", type free-text symptoms in plain English
4. Each result card shows:
   - Confidence percentage + reasoning trace
   - Official **DOID badge** (links to disease-ontology.org)
   - **ICD-10-CM code** (e.g., J18.9, J11.1, I10)
   - **MeSH reference** and verbatim clinical definition
   - Suggested treatments and severity level

---

## Project Structure

```
WALLY-CLEAN/
├── ontology_api.py          # Flask REST API (741 lines)
├── graph_db.py              # GraphDB wrapper
├── requirements.txt          # Python dependencies
│
├── src/
│   ├── core/                # C libraries (libsimpledb.so)
│   │   ├── Makefile
│   │   ├── src/*.c
│   │   └── include/*.h
│   └── services/
│       ├── graph_pagination_service.py  # BFS fish-eye algorithm
│       └── ontology_service.py
│
├── graph-ui/                # React frontend
│   ├── package.json
│   ├── vite.config.js       # Build config + dev proxy
│   └── src/
│       ├── App.jsx          # Main app with tabs
│       └── components/
│           └── Ontology/
│               ├── VirtualizedGraphView.jsx  # Fish-eye viz
│               └── PaginationTest.jsx        # API test UI
│
├── docs/                    # GitHub Pages documentation
│   ├── index.md
│   ├── features.md
│   └── ...
│
└── deploy/                  # Deployment configs
    ├── systemd/
    └── nginx/
```

---

## API Endpoints

Test the API directly with curl:

### Get Paginated Node List

```bash
curl "http://localhost:5002/api/ontology/graph/nodes?skip=0&limit=10"
```

### Get Fish-Eye Viewport

```bash
curl -X POST "http://localhost:5002/api/ontology/graph/viewport" \
  -H "Content-Type: application/json" \
  -d '{
    "center_node": "owl:Thing",
    "radius": 2,
    "limit": 50
  }'
```

### Get Node Neighbors

```bash
curl "http://localhost:5002/api/ontology/graph/neighbors/demo:Person"
```

---

## Configuration

### Backend Configuration

Edit `ontology_api.py` to customize:

```python
# Port configuration
PORT = 5002

# CORS settings
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"]
    }
})

# Demo data
def init_demo_data():
    # Customize your demo ontology here
    pass
```

### Frontend Configuration

Edit `graph-ui/vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5002',
        changeOrigin: true
      }
    }
  }
})
```

Edit `graph-ui/src/components/Ontology/VirtualizedGraphView.jsx`:

```javascript
// Default viewport settings
const initialCenter = 'owl:Thing';
const initialRadius = 2;

// Fish-eye scaling factors
const scales = [1.8, 1.3, 1.0, 0.7, 0.5];
const opacities = [1, 0.95, 0.85, 0.7, 0.5];
```

---

## Loading Your Own Ontology

### Option 1: Import from File

Edit `ontology_api.py` to load from RDF/OWL file:

```python
from rdflib import Graph

# Load your ontology
g = Graph()
g.parse("path/to/your/ontology.owl", format="xml")

# Initialize with your data
ontology_service = OntologyService(g)
```

### Option 2: Use API to Add Nodes

```python
# Add class
POST /api/classes
{
  "class_uri": "http://example.org/MyClass",
  "label": "My Class",
  "description": "A custom class"
}

# Add property
POST /api/properties
{
  "property_uri": "http://example.org/myProperty",
  "label": "My Property",
  "property_type": "data"
}
```

### Option 3: Connect to External Triplestore

```python
from rdflib import Graph
from rdflib.plugins.stores import sparqlstore

# Connect to SPARQL endpoint
store = sparqlstore.SPARQLStore()
store.open("http://your-sparql-endpoint/sparql")
g = Graph(store)
```

---

## Development Workflow

### 1. Make Changes

Edit files in `src/` or `graph-ui/src/`

### 2. Backend Auto-Reload

Flask automatically reloads on Python file changes (if debug=True):

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
```

### 3. Frontend Hot Reload

Vite automatically hot-reloads on React file changes - just save and see updates!

### 4. Test Changes

- Open browser console (F12) to see debug logs
- Use PaginationTest component for API testing
- Check API logs in terminal

---

## Common Issues & Solutions

### Port Already in Use

```bash
# Kill process on port 5002
lsof -ti :5002 | xargs kill -9

# Kill process on port 5173
lsof -ti :5173 | xargs kill -9
```

### C Library Not Found

```bash
# Rebuild C libraries
cd src/core
make clean
make
cd ../..
```

### Frontend Not Fetching Data

Check Vite proxy configuration in `graph-ui/vite.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5002',
    changeOrigin: true,
    secure: false
  }
}
```

### CORS Errors

Ensure backend CORS is configured for frontend origin:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:5002"]
    }
})
```

---

## Testing

### Manual Testing

1. Start backend and frontend
2. Open http://localhost:5173
3. Test each feature:
   - Click nodes to recenter
   - Adjust radius slider
   - Use MiniMap navigation
   - Check browser console for errors

### API Testing

Use the built-in PaginationTest component:

1. Navigate to "Pagination Tests" tab
2. Click "Test Nodes List"
3. Click "Test Viewport"
4. Click "Test Neighbors"

### Unit Tests (Coming Soon)

```bash
# Backend tests
pytest tests/

# Frontend tests  
cd graph-ui
npm test
```

---

## Next Steps

Now that you have WALLY running locally:

1. **Explore Features** - [Read the Features Guide →](features)
2. **Understand Architecture** - [Architecture Overview →](architecture)
3. **Deploy to Production** - [Deployment Guide →](deployment)
4. **Contribute** - [Development Guide →](development)

---

## Quick Reference

### Start Development Servers

```bash
# Terminal 1: Backend
python3 ontology_api.py

# Terminal 2: Frontend
cd graph-ui && npm run dev
```

### Access URLs

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5002
- **API Docs:** http://localhost:5002/api/docs (coming soon)

### Useful Commands

```bash
# Restart backend
pkill -f "python3 ontology_api.py"
python3 ontology_api.py

# Rebuild frontend
cd graph-ui
npm run build

# View logs
tail -f logs/ontology_api.log
```

---

## Getting Help

- **GitHub Issues:** [Report bugs or request features](https://github.com/gpad1234/Startup-One-Wally-Clean/issues)
- **Documentation:** [Full docs on GitHub Pages](https://gpad1234.github.io/Startup-One-Wally-Clean/)
- **Live Demo:** [Try it online](http://161.35.239.151)

---

[← Back to Home](./) | [Features →](features)
