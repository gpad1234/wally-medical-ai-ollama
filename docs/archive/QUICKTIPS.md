# Quick Tips - Ontology Editor

## 🚀 Starting the System

### Quick Start (2 terminals)
```bash
# Terminal 1: Backend API
python3 ontology_api.py

# Terminal 2: React UI
cd graph-ui && npm run dev
```

**Access at:** http://localhost:5173  
**API Port:** 5002

---

## 📥 Importing RDF/OWL Files

### Via Web UI
1. Click **"📥 Import RDF/OWL"** button
2. Select file (`.owl`, `.rdf`, `.ttl`, `.n3`, `.nt`)
3. Wait for success message

### Via Command Line
```bash
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@sample_data/university.owl"
```

### Supported Formats
- **OWL/XML** - `.owl`, `.rdf`, `.xml`
- **Turtle** - `.ttl`, `.turtle`
- **N-Triples** - `.nt`
- **Notation3** - `.n3`

---

## 📤 Exporting Ontology

### Via Web UI
Click **"📤 Export RDF/OWL"** → Downloads as `.owl` file

### Via Command Line
```bash
# Export as OWL/XML
curl -O http://127.0.0.1:5002/api/ontology/export?format=xml

# Export as Turtle
curl -O http://127.0.0.1:5002/api/ontology/export?format=turtle

# Export as N-Triples
curl -O http://127.0.0.1:5002/api/ontology/export?format=nt
```

---

## 🧪 Testing with Sample Files

### Available Samples
```bash
sample_data/university.owl   # Academic domain (60 triples)
sample_data/animals.ttl       # Biology domain (73 triples)
sample_data/food.rdf          # Food/nutrition (58 triples)
```

### Quick Import Test
```bash
# Import university ontology
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@sample_data/university.owl"

# Expected result:
# Classes: 5, Properties: 8, Instances: 0
```

---

## 🔧 API Endpoints

### Health Check
```bash
curl http://127.0.0.1:5002/api/ontology/health
```

### Get All Classes
```bash
curl http://127.0.0.1:5002/api/ontology/classes
```

### Get Class Details
```bash
curl http://127.0.0.1:5002/api/ontology/classes/{classId}
```

### Get Statistics
```bash
curl http://127.0.0.1:5002/api/ontology/statistics
```

### Import (clear existing first)
```bash
curl -X POST "http://127.0.0.1:5002/api/ontology/import?clear=true" \
  -F "file=@yourfile.owl"
```

---

## 🐛 Troubleshooting

### Connection Refused Error
```
❌ Ontology API Error: Network Error
```
**Fix:** Start the backend API server:
```bash
python3 ontology_api.py
```

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Fix:** Kill the process or use a different port:
```bash
# Kill process on port 5002
lsof -ti:5002 | xargs kill -9

# Or kill by name
pkill -f ontology_api
```

### File Not Found
**Fix:** Use absolute or relative paths:
```bash
# Relative from WALLY-CLEAN directory
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@./sample_data/university.owl"

# Absolute path
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@/full/path/to/file.owl"
```

### rdflib Not Found
```
ModuleNotFoundError: No module named 'rdflib'
```
**Fix:** Install dependencies:
```bash
pip3 install -r requirements.txt
```

---

## 📊 Knowledge Graph Controls

### Navigation
- **Pan:** Click and drag background
- **Zoom:** Mouse wheel or trackpad pinch
- **Reset View:** Double-click background

### Visual Legend
- 🔵 **Blue Rectangles** = Classes
- 🟢 **Green Circles** = Instances
- 🟣 **Purple Boxes** = Properties
- **Arrows** = Relationships (subClassOf, instanceOf, hasProperty)

---

## 🔄 Git Workflow

### Get Latest Code
```bash
# On new machine
git clone https://github.com/gpad1234/Startup-One-Wally-Clean.git

# On existing clone
git pull origin main
git fetch --tags
```

### Current Version
```bash
# Check current commit
git log --oneline -1

# Check available tags
git tag -l

# Latest tag: rdf-import-samples
```

---

## 📦 Dependencies Check

### Python Requirements
```bash
# Check what's installed
pip3 list | grep -E "flask|rdflib|pytest"

# Install/update all
pip3 install -r requirements.txt
```

### React Requirements
```bash
cd graph-ui

# Check if node_modules exists
ls node_modules

# Install if missing
npm install
```

---

## ⚡ Performance Tips

### Large Ontologies
- Import may take 10-30 seconds for 1000+ classes
- Graph visualization works best with < 500 nodes
- Use `?clear=true` to replace instead of append

### Testing Locally
- Use sample files for quick testing
- Start with small ontologies first
- Check API logs for detailed error messages

---

## 📁 Key Files

```
WALLY-CLEAN/
├── ontology_api.py              # Backend API (port 5002)
├── graph-ui/                    # React frontend
│   └── src/
│       ├── App.jsx              # Main app (ontology only)
│       └── components/Ontology/
│           └── OntologyDemo.jsx # Graph view with import/export
├── sample_data/                 # Sample RDF/OWL files
│   ├── university.owl
│   ├── animals.ttl
│   ├── food.rdf
│   └── README_SAMPLES.md        # Sample file docs
├── requirements.txt             # Python dependencies
└── DAILY_LOG_2026-02-17.md     # Latest changes
```

---

## 🆘 Getting Help

### Check Logs
```bash
# View API logs (if running in background)
tail -f logs/ontology_*.log

# Check React dev server output
# (visible in terminal where npm run dev is running)
```

### Validate RDF Files
```bash
# Test parse with Python
python3 -c "
from rdflib import Graph
g = Graph()
g.parse('yourfile.owl', format='xml')
print(f'Valid! {len(g)} triples')
"
```

### Documentation
- **Samples:** `sample_data/README_SAMPLES.md`
- **Daily Log:** `DAILY_LOG_2026-02-17.md`
- **Architecture:** `ARCHITECTURE_REFACTOR.md`

---

## 💡 Pro Tips

1. **Use curl for batch imports** - Faster than clicking for multiple files
2. **Check sample files first** - Validate your setup works before importing custom files
3. **Export before importing** - Save current state before replacing
4. **Clear flag is optional** - Default appends to existing ontology
5. **Format auto-detected** - From file extension, no need to specify

---

**Last Updated:** February 17, 2026  
**Version:** rdf-import-samples tag  
**Repository:** https://github.com/gpad1234/Startup-One-Wally-Clean
