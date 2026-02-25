# Service Layer Design

**Date**: February 10, 2026  
**Status**: Design Document  
**Author**: Architecture Team

---

## 1. Overview

The service layer provides a clean separation between the Flask API routes and the business logic, ensuring:
- **Single Responsibility**: Each service handles one domain concern
- **Testability**: Business logic can be tested without HTTP layer
- **Reusability**: Services can be used by CLI, API, or other interfaces
- **Maintainability**: Changes to business logic don't affect route definitions

---

## 2. Current Architecture Problems

### 2.1 Issues with Current Design

```
graph_web_ui.py (981 lines)
├── Flask routes (20+ endpoints)
├── Business logic mixed in routes
├── Direct GraphDB instantiation
├── OpenAI/Claude API calls in routes
└── No separation of concerns
```

**Problems:**
- ❌ Routes have too much responsibility
- ❌ Business logic not reusable
- ❌ Hard to test without Flask
- ❌ No clear domain boundaries
- ❌ Difficult to maintain

---

## 3. Proposed Service Layer Architecture

### 3.1 Layered Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Flask API    │  │ CLI Tools    │  │ Future: gRPC │      │
│  │ Routes       │  │              │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼──────────────┐
│                    SERVICE LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Graph        │  │ Query        │  │ NLP          │      │
│  │ Service      │  │ Service      │  │ Service      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼──────────────┐
│                    DOMAIN LAYER                               │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ GraphDB      │  │ Models       │                         │
│  │ (graph_db.py)│  │ (DTOs)       │                         │
│  └──────┬───────┘  └──────────────┘                         │
└─────────┼────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────┐
│                    ADAPTER LAYER                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ SimpleDB     │  │ External     │                         │
│  │ Adapter      │  │ APIs         │                         │
│  └──────────────┘  └──────────────┘                         │
└───────────────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────┐
│                    CORE LAYER (C)                             │
│  libsimpledb.dylib, liblinkedlist.dylib, etc.               │
└───────────────────────────────────────────────────────────────┘
```

### 3.2 Service Layer Components

#### **GraphService**
- Manages graph operations (CRUD for nodes/edges)
- Handles graph algorithms (BFS, DFS, shortest path)
- Manages graph state and validation
- Encapsulates GraphDB interactions

#### **QueryService**
- Processes queries (search, filter, traversal)
- Coordinates between graph service and algorithms
- Handles complex multi-step queries
- Returns formatted results

#### **NLPService**
- Natural language processing
- Intent detection and entity extraction
- Maps NL queries to graph operations
- Handles OpenAI/Claude API interactions

#### **ExportService**
- Data serialization (JSON, adjacency list, etc.)
- Import/export operations
- Format conversion
- Data validation

---

## 4. Service Implementation Patterns

### 4.1 Service Base Pattern

```python
class BaseService:
    """Base class for all services"""
    
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def _log_operation(self, operation: str, **kwargs):
        """Log service operations"""
        self._logger.info(f"{operation}: {kwargs}")
    
    def _handle_error(self, error: Exception, context: str):
        """Centralized error handling"""
        self._logger.error(f"Error in {context}: {str(error)}")
        raise ServiceError(f"{context} failed") from error
```

### 4.2 Service Interface Pattern

Each service should:
1. Have a clear, focused responsibility
2. Return domain objects (not Flask responses)
3. Raise domain exceptions (not HTTP errors)
4. Be independently testable
5. Have no knowledge of HTTP/Flask

---

## 5. Detailed Service Designs

### 5.1 GraphService

**Responsibility**: Core graph operations

```python
class GraphService:
    """
    Service for graph database operations
    
    Handles:
    - Node and edge CRUD
    - Graph validation
    - Algorithm execution
    - State management
    """
    
    def __init__(self, graph_db: GraphDB = None):
        self.graph = graph_db or GraphDB()
    
    # Node Operations
    def add_node(self, node_id: str, properties: dict = None) -> NodeResult
    def get_node(self, node_id: str) -> Optional[NodeResult]
    def update_node(self, node_id: str, properties: dict) -> NodeResult
    def delete_node(self, node_id: str) -> bool
    def list_nodes(self) -> List[NodeResult]
    
    # Edge Operations
    def add_edge(self, from_node: str, to_node: str, 
                 weight: float = 1.0, label: str = None) -> EdgeResult
    def get_edges(self, node_id: str = None) -> List[EdgeResult]
    def delete_edge(self, from_node: str, to_node: str) -> bool
    
    # Graph Algorithms
    def bfs(self, start: str) -> TraversalResult
    def dfs(self, start: str) -> TraversalResult
    def shortest_path(self, start: str, end: str) -> PathResult
    def all_paths(self, start: str, end: str) -> List[PathResult]
    
    # Graph Queries
    def get_stats(self) -> GraphStats
    def get_neighbors(self, node_id: str) -> List[NodeResult]
    def search_nodes(self, pattern: str) -> List[NodeResult]
```

### 5.2 QueryService

**Responsibility**: Query processing and coordination

```python
class QueryService:
    """
    Service for complex query operations
    
    Handles:
    - Multi-step queries
    - Query optimization
    - Result formatting
    - Query validation
    """
    
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service
    
    def execute_query(self, query: Query) -> QueryResult:
        """Execute a structured query"""
        pass
    
    def search(self, criteria: SearchCriteria) -> SearchResult:
        """Search with filters and pagination"""
        pass
    
    def aggregate(self, aggregation: Aggregation) -> AggregateResult:
        """Compute aggregations (count, sum, etc.)"""
        pass
