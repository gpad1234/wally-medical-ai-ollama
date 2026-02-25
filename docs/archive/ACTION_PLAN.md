# Action Plan - Scalable Ontology Editor

**Start Date:** February 18, 2026  
**Database Choice:** Enhanced graph_db.py → Neo4j (if needed)  
**Timeline:** 4 weeks to MVP  

---

## 🎯 Week 1: Backend Pagination (Feb 18-24)

### Day 1-2: Integrate Pagination Service ✅ POC Ready
- [x] Pagination service POC created
- [ ] Add pagination service to ontology_api.py
- [ ] Create API endpoint: `/api/ontology/graph/nodes` (paginated)
- [ ] Test with existing test data

**Files to modify:**
- `ontology_api.py` - Add endpoints
- `src/services/ontology_service.py` - Integrate pagination service

**Code:**
```python
# ontology_api.py

from src.services.graph_pagination_service import GraphPaginationService

# Initialize pagination service
pagination_service = None

def get_pagination_service():
    global pagination_service
    if pagination_service is None:
        pagination_service = GraphPaginationService(
            get_ontology_service().graph
        )
    return pagination_service

@app.route('/api/ontology/graph/nodes', methods=['GET'])
def get_paginated_nodes():
    """Get paginated nodes"""
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 50))
    node_type = request.args.get('type')
    
    result = get_pagination_service().get_page(
        skip=skip, 
        limit=limit, 
        node_type=node_type
    )
    return jsonify(success_response(result))
```

### Day 3-4: Fish-Eye Viewport Endpoint
- [ ] Create endpoint: `/api/ontology/graph/viewport` (POST)
- [ ] Create endpoint: `/api/ontology/graph/neighbors/<id>` (GET)
- [ ] Write unit tests
- [ ] Test with 1000+ node ontology

**Code:**
```python
@app.route('/api/ontology/graph/viewport', methods=['POST'])
def get_viewport():
    """Get fish-eye viewport"""
    data = request.get_json()
    result = get_pagination_service().get_viewport(
        center_id=data['center_node'],
        radius=data.get('radius', 2),
        limit=data.get('limit', 50)
    )
    return jsonify(success_response(result))

@app.route('/api/ontology/graph/neighbors/<node_id>', methods=['GET'])
def get_neighbors(node_id):
    """Get node neighbors"""
    result = get_pagination_service().get_neighbors(node_id)
    return jsonify(success_response(result))
```

### Day 5: Search & Stats
- [ ] Create endpoint: `/api/ontology/graph/search` (GET)
- [ ] Enhance stats endpoint with pagination info
- [ ] Documentation

**Deliverable:** Working paginated backend API ✅

---

## 🎯 Week 2: Frontend Foundation (Feb 25 - Mar 3)

### Day 6-8: Virtualized Graph Component
- [ ] Create `VirtualizedGraphView.jsx`
- [ ] Implement viewport loading on mount
- [ ] Add loading states & error handling
- [ ] Basic node/edge rendering with React Flow

**Files to create:**
- `graph-ui/src/components/Ontology/VirtualizedGraphView.jsx`
- `graph-ui/src/hooks/useViewport.js`
- `graph-ui/src/services/viewportApi.js`

**Code:**
```jsx
// VirtualizedGraphView.jsx
import { useState, useEffect } from 'react';
import ReactFlow from 'reactflow';

const VirtualizedGraphView = () => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [centerNode, setCenterNode] = useState('owl:Thing');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadViewport(centerNode, 2);
  }, [centerNode]);

  const loadViewport = async (center, radius) => {
    setLoading(true);
    try {
      const response = await fetch(
        'http://127.0.0.1:5002/api/ontology/graph/viewport',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            center_node: center,
            radius: radius,
            limit: 50
          })
        }
      );
      const data = await response.json();
      setNodes(formatNodes(data.data.nodes));
      setEdges(formatEdges(data.data.edges));
    } finally {
      setLoading(false);
    }
  };

  const onNodeClick = (event, node) => {
    setCenterNode(node.id);
  };

  return (
    <div style={{ height: '600px' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodeClick={onNodeClick}
        fitView
      />
      {loading && <LoadingOverlay />}
    </div>
  );
};
```

### Day 9-10: Fish-Eye Controls & Navigation
- [ ] Add fish-eye radius control (1-5 hops)
- [ ] Add center node selector/search
- [ ] Add "Recenter on Click" functionality
- [ ] Node count indicator

**Deliverable:** Working paginated graph view ✅

---

## 🎯 Week 3: Fish-Eye Visualization (Mar 4-10)

### Day 11-13: Progressive Detail Levels
- [ ] Implement distance-based node sizing
- [ ] Progressive detail (full → minimal)
- [ ] Smooth transitions with react-spring
- [ ] Node style variations by distance

**Code:**
```jsx
// Fish-eye styling
const getNodeStyle = (node) => {
  const distance = node.data.distance_from_center || 0;
  const scales = [1.5, 1.2, 1.0, 0.7, 0.4];
  const scale = scales[Math.min(distance, 4)];
  
  return {
    transform: `scale(${scale})`,
    opacity: distance > 3 ? 0.5 : 1,
    fontSize: distance === 0 ? '14px' : distance === 1 ? '12px' : '10px'
  };
};

const MemoizedNode = React.memo(({ data }) => {
  const distance = data.distance_from_center || 0;
  const showLabel = distance <= 2;
  const showIcon = distance <= 3;
  
  return (
    <div className="custom-node" style={getNodeStyle(data)}>
      {showIcon && <Icon type={data.type} />}
      {showLabel && <span>{data.label}</span>}
    </div>
  );
});
```

