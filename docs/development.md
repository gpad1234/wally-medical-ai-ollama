---
layout: default
title: Development
---

# 💻 Development Guide

Complete guide for developers working on WALLY. Covers workflow, architecture, coding standards, and contribution process.

---

## Development Environment Setup

### System Requirements

- **OS:** macOS, Linux, or Windows (WSL recommended)
- **Python:** 3.12+
- **Node.js:** 18+
- **Memory:** 4GB+ RAM recommended
- **IDE:** VS Code (recommended) with extensions:
  - Python
  - ESLint
  - Prettier
  - ReactFlow Snippets

### Initial Setup

```bash
# 1. Fork on GitHub, then clone your fork

git clone https://github.com/YOUR_USERNAME/Startup-One-Wally-Clean.git
cd Startup-One-Wally-Clean

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


# 4. Install frontend dependencies
cd graph-ui && npm install && cd ..

# 5. Start development servers
# Terminal 1: python3 ontology_api.py
# Terminal 2: cd graph-ui && npm run dev
# Terminal 3 (LLM/NLP): cd ubuntu-deploy && node llm-service.js
```
---

## Project Architecture

### High-Level Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  React Frontend │◄────►│   Flask API      │◄────►│   GraphDB       │
│  (Port 5173)    │ HTTP │  (Port 5002)     │      │  (In-Memory)    │
│                 │      │                  │      │                 │
│  Fish-Eye View  │      │  Pagination      │      │  C Libraries    │
│  ReactFlow      │      │  BFS Algorithm   │      │  libsimpledb.so │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

### Backend Architecture

**ontology_api.py (741 lines)**
- Flask REST API with CORS
- 3 pagination endpoints
- Demo data initialization
- Error handling and logging

**src/services/graph_pagination_service.py (380 lines)**
- BFS-based fish-eye viewport algorithm
- Bidirectional graph traversal
- Distance tracking and level grouping
- Performance optimized

**graph_db.py**
- GraphDB wrapper
- RDF/OWL operations
- C library integration

### Frontend Architecture

**graph-ui/src/App.jsx**
- Main application component
- Tab navigation (Fish-Eye, Pagination Tests, About)
- Global state management

**components/Ontology/VirtualizedGraphView.jsx (500+ lines)**
- Fish-eye visualization
- ReactFlow integration
- Distance-based node styling
- Click-to-recenter logic
- MiniMap configuration

**components/Ontology/PaginationTest.jsx (458 lines)**
- API testing interface
- Debug visualization
- Network request inspection

---

## Development Workflow

### Daily Workflow

```bash
# 1. Start development
git pull origin main
git checkout -b feature/my-feature
source .venv/bin/activate

# 2. Start servers
python3 ontology_api.py &            # Backend
cd graph-ui && npm run dev &         # Frontend

# 3. Make changes
# Edit files in src/ or graph-ui/src/

# 4. Test changes
# Open http://localhost:5173
# Check browser console (F12)
# Verify API responses

# 5. Commit and push
git add -A
git commit -m "feat: Add awesome feature"
git push origin feature/my-feature

# 6. Create Pull Request
# Visit GitHub and open PR to main branch
```

### Git Commit Convention

Follow conventional commits:

```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Code style changes (formatting)
refactor: Code refactoring
perf: Performance improvements
test: Add or update tests
chore: Build/tooling changes
```

Examples:
```
feat: Add search bar to fish-eye view
fix: Correct bidirectional edge traversal
docs: Update API endpoint documentation
perf: Optimize BFS algorithm for 1000+ nodes
```

---

## Code Organization

### Backend Structure

```
src/
├── core/                    # C libraries
│   ├── Makefile
│   ├── src/
│   │   ├── simple_db.c      # Core database (430 lines)
│   │   ├── linked_list.c    # Singly linked (241 lines)
│   │   ├── doubly_linked_list.c
│   │   └── circular_linked_list.c
│   └── include/
│       ├── simple_db.h
│       └── linked_list.h
│
├── services/
│   ├── graph_pagination_service.py  # Fish-eye algorithm
│   ├── ontology_service.py          # RDF operations
│   └── __init__.py
│
└── utils/                   # Utilities (future)
    └── logging.py

# Root level
ontology_api.py              # Main API server
graph_db.py                  # DB wrapper
requirements.txt             # Python deps
```

### Frontend Structure

