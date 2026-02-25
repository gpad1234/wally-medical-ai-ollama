# Scaling to Large Ontologies - Implementation Guide

**Date:** February 18, 2026  
**Goal:** Handle 1000+ node ontologies with efficient visualization  
**Approach:** Fish-eye pagination with progressive loading

---

## 📋 Quick Summary

### Problem
Current system loads all nodes at once:
- Performance degrades with 500+ nodes
- Memory intensive
- Poor user experience with large ontologies

### Solution
**Fish-Eye Graph with Pagination:**
- Show 50 nodes at a time (focus + context)
- Progressive loading as user explores
- Center node + N-hop neighbors
- Smooth transitions between views

---

## 🎯 Implementation Strategy

### 1. **Backend: Pagination Service** ✅ POC Complete
```python
# src/services/graph_pagination_service.py

service = GraphPaginationService(graph_db)

# Get page of nodes
page = service.get_page(skip=0, limit=50)

# Get fish-eye viewport (center + neighbors)
viewport = service.get_viewport(
    center_id='demo:Person',
    radius=2,  # 2 hops
    limit=50
)

# Expand node neighbors
neighbors = service.get_neighbors('demo:Person')
```

### 2. **Backend: API Endpoints** (TODO - Week 2)

```python
# New endpoints to add to ontology_api.py

GET  /api/ontology/graph/nodes?skip=0&limit=50&type=class
POST /api/ontology/graph/viewport
     Body: { center_node, radius, limit }
GET  /api/ontology/graph/neighbors/<node_id>?depth=1
GET  /api/ontology/graph/search?q=query&skip=0&limit=20
```

### 3. **Frontend: Virtualized Graph** (TODO - Week 3)

```jsx
// VirtualizedGraphView.jsx

const VirtualizedGraphView = () => {
  const [visibleNodes, setVisibleNodes] = useState([]);
  const [centerNode, setCenterNode] = useState('owl:Thing');
  const [radius, setRadius] = useState(2);
  
  // Load initial viewport
  useEffect(() => {
    loadViewport(centerNode, radius);
  }, [centerNode, radius]);
  
  const loadViewport = async (center, r) => {
    const response = await fetch('/api/ontology/graph/viewport', {
      method: 'POST',
      body: JSON.stringify({ 
        center_node: center, 
        radius: r, 
        limit: 50 
      })
    });
    const data = await response.json();
    setVisibleNodes(data.nodes);
  };
  
  // Click node to recenter
  const onNodeClick = (node) => {
    setCenterNode(node.id);
  };
  
  return (
    <ReactFlow
      nodes={visibleNodes}
      onNodeClick={onNodeClick}
    />
  );
};
```

### 4. **Fish-Eye Visualization** (TODO - Week 3)

**Progressive Detail Levels:**
```
Distance 0 (Focus):     Large node, full details
Distance 1:             Medium node, label + icon
Distance 2:             Normal node, label only
Distance 3+:            Small node, minimal
```

**Visual Implementation:**
```jsx
const getNodeStyle = (node) => {
  const distance = node.distance_from_center || 0;
  const scales = [1.5, 1.2, 1.0, 0.7, 0.4];
  return {
    transform: `scale(${scales[Math.min(distance, 4)]})`,
    opacity: distance > 3 ? 0.5 : 1
  };
};
```

---

## 🛠️ Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [x] Create pagination service POC
- [ ] Add API endpoints to ontology_api.py
- [ ] Test with existing graph_db
- [ ] Unit tests for pagination logic

### Phase 2: Frontend Integration (Week 3)
- [ ] Create VirtualizedGraphView component
- [ ] Implement fish-eye zoom levels
- [ ] Add navigation controls
- [ ] Progressive loading on pan/zoom

### Phase 3: Database (Week 4)
- [ ] Evaluate Neo4j vs graph_db
- [ ] Add database indexes
- [ ] Implement caching strategy
- [ ] Performance benchmarks

### Phase 4: Polish (Week 5)
- [ ] Loading states and skeletons
- [ ] Error handling
- [ ] Documentation
- [ ] User testing

---

## 🚀 Quick Start (Using POC)

### Test the Pagination Service

```bash
# Run the proof-of-concept
python3 src/services/graph_pagination_service.py
```

**Output:**
```
=== Graph Stats ===
{'total_nodes': 4, 'total_edges': 3}

=== Page 1 (limit=2) ===
Nodes: ['demo:Person', 'demo:Professor']
Total: 4, Has More: True

=== Viewport around demo:Person (radius=2) ===
Center: demo:Person
Nodes: ['demo:Person', 'demo:Student', 'demo:Professor']
```

### Integrate with Existing System