### Day 14-15: Polish & Optimization
- [ ] React.memo for node components
- [ ] Debounce viewport loads
- [ ] Add mini-map showing context
- [ ] Loading skeletons

**Deliverable:** Full fish-eye visualization ✅

---

## 🎯 Week 4: Testing & Optimization (Mar 11-17)

### Day 16-17: Performance Testing
- [ ] Create 1,000 node test ontology
- [ ] Create 5,000 node test ontology
- [ ] Measure load times
- [ ] Measure FPS during interaction
- [ ] Memory profiling

**Test Script:**
```python
# generate_large_ontology.py
# Create test ontology with N nodes

def generate_test_ontology(num_classes=1000):
    ontology = []
    for i in range(num_classes):
        ontology.append({
            'id': f'test:Class{i}',
            'label': f'Test Class {i}',
            'parent': f'test:Class{i-1}' if i > 0 else 'owl:Thing'
        })
    return ontology
```

### Day 18-19: Caching & Optimization
- [ ] Add Flask-Caching to backend
- [ ] Cache viewport queries (5 min TTL)
- [ ] Frontend request deduplication
- [ ] Lazy load node details

**Code:**
```python
# Backend caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/ontology/graph/viewport', methods=['POST'])
@cache.cached(timeout=300, query_string=True)
def get_viewport():
    # Cached for 5 minutes
    pass
```

### Day 20: Documentation & Cleanup
- [ ] Update QUICKTIPS.md with new features
- [ ] Create VIDEO_DEMO.md with screenshots
- [ ] Update README.md
- [ ] Code cleanup & comments

**Deliverable:** Production-ready scalable system ✅

---

## 📊 Success Metrics

### Week 1 (Backend)
- ✅ Pagination endpoint returns < 500ms
- ✅ Viewport endpoint returns < 500ms
- ✅ Can handle 1,000 node ontology

### Week 2 (Frontend)
- ✅ Initial load < 1 second
- ✅ Node click recenters < 500ms
- ✅ Smooth 60fps interactions

### Week 3 (Fish-Eye)
- ✅ Visual hierarchy clear (focus vs context)
- ✅ Transitions smooth with react-spring
- ✅ User can navigate 1000+ node ontology

### Week 4 (Polish)
- ✅ Load 5,000 node ontology successfully
- ✅ Memory usage < 200MB frontend
- ✅ All features documented

---

## 🚦 Daily Standup Checklist

**Every Day:**
- [ ] What did I complete yesterday?
- [ ] What will I complete today?
- [ ] Any blockers?
- [ ] Commit & push to GitHub

**End of Week:**
- [ ] Tag release (week-1, week-2, etc.)
- [ ] Update progress in SCALING_GUIDE.md
- [ ] Demo to stakeholders

---

## 🔄 Immediate Next Steps (This Week)

### Today (Day 1)
1. [ ] Open `ontology_api.py`
2. [ ] Import `GraphPaginationService`
3. [ ] Add `/api/ontology/graph/nodes` endpoint
4. [ ] Test with curl

```bash
# Test command
curl "http://127.0.0.1:5002/api/ontology/graph/nodes?skip=0&limit=10"
```

### Tomorrow (Day 2)
1. [ ] Add `/api/ontology/graph/viewport` endpoint
2. [ ] Test with curl
3. [ ] Unit tests

```bash
# Test command
curl -X POST http://127.0.0.1:5002/api/ontology/graph/viewport \
  -H "Content-Type: application/json" \
  -d '{"center_node":"demo:Person","radius":2,"limit":50}'
```

### Day 3
1. [ ] Add `/api/ontology/graph/neighbors/<id>` endpoint
2. [ ] Add `/api/ontology/graph/search` endpoint
3. [ ] Integration tests

---

## 🎯 Quick Wins (Do These First)

### 1. Backend Endpoints (2-3 hours)
Copy-paste ready code:
- `/api/ontology/graph/nodes` - Already designed ✅
- `/api/ontology/graph/viewport` - Already designed ✅
- Pagination service - Already coded ✅

### 2. Frontend Basic View (3-4 hours)
- Copy GraphView.jsx → VirtualizedGraphView.jsx
- Add viewport loading hook
- Test with demo data

### 3. Fish-Eye Styling (2 hours)
- Distance-based scaling CSS
- Show/hide labels by distance
- Simple, immediate visual impact

---

## 📦 Dependencies to Install

### Backend (Week 1)
```bash
pip3 install flask-caching
```

### Frontend (Week 2)
```bash
cd graph-ui
npm install @react-spring/web
npm install react-intersection-observer
```

---

## 🎓 Learning Resources

**React Flow:**
- https://reactflow.dev/examples/nodes/custom-node
- https://reactflow.dev/examples/interaction/node-click

**Fish-Eye Visualization:**
- https://en.wikipedia.org/wiki/Fisheye_lens
- Focus + Context visualization patterns

**Performance:**
- React.memo documentation
- Debouncing in React

---

## 📝 Notes

- Keep graph_db.py as-is (no major changes needed)
- Pagination service handles all heavy lifting
- Focus on UX - smooth, intuitive navigation
- Test with real RDF/OWL samples

---

## ✅ Ready to Start?

**First command:**
```bash
cd /Users/gp/claude-code/startup-one/WALLY-CLEAN
code ontology_api.py
# Add pagination endpoints (Day 1)
```

**Status:** ✅ POC proven, ready to implement  
**Next:** Day 1 - Backend endpoints  
**Timeline:** 4 weeks to MVP  
**Risk:** Low (building on proven POC)