```

### 5.3 NLPService

**Responsibility**: Natural language processing

```python
class NLPService:
    """
    Service for natural language query processing
    
    Handles:
    - Intent detection
    - Entity extraction
    - Query mapping
    - AI provider abstraction
    """
    
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service
        self.providers = [OpenAIProvider(), ClaudeProvider()]
    
    def process_query(self, natural_query: str) -> NLPResult:
        """Process natural language query"""
        pass
    
    def extract_intent(self, query: str) -> Intent:
        """Detect user intent"""
        pass
    
    def extract_entities(self, query: str) -> List[Entity]:
        """Extract graph entities from query"""
        pass
    
    def execute_nl_query(self, query: str) -> QueryResult:
        """End-to-end NL query execution"""
        pass
```

### 5.4 ExportService

**Responsibility**: Data import/export

```python
class ExportService:
    """
    Service for data import/export operations
    
    Handles:
    - Format conversion
    - Data validation
    - Serialization/deserialization
    """
    
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service
    
    def export_json(self) -> str:
        """Export graph as JSON"""
        pass
    
    def export_adjacency_list(self) -> str:
        """Export as adjacency list"""
        pass
    
    def import_json(self, data: str) -> ImportResult:
        """Import graph from JSON"""
        pass
    
    def import_adjacency_list(self, data: str) -> ImportResult:
        """Import from adjacency list"""
        pass
```

---

## 6. Data Transfer Objects (DTOs)

### 6.1 Result Objects

```python
@dataclass
class NodeResult:
    node_id: str
    properties: dict
    neighbors: Optional[List[str]] = None

@dataclass
class EdgeResult:
    from_node: str
    to_node: str
    weight: float
    label: Optional[str] = None

@dataclass
class PathResult:
    path: List[str]
    cost: float
    edges: List[EdgeResult]

@dataclass
class TraversalResult:
    order: List[str]
    visited: Set[str]
    depth: Dict[str, int]

@dataclass
class GraphStats:
    node_count: int
    edge_count: int
    avg_degree: float
    is_connected: bool
    diameter: Optional[int] = None
```

### 6.2 Request Objects

```python
@dataclass
class SearchCriteria:
    pattern: str
    filters: dict
    limit: int = 100
    offset: int = 0

@dataclass
class Query:
    operation: str
    parameters: dict
    options: dict = None
```

---

## 7. Error Handling

### 7.1 Service Exceptions

```python
class ServiceError(Exception):
    """Base service exception"""
    pass

class NodeNotFoundError(ServiceError):
    """Node doesn't exist"""
    pass

class InvalidOperationError(ServiceError):
    """Operation not allowed"""
    pass

class ValidationError(ServiceError):
    """Data validation failed"""
    pass
```

### 7.2 Error Translation Layer

API routes should translate service exceptions to HTTP responses:

```python
# In API routes
try:
    result = graph_service.get_node(node_id)
    return jsonify(result), 200
except NodeNotFoundError as e:
    return jsonify({'error': str(e)}), 404
except ServiceError as e:
    return jsonify({'error': str(e)}), 500
```

---

## 8. Testing Strategy

### 8.1 Service Layer Tests

```python
# tests/unit/test_services/test_graph_service.py

def test_add_node():
    service = GraphService()
    result = service.add_node("A", {"label": "Node A"})
    assert result.node_id == "A"
    assert result.properties["label"] == "Node A"

def test_shortest_path():
    service = GraphService()
    # Setup graph
    service.add_node("A")
    service.add_node("B")
    service.add_edge("A", "B")
    
    # Test
    result = service.shortest_path("A", "B")
    assert result.path == ["A", "B"]
    assert result.cost == 1.0
```

### 8.2 Integration Tests

```python
# tests/integration/test_api_service_integration.py

def test_api_calls_service(client):
    """Test that API routes correctly call service layer"""
    response = client.post('/api/graph/node', json={'node_id': 'A'})
    assert response.status_code == 201
```

---

## 9. Migration Plan

### Phase 1: Create Service Layer Structure ✅
- [x] Create service layer directory structure
- [ ] Define base service class
- [ ] Create DTOs/models
- [ ] Define service interfaces

### Phase 2: Implement GraphService
- [ ] Extract node operations from routes
- [ ] Extract edge operations from routes
- [ ] Extract algorithm operations
- [ ] Write service tests

### Phase 3: Implement Supporting Services
- [ ] Create QueryService
- [ ] Create NLPService
- [ ] Create ExportService
- [ ] Write service tests

### Phase 4: Refactor API Routes
- [ ] Update routes to use services
- [ ] Remove business logic from routes
- [ ] Add error translation layer
- [ ] Update integration tests

### Phase 5: Testing & Documentation
- [ ] Complete test coverage
- [ ] Update API documentation
- [ ] Update architecture docs
- [ ] Performance testing

---

## 10. Benefits

### 10.1 For Development
- ✅ Cleaner, more maintainable code
- ✅ Better separation of concerns
- ✅ Easier to add new features
- ✅ Reusable business logic

### 10.2 For Testing
- ✅ Test business logic without HTTP
- ✅ Mock services easily
- ✅ Better test coverage
- ✅ Faster test execution

### 10.3 For Future Expansion
- ✅ Add CLI interface easily
- ✅ Add gRPC/GraphQL easily
- ✅ Support multiple clients
- ✅ Microservice-ready architecture

---

## 11. Next Steps

1. **Review this design** with the team
2. **Create directory structure** in `src/services/`
3. **Implement GraphService** as proof of concept
4. **Refactor one API route** to use the service
5. **Iterate and expand** to other services

---

## 12. References

- Clean Architecture by Robert C. Martin
- Domain-Driven Design by Eric Evans
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [TECH_SPEC.md](../../TECH_SPEC.md)
