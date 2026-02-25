# Scalable Ontology Architecture Plan

**Date:** February 18, 2026  
**Goal:** Scale to handle large ontologies (1000+ nodes) with efficient pagination and fish-eye visualization

---

## 🎯 Current Limitations

### Backend
- ✗ In-memory graph_db.py (no persistence)
- ✗ No pagination - returns all nodes at once
- ✗ No query optimization
- ✗ Memory-bound for large ontologies

### Frontend
- ✗ Renders all nodes simultaneously
- ✗ Performance degrades with 500+ nodes
- ✗ No virtualization
- ✗ No progressive loading

---

## 🏗️ Proposed Architecture

### Phase 1: Database Layer (Week 1)

#### Option A: Graph Database (Recommended)
**Neo4j**
- ✅ Native graph storage and queries
- ✅ Built-in pagination (SKIP/LIMIT)
- ✅ Cypher query language
- ✅ Excellent performance for graph traversal
- ✅ Python driver (neo4j-driver)
- ⚠️ Requires separate service

**Setup:**
```python
from neo4j import GraphDatabase

class Neo4jOntologyDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def get_nodes_paginated(self, skip=0, limit=50, filter_type=None):
        with self.driver.session() as session:
            query = """
            MATCH (n:OntologyClass)
            RETURN n
            ORDER BY n.id
            SKIP $skip LIMIT $limit
            """
            return session.run(query, skip=skip, limit=limit)
```

#### Option B: RDF Store
**Apache Jena Fuseki** or **Virtuoso**
- ✅ Native RDF/OWL support
- ✅ SPARQL queries
- ✅ Standards-compliant
- ⚠️ More complex setup

#### Option C: Enhanced graph_db.py
**Keep in-memory but add:**
- Pagination support
- Index structures (dict lookups)
- Lazy loading
- Optional SQLite persistence
- ⚠️ Still memory-limited

**Recommendation:** Start with **Neo4j** for production scalability, keep graph_db.py as fallback.

---

### Phase 2: Backend API Enhancements (Week 2)

#### New Endpoints

```python
# Paginated node retrieval
@app.route('/api/ontology/graph/nodes', methods=['GET'])
def get_nodes_paginated():
    """
    GET /api/ontology/graph/nodes?skip=0&limit=50&type=class
    
    Returns:
    {
      "nodes": [...],
      "total": 1500,
      "skip": 0,
      "limit": 50,
      "has_more": true
    }
    """
    pass

# Get nodes within viewport
@app.route('/api/ontology/graph/viewport', methods=['POST'])
def get_viewport_nodes():
    """
    POST /api/ontology/graph/viewport
    Body: {
      "center_node": "demo:Person",
      "radius": 2,  # hops from center
      "limit": 50
    }
    
    Returns nodes within radius of center (fish-eye center)
    """
    pass

# Get neighbors of specific node
@app.route('/api/ontology/graph/neighbors/<node_id>', methods=['GET'])
def get_node_neighbors(node_id):
    """
    GET /api/ontology/graph/neighbors/demo:Person?depth=1
    
    Returns immediate neighbors for expansion
    """
    pass

# Search with pagination
@app.route('/api/ontology/graph/search', methods=['GET'])
def search_nodes():
    """
    GET /api/ontology/graph/search?q=person&skip=0&limit=20
    
    Search across labels and IDs
    """
    pass
```

#### Backend Service Layer

```python
# src/services/graph_pagination_service.py

class GraphPaginationService:
    def __init__(self, graph_service):
        self.graph_service = graph_service
        self._build_indexes()
    
    def _build_indexes(self):
        """Build lookup indexes for fast access"""
        self.node_index = {}  # id -> node
        self.type_index = {}  # type -> [node_ids]
        self.edge_index = {}  # node_id -> [edges]
    
    def get_page(self, skip=0, limit=50, node_type=None):
        """Get paginated nodes"""
        nodes = self._get_filtered_nodes(node_type)
        total = len(nodes)
        page = nodes[skip:skip+limit]
        
        return {
            'nodes': page,
            'edges': self._get_edges_for_nodes(page),
            'total': total,
            'skip': skip,
            'limit': limit,
            'has_more': skip + limit < total
        }
    
    def get_viewport(self, center_id, radius=2, limit=50):
        """Get nodes within radius hops of center (fish-eye)"""
        visited = set()
        current_level = {center_id}
        
        for _ in range(radius):
            next_level = set()
            for node_id in current_level:
                neighbors = self._get_neighbors(node_id)
                next_level.update(neighbors)
            visited.update(current_level)
            current_level = next_level - visited
            
            if len(visited) >= limit:
                break
        
        return self._format_subgraph(list(visited)[:limit])
```