```python
# In ontology_api.py

from src.services.graph_pagination_service import GraphPaginationService

# Initialize
pagination_service = GraphPaginationService(ontology_service.graph)

@app.route('/api/ontology/graph/viewport', methods=['POST'])
def get_viewport():
    data = request.get_json()
    viewport = pagination_service.get_viewport(
        center_id=data['center_node'],
        radius=data.get('radius', 2),
        limit=data.get('limit', 50)
    )
    return jsonify(success_response(viewport))
```

---

## 📊 Performance Targets

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Max visible nodes | All (~500) | 50 | ✅ POC |
| Viewport load time | N/A | < 500ms | 🔜 |
| Memory usage | ~200MB | < 100MB | 🔜 |
| FPS (interaction) | 30-60 | 60 | 🔜 |
| Max DB nodes | 1000 | 10,000+ | 🔄 |

---

## 🎨 UI Mockup

```
┌──────────────────────────────────────────────────────────┐
│  Ontology Knowledge Graph                    [Import][Export] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [🎯] Focus: demo:Person     Radius: [1][2][3][4][5]   │
│  [🔍] Search: _________      Page: 1/20 (showing 50)    │
│                                                          │
│  ┌────────────────────────────────────────────────┐   │
│  │                                                  │   │
│  │     owl:Thing          ← Context (small)       │   │
│  │         │                                        │   │
│  │    ┌────▼────┐                                  │   │
│  │    │ Person  │         ← Focus (large)         │   │
│  │    └─┬────┬──┘                                  │   │
│  │      │    │                                      │   │
│  │  ┌───▼┐ ┌▼────┐        ← Neighbors (medium)   │   │
│  │  │Stud│ │Prof │                                │   │
│  │  └────┘ └─────┘                                │   │
│  │                                                  │   │
│  │  [Click node to recenter] [Load More Nodes]   │   │
│  └────────────────────────────────────────────────┘   │
│                                                          │
│  Showing: 8 nodes, 6 edges | Total: 1,234 nodes        │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Backend Settings
```python
# ontology_api.py

PAGINATION_CONFIG = {
    'default_limit': 50,
    'max_limit': 200,
    'default_radius': 2,
    'max_radius': 5,
    'cache_timeout': 300  # 5 minutes
}
```

### Frontend Settings
```javascript
// graphConfig.js

export const GRAPH_CONFIG = {
  maxVisibleNodes: 50,
  fisheyeRadius: 2,
  zoomLevels: {
    0: { scale: 1.5, detail: 'full' },
    1: { scale: 1.2, detail: 'full' },
    2: { scale: 1.0, detail: 'medium' },
    3: { scale: 0.7, detail: 'minimal' }
  },
  loadMoreThreshold: 0.8  // Load when 80% of nodes visible
};
```

---

## 📚 Resources

### Documentation
- [SCALABLE_ARCHITECTURE_PLAN.md](SCALABLE_ARCHITECTURE_PLAN.md) - Detailed architecture
- [QUICKTIPS.md](QUICKTIPS.md) - Quick reference
- [DAILY_LOG_2026-02-17.md](DAILY_LOG_2026-02-17.md) - Recent changes

### Code Files
- `src/services/graph_pagination_service.py` - Pagination POC
- `src/services/ontology_service.py` - Core ontology logic
- `graph-ui/src/components/Ontology/GraphView.jsx` - Current graph view

### External References
- [React Flow Docs](https://reactflow.dev/)
- [Fish-Eye Visualization](https://en.wikipedia.org/wiki/Fisheye_lens)
- [Neo4j Graph Database](https://neo4j.com/)

---

## 🎯 Next Actions

### This Week
1. ✅ Create [SCALABLE_ARCHITECTURE_PLAN.md](SCALABLE_ARCHITECTURE_PLAN.md)
2. ✅ Build pagination service POC
3. [ ] Add viewport API endpoint
4. [ ] Test with 1000-node ontology

### Next Week
1. [ ] Build VirtualizedGraphView component
2. [ ] Implement fish-eye zoom
3. [ ] Add loading states
4. [ ] User testing

---

## 💬 Discussion Points

### Database Choice
- **Keep graph_db.py:** Simple, no external dependencies
- **Add Neo4j:** Production-ready, scales to millions
- **Hybrid:** Auto-switch based on ontology size

**Recommendation:** Start with enhanced graph_db.py, plan Neo4j migration

### Fish-Eye vs Traditional Pagination
- **Fish-Eye:** Better for graph exploration, intuitive
- **Traditional:** Simpler to implement, familiar pattern

**Recommendation:** Fish-eye for primary interaction, traditional as fallback

---

**Status:** Phase 1 - POC Complete  
**Next Milestone:** API Endpoints (Week 2)  
**Last Updated:** February 18, 2026