```
graph-ui/
├── src/
│   ├── App.jsx              # Main app
│   ├── main.jsx             # Entry point
│   ├── components/
│   │   └── Ontology/
│   │       ├── VirtualizedGraphView.jsx  # Fish-eye
│   │       └── PaginationTest.jsx        # Testing
│   └── assets/              # Static files
│
├── public/                  # Public assets
├── vite.config.js           # Build config
├── package.json             # npm deps
└── index.html               # HTML template
```

---

## Coding Standards

### Python Standards

Follow PEP 8 with these additions:

```python
# Type hints
def get_viewport(center: str, radius: int, limit: int) -> Dict[str, Any]:
    """
    Get fish-eye viewport around center node.
    
    Args:
        center: URI of center node
        radius: Number of hops from center
        limit: Max nodes to return
        
    Returns:
        Dict with nodes, edges, levels
    """
    pass

# Logging
import logging
logger = logging.getLogger(__name__)

logger.info(f"Loading viewport: center={center}, radius={radius}")
logger.error(f"Failed to load viewport: {error}")

# Error handling
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return {"success": False, "error": str(e)}
```

### JavaScript/React Standards

Follow Airbnb style guide with these additions:

```javascript
// Use functional components with hooks
const VirtualizedGraphView = ({ initialCenter = 'owl:Thing' }) => {
  const [nodes, setNodes] = useState([]);
  
  useEffect(() => {
    // Load data
  }, [initialCenter]);
  
  return <div>...</div>;
};

// Destructure props
const CustomNode = ({ data, id }) => {
  const { label, distance } = data;
  return <div>{label}</div>;
};

// useMemo for expensive computations
const nodeTypes = useMemo(() => ({
  custom: CustomNode
}), []);

// useCallback for event handlers
const onNodeClick = useCallback((event, node) => {
  console.log('Node clicked:', node.id);
}, []);

// Console logging with emojis for readability
console.log('🔍 Loading viewport:', { center, radius });
console.log('📦 API Response:', result);
console.log('✅ Success:', data);
console.error('❌ Error:', error);
```

### CSS/Styling Standards

```javascript
// Inline styles with consistent naming
const styles = {
  container: {
    width: '100%',
    height: '100%',
    display: 'flex'
  },
  header: {
    padding: '20px',
    background: 'white'
  }
};

// Color palette
const colors = {
  primary: '#3b82f6',
  secondary: '#10b981',
  danger: '#ef4444',
  text: '#1e293b',
  border: '#e2e8f0'
};
```

---

## Testing Strategy

### Current Testing Approach

**Manual Testing:**
1. Visual inspection in browser
2. Console log verification
3. Network tab monitoring
4. PaginationTest component

**API Testing:**
```bash
# Test each endpoint with curl
curl "http://localhost:5002/api/ontology/graph/nodes?skip=0&limit=10"

curl -X POST "http://localhost:5002/api/ontology/graph/viewport" \
  -H "Content-Type: application/json" \
  -d '{"center_node":"owl:Thing","radius":2,"limit":50}'
```

### Future Testing (Planned)

**Backend Unit Tests:**
```python
# tests/test_pagination_service.py
def test_bfs_viewport():
    service = GraphPaginationService(graph)
    result = service.get_viewport("owl:Thing", radius=2, limit=50)
    
    assert len(result['nodes']) <= 50
    assert result['center'] == "owl:Thing"
    assert 0 in result['levels']
```

**Frontend Component Tests:**
```javascript
// __tests__/VirtualizedGraphView.test.jsx
test('renders fish-eye graph', () => {
  render(<VirtualizedGraphView />);
  expect(screen.getByText(/Fish-Eye Graph View/i)).toBeInTheDocument();
});

test('recenters on node click', () => {
  render(<VirtualizedGraphView />);
  fireEvent.click(screen.getByText('Person'));
  // Assert viewport updated
});
```

---

## Debugging Tips

### Backend Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for breakpoints
import pdb; pdb.set_trace()

# Check API responses
logger.debug(f"Viewport result: {result}")
logger.debug(f"Node count: {len(nodes)}")
```

### Frontend Debugging

```javascript
// Browser console logs
console.log('🔍 Current state:', { nodes, edges, centerNode });

// React DevTools
// Install browser extension to inspect component state

// Network tab
// Check API request/response in browser DevTools

// React Flow debugging
console.log('Node positions:', nodes.map(n => ({
  id: n.id,
  position: n.position
})));
```

### Common Issues

**Backend not responding:**
```bash
# Check if port is in use
lsof -ti :5002