---

### Phase 3: Frontend - Fish-Eye Visualization (Week 3)

#### React Flow Virtualization

```jsx
// graph-ui/src/components/Ontology/VirtualizedGraphView.jsx

import { useEffect, useState, useCallback } from 'react';
import ReactFlow, { useViewport } from 'reactflow';

const VirtualizedGraphView = () => {
  const [visibleNodes, setVisibleNodes] = useState([]);
  const [centerNode, setCenterNode] = useState(null);
  const viewport = useViewport();
  const [loading, setLoading] = useState(false);
  
  // Load initial viewport
  useEffect(() => {
    loadViewport('owl:Thing', 2);
  }, []);
  
  const loadViewport = async (centerId, radius) => {
    setLoading(true);
    const response = await fetch('/api/ontology/graph/viewport', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ center_node: centerId, radius, limit: 50 })
    });
    const data = await response.json();
    setVisibleNodes(data.nodes);
    setCenterNode(centerId);
    setLoading(false);
  };
  
  // Handle node click - expand neighborhood
  const onNodeClick = useCallback((event, node) => {
    loadViewport(node.id, 2);
  }, []);
  
  // Handle viewport change - load more if needed
  const onMove = useCallback((event, viewport) => {
    // Check if user panned to edge, load adjacent region
    // Implement boundary detection and progressive loading
  }, []);
  
  return (
    <ReactFlow
      nodes={visibleNodes}
      edges={visibleEdges}
      onNodeClick={onNodeClick}
      onMove={onMove}
      fitView
    >
      {loading && <LoadingOverlay />}
      <FishEyeControls 
        onCenterChange={setCenterNode}
        onRadiusChange={setRadius}
      />
    </ReactFlow>
  );
};
```

#### Fish-Eye Zoom Implementation

```jsx
// graph-ui/src/components/Ontology/FishEyeGraph.jsx

const FishEyeGraph = () => {
  const [focusNode, setFocusNode] = useState(null);
  const [zoomLevels, setZoomLevels] = useState({
    // Distance from focus determines size/detail
    0: { scale: 1.5, detail: 'full' },      // Focus node
    1: { scale: 1.2, detail: 'full' },      // Immediate neighbors
    2: { scale: 1.0, detail: 'medium' },    // 2 hops away
    3: { scale: 0.7, detail: 'minimal' },   // 3 hops away
    4: { scale: 0.4, detail: 'minimal' }    // Periphery
  });
  
  const calculateNodeStyle = (node) => {
    const distance = calculateDistance(focusNode, node);
    const level = zoomLevels[Math.min(distance, 4)];
    
    return {
      transform: `scale(${level.scale})`,
      opacity: distance > 3 ? 0.5 : 1,
      detail: level.detail
    };
  };
  
  return (
    <div className="fisheye-container">
      {visibleNodes.map(node => (
        <Node
          key={node.id}
          node={node}
          style={calculateNodeStyle(node)}
          onClick={() => setFocusNode(node.id)}
        />
      ))}
    </div>
  );
};
```

#### Pagination Controls

```jsx
// graph-ui/src/components/Ontology/GraphPagination.jsx

const GraphPagination = ({ currentPage, totalPages, onPageChange }) => {
  return (
    <div className="graph-pagination">
      <button onClick={() => onPageChange(currentPage - 1)}>
        ← Previous 50
      </button>
      
      <span>Showing {currentPage * 50} - {(currentPage + 1) * 50}</span>
      
      <button onClick={() => onPageChange(currentPage + 1)}>
        Next 50 →
      </button>
      
      <JumpToNode onJump={(nodeId) => loadViewport(nodeId)} />
    </div>
  );
};
```

---

### Phase 4: Performance Optimizations (Week 4)

#### Backend Caching
```python
from functools import lru_cache
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300, query_string=True)
@app.route('/api/ontology/graph/nodes')
def get_nodes_paginated():
    # Cached for 5 minutes
    pass
```