# Check if C library loaded
python3 -c "import ctypes; print(ctypes.cdll.LoadLibrary('./src/core/libsimpledb.so'))"
```

**Frontend not fetching:**
```javascript
// Check Vite proxy in vite.config.js
// Verify API URL is relative: '/api/...'
// Check CORS in browser console
```

---

## Performance Optimization

### Backend Performance

```python
# Cache frequently accessed views
from functools import lru_cache

@lru_cache(maxsize=128)
def get_viewport_cached(center: str, radius: int):
    return get_viewport(center, radius, 50)

# Profile code
import cProfile
cProfile.run('get_viewport("owl:Thing", 2, 50)')

# Monitor memory
import tracemalloc
tracemalloc.start()
# ... code ...
print(tracemalloc.get_traced_memory())
```

### Frontend Performance

```javascript
// Memoize expensive computations
const nodeTypes = useMemo(() => ({
  custom: CustomNode
}), []);

// Debounce frequent updates
import { debounce } from 'lodash';
const debouncedUpdate = debounce(loadViewport, 300);

// Use React.memo for pure components
const CustomNode = React.memo(({ data }) => {
  return <div>{data.label}</div>;
});

// Lazy load components
const PaginationTest = lazy(() => import('./PaginationTest'));
```

---

## Adding New Features

### Example: Add Search Feature

**1. Backend API:**
```python
@app.route('/api/ontology/graph/search', methods=['GET'])
def search_nodes():
    query = request.args.get('q', '')
    results = ontology_service.search_nodes(query)
    return jsonify({
        "success": True,
        "results": results,
        "count": len(results)
    })
```

**2. Service Layer:**
```python
# src/services/ontology_service.py
def search_nodes(self, query: str) -> List[Dict]:
    """Search nodes by label or URI."""
    matches = []
    for node_uri in self.graph.subjects():
        label = self.get_node_label(node_uri)
        if query.lower() in label.lower():
            matches.append({
                "id": str(node_uri),
                "label": label
            })
    return matches
```

**3. Frontend Component:**
```javascript
const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  
  const handleSearch = async () => {
    const response = await fetch(`/api/ontology/graph/search?q=${query}`);
    const data = await response.json();
    setResults(data.results);
  };
  
  return (
    <input 
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyUp={(e) => e.key === 'Enter' && handleSearch()}
    />
  );
};
```

**4. Test & Document:**
- Test manually
- Add to features.md
- Update API docs
- Commit with descriptive message

---

## Release Process

### Version Numbering

Follow Semantic Versioning (semver):

- **Major (1.0.0):** Breaking changes
- **Minor (1.1.0):** New features (backwards compatible)
- **Patch (1.1.1):** Bug fixes

### Release Checklist

```bash
# 1. Update version
# Edit package.json and any version files

# 2. Update changelog
# Add new version section to CHANGELOG.md

# 3. Run tests
pytest tests/
cd graph-ui && npm test

# 4. Build production
cd graph-ui && npm run build

# 5. Tag release
git tag -a v1.1.0 -m "Release v1.1.0: Interactive MiniMap"
git push origin v1.1.0

# 6. Create GitHub release
# Visit GitHub and create release from tag

# 7. Deploy to production
./scripts/deploy_to_droplet.sh
```

---

## Contributing Guidelines

### Pull Request Process

1. **Create feature branch** from `main`
2. **Make focused changes** - one feature per PR
3. **Write clear commit messages**
4. **Test thoroughly** - manual testing required
5. **Update documentation** - features.md, README.md
6. **Submit PR** with description
7. **Respond to review feedback**
8. **Merge after approval**

### Code Review Checklist

**Reviewer checks:**
- ✅ Code follows style guidelines
- ✅ No unnecessary console.logs in production
- ✅ Error handling present
- ✅ Documentation updated
- ✅ No security vulnerabilities
- ✅ Performance considerations addressed

---

## Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [ReactFlow Documentation](https://reactflow.dev/)
- [rdflib Documentation](https://rdflib.readthedocs.io/)

### Tools
- [Python Type Checking (mypy)](http://mypy-lang.org/)
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)
- [React DevTools](https://react.dev/learn/react-developer-tools)

### Project Documentation
- [ACTION_PLAN.md](../ACTION_PLAN.md) - 4-week roadmap
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [DIGITALOCEAN_DEPLOY.md](../DIGITALOCEAN_DEPLOY.md) - Deployment

---

[← Back to Home](./) | [Deployment →](deployment)