#### Frontend Optimizations
```jsx
// React.memo for node components
const MemoizedNode = React.memo(({ node }) => {
  return <NodeComponent node={node} />;
}, (prev, next) => {
  return prev.node.id === next.node.id && 
         prev.node.position === next.node.position;
});

// Virtualization with react-window
import { FixedSizeList } from 'react-window';

// Lazy loading images/icons
const NodeIcon = lazy(() => import('./NodeIcon'));
```

#### Database Indexes
```cypher
// Neo4j indexes
CREATE INDEX class_id FOR (n:OntologyClass) ON (n.id);
CREATE INDEX class_label FOR (n:OntologyClass) ON (n.label);
CREATE INDEX property_domain FOR (p:Property) ON (p.domain);
```

---

## 📊 Implementation Timeline

### Week 1: Database Layer
- [ ] Install and configure Neo4j
- [ ] Create Neo4j adapter service
- [ ] Migrate data from graph_db to Neo4j
- [ ] Test basic CRUD operations
- [ ] Add pagination queries

### Week 2: Backend API
- [ ] Implement paginated endpoints
- [ ] Add viewport/fish-eye endpoint
- [ ] Add neighbor expansion endpoint
- [ ] Add search with pagination
- [ ] Write tests for new endpoints

### Week 3: Frontend Visualization
- [ ] Create VirtualizedGraphView component
- [ ] Implement fish-eye zoom logic
- [ ] Add pagination controls
- [ ] Progressive loading on pan/zoom
- [ ] Performance testing

### Week 4: Optimization & Polish
- [ ] Add backend caching
- [ ] Optimize React rendering
- [ ] Add loading states/skeletons
- [ ] Performance profiling
- [ ] Documentation

---

## 🎨 UI/UX Enhancements

### Fish-Eye Controls
```
┌─────────────────────────────────┐
│  🎯 Focus: demo:Person          │
│  📏 Radius: [1][2][3][4][5]     │
│  🔍 Zoom: [-][+]                │
│  📄 Page: 1 of 30 (50 per page)│
└─────────────────────────────────┘
```

### Progressive Disclosure
- **Level 0 (Focus):** Full details, large node
- **Level 1:** Label + icon, medium size
- **Level 2:** Label only, normal size
- **Level 3:** Icon only, small size
- **Level 4:** Dot only, minimal size

### Viewport Indicators
- Show "Load More" zones at boundaries
- Mini-map showing current view in context
- Node count indicator
- Loading spinner for async operations

---

## 🧪 Testing Strategy

### Performance Targets
- ✅ Support 10,000+ nodes in database
- ✅ Render 50 nodes in < 100ms
- ✅ Viewport load in < 500ms
- ✅ Smooth 60fps interactions
- ✅ Memory usage < 200MB frontend

### Test Cases
1. Load 10,000 node ontology
2. Pan across entire graph
3. Zoom in/out with fish-eye
4. Expand node neighborhoods
5. Search and filter
6. Concurrent users

---

## 📦 Dependencies

### Backend
```txt
neo4j>=5.0.0              # Graph database driver
flask-caching>=2.0.0      # Response caching
```

### Frontend
```json
{
  "react-window": "^1.8.8",           // Virtualization
  "react-intersection-observer": "^9.5.0",  // Lazy loading
  "@react-spring/web": "^9.7.0"       // Smooth animations
}
```

---

## 🔄 Migration Path

### Phase 1: Keep Dual Support
- Keep graph_db.py for small ontologies
- Add Neo4j for large ontologies
- Auto-detect and switch based on size

### Phase 2: Gradual Migration
- Export existing data to Neo4j
- Run both systems in parallel
- Compare performance

### Phase 3: Full Switch
- Deprecate graph_db.py
- Neo4j as primary
- Keep graph_db as lightweight option

---

## 💡 Future Enhancements

1. **Clustering:** Group related nodes visually
2. **Filtering:** Show only specific node types
3. **Layouts:** Multiple layout algorithms (hierarchical, force-directed, circular)
4. **Bookmarks:** Save interesting views
5. **Annotations:** Add notes to nodes
6. **Export Views:** Save current viewport as image
7. **Real-time Updates:** WebSocket for live collaboration

---

**Status:** Planning Phase  
**Next Step:** Week 1 - Database Layer Implementation  
**Owner:** TBD  
**Priority:** High
