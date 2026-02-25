# Graph Database - Technical Guide

A powerful in-memory graph database built on top of SimpleDB, featuring graph traversal algorithms, flexible import/export, and comprehensive node/edge operations.

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Graph Types](#graph-types)
- [API Reference](#api-reference)
- [Algorithms](#algorithms)
- [Import/Export Formats](#importexport-formats)
- [Examples](#examples)
- [Use Cases](#use-cases)

---

## ✨ Features

### Core Functionality
- ✅ **Directed & Undirected Graphs**
- ✅ **Weighted & Unweighted Edges**
- ✅ **Dynamic Node/Edge Operations** (add, delete, update)
- ✅ **In-Memory Storage** using SimpleDB hash table
- ✅ **Graph Traversal**: BFS, DFS
- ✅ **Shortest Path**: Dijkstra's algorithm
- ✅ **All Paths Finding**
- ✅ **Node Search & Queries**
- ✅ **Import/Export**: JSON & Adjacency List

### Performance
- **Fast Operations**: O(1) average for node/edge access
- **Efficient Traversal**: BFS/DFS with visited tracking
- **Optimal Paths**: Dijkstra with priority queue
- **Scalable**: Handles thousands of nodes/edges

---

## 🚀 Quick Start

### Basic Usage

```python
from graph_db import GraphDB

# Create a directed graph
graph = GraphDB(directed=True, weighted=False)

# Add nodes
graph.add_node("A", {"label": "Start"})
graph.add_node("B", {"label": "Middle"})
graph.add_node("C", {"label": "End"})

# Add edges
graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("A", "C")

# BFS traversal
result = graph.bfs("A", "C")
print(f"Path: {result['path']}")  # ['A', 'C']

# Export to JSON
json_str = graph.export_to_json()
```

### Running Examples

```bash
# Run basic graph demo
make run-graph-db

# Run all examples
make run-graph-examples

# Run all graph tests
make test-graph
```

---

## 📊 Graph Types

### Directed vs Undirected

```python
# Directed: A → B (one-way)
directed_graph = GraphDB(directed=True)
directed_graph.add_edge("A", "B")
# Can go from A to B, but not B to A

# Undirected: A ↔ B (two-way)
undirected_graph = GraphDB(directed=False)
undirected_graph.add_edge("A", "B")
# Can go from A to B AND B to A
```

### Weighted vs Unweighted

```python
# Weighted: edges have costs/distances
weighted_graph = GraphDB(weighted=True)
weighted_graph.add_edge("NYC", "Boston", 215.0)  # 215 miles

# Unweighted: all edges equal
unweighted_graph = GraphDB(weighted=False)
unweighted_graph.add_edge("A", "B")  # default weight = 1.0
```

---

## 📖 API Reference

### Node Operations

#### `add_node(node_id, data=None)`
Add a node to the graph.

```python
graph.add_node("user123", {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
})
```

#### `delete_node(node_id)`
Delete a node and all its edges.

```python
graph.delete_node("user123")
```

#### `get_node(node_id)`
Get node data.

```python
data = graph.get_node("user123")
# Returns: {"name": "Alice", "age": 30, ...}
```

#### `update_node(node_id, data)`
Update node data.

```python
graph.update_node("user123", {"age": 31})
```

#### `node_exists(node_id)`
Check if node exists.

```python
if graph.node_exists("user123"):
    print("User exists!")
```

#### `get_all_nodes()`
Get list of all node IDs.

```python
nodes = graph.get_all_nodes()
# Returns: ["A", "B", "C", ...]
```

### Edge Operations

#### `add_edge(from_node, to_node, weight=1.0)`
Add an edge between two nodes.

```python
# Unweighted
graph.add_edge("A", "B")

# Weighted
graph.add_edge("NYC", "Boston", 215.0)
```

#### `delete_edge(from_node, to_node)`
Delete an edge.

```python
graph.delete_edge("A", "B")
```

#### `get_edge(from_node, to_node)`
Get edge data.

```python
edge = graph.get_edge("NYC", "Boston")
# Returns: {"weight": 215.0}
```

#### `edge_exists(from_node, to_node)`
Check if edge exists.

```python
if graph.edge_exists("A", "B"):
    print("Edge exists!")
```

#### `get_neighbors(node_id)`
Get all neighbors of a node.

```python
neighbors = graph.get_neighbors("A")
# Returns: [{"to": "B"}, {"to": "C", "weight": 2.0}, ...]
```

#### `get_all_edges()`
Get all edges in the graph.

```python
edges = graph.get_all_edges()
# Returns: [("A", "B", None), ("NYC", "Boston", 215.0), ...]
```

### Traversal Algorithms

#### `bfs(start_node, target_node=None)`
Breadth-First Search.

```python
result = graph.bfs("A", "E")
# Returns:
{
    "visited": ["A", "B", "C", "D", "E"],
    "found": True,
    "path": ["A", "C", "E"],
    "distances": {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2}
}
```

#### `dfs(start_node, target_node=None)`
Depth-First Search.

```python
result = graph.dfs("A", "E")
# Returns:
{
    "visited": ["A", "B", "D", "E"],
    "found": True,
    "path": ["A", "B", "D", "E"]
}
```

#### `shortest_path(start_node, end_node)`
Find shortest path (Dijkstra for weighted, BFS for unweighted).

```python
result = graph.shortest_path("NYC", "Washington")
# Returns:
{
    "path": ["NYC", "Philadelphia", "Washington"],
    "distance": 235.0
}
```

#### `find_all_paths(start_node, end_node, max_length=None)`
Find all paths between two nodes.

```python
paths = graph.find_all_paths("A", "E", max_length=5)
# Returns: [
#     ["A", "B", "D", "E"],
#     ["A", "C", "D", "E"],
#     ["A", "C", "E"]
# ]
```

### Search & Query

#### `find_nodes(predicate)`
Find nodes matching a condition.

```python
# Find all users over 30
older_users = graph.find_nodes(
    lambda id, data: data.get("age", 0) > 30
)
```

#### `get_degree(node_id)`
Get node degree information.

```python
degree = graph.get_degree("A")
# Returns:
{
    "in_degree": 2,    # edges coming in
    "out_degree": 3,   # edges going out
    "total": 5
}
```

### Import/Export

#### `import_from_json(json_str)`
Import graph from JSON.

```python
json_data = '''
{
    "directed": true,
    "weighted": false,
    "nodes": [
        {"id": "A", "data": {"label": "Node A"}},
        {"id": "B", "data": {"label": "Node B"}}
    ],
    "edges": [
        {"from": "A", "to": "B"}
    ]
}
'''

graph.import_from_json(json_data)
```

#### `export_to_json(pretty=True)`
Export graph to JSON.

```python
json_str = graph.export_to_json(pretty=True)
print(json_str)
```

#### `import_from_adjacency_list(text)`
Import from adjacency list format.

```python
adj_list = """
A -> B, C
B -> D
C -> D, E
"""

graph.import_from_adjacency_list(adj_list)
```

#### `export_to_adjacency_list()`
Export to adjacency list format.

```python
adj_str = graph.export_to_adjacency_list()
# Returns:
# A -> B, C
# B -> D
# C -> D, E
```

---

## 🧮 Algorithms

### Breadth-First Search (BFS)

**Use Case**: Shortest path in unweighted graphs, level-order traversal

**Complexity**: O(V + E) where V = vertices, E = edges

**Example**: Social network degrees of separation

```python
# Find how many degrees separate Alice from Eve
result = graph.bfs("alice", "eve")
print(f"Separation: {result['distances']['eve']} degrees")
```

### Depth-First Search (DFS)

**Use Case**: Path finding, cycle detection, topological sorting

**Complexity**: O(V + E)

**Example**: Dependency resolution

```python
# Find dependency installation order
result = graph.dfs("app")
install_order = reversed(result['visited'])
```

### Dijkstra's Algorithm

**Use Case**: Shortest path in weighted graphs

**Complexity**: O((V + E) log V) with priority queue

**Example**: Route planning

```python
# Find shortest route from NYC to LA
result = graph.shortest_path("NYC", "LA")
print(f"Distance: {result['distance']} miles")
print(f"Route: {' -> '.join(result['path'])}")
```

---

## 📁 Import/Export Formats

### JSON Format

**Structure:**
```json
{
  "directed": true,
  "weighted": false,
  "nodes": [
    {
      "id": "node1",
      "data": {
        "attribute1": "value1",
        "attribute2": "value2"
      }
    }
  ],
  "edges": [
    {
      "from": "node1",
      "to": "node2",
      "weight": 1.5
    }
  ]
}
```

**Usage:**
```python
# Export
with open("graph.json", "w") as f:
    f.write(graph.export_to_json())

# Import
with open("graph.json", "r") as f:
    graph.import_from_json(f.read())
```

### Adjacency List Format

**Structure:**
```
# Unweighted
A -> B, C, D
B -> E
C -> E, F

# Weighted
A -> B(1.5), C(2.0)
B -> D(3.5)
```

**Usage:**
```python
# Export
adj_list = graph.export_to_adjacency_list()
with open("graph.txt", "w") as f:
    f.write(adj_list)

# Import
with open("graph.txt", "r") as f:
    graph.import_from_adjacency_list(f.read())
```

---

## 💡 Examples

### Example 1: Social Network

```python
from graph_db import GraphDB

# Create undirected graph (friendships)
graph = GraphDB(directed=False)

# Add people
graph.add_node("alice", {"name": "Alice", "city": "NYC"})
graph.add_node("bob", {"name": "Bob", "city": "SF"})
graph.add_node("charlie", {"name": "Charlie", "city": "NYC"})

# Add friendships
graph.add_edge("alice", "bob")
graph.add_edge("alice", "charlie")

# Find Alice's network
network = graph.bfs("alice")
print(f"Alice knows {len(network['visited']) - 1} people")

# Find people in NYC
nyc_people = graph.find_nodes(
    lambda id, data: data.get("city") == "NYC"
)
```

### Example 2: Road Network

```python
# Create weighted undirected graph
graph = GraphDB(directed=False, weighted=True)

# Add cities
for city in ["NYC", "Boston", "Philadelphia"]:
    graph.add_node(city)

# Add roads with distances
graph.add_edge("NYC", "Boston", 215.0)
graph.add_edge("NYC", "Philadelphia", 95.0)
graph.add_edge("Boston", "Philadelphia", 300.0)

# Find shortest route
route = graph.shortest_path("NYC", "Boston")
print(f"Shortest route: {' -> '.join(route['path'])}")
print(f"Distance: {route['distance']} miles")
```

### Example 3: Package Dependencies

```python
# Create directed graph
graph = GraphDB(directed=True)

# Define dependencies
dependencies = {
    "app": ["web-framework", "database"],
    "web-framework": ["http-server"],
    "database": ["connection-pool"],
    "http-server": [],
    "connection-pool": []
}

# Build graph
for package, deps in dependencies.items():
    graph.add_node(package)
    for dep in deps:
        if not graph.node_exists(dep):
            graph.add_node(dep)
        graph.add_edge(package, dep)

# Get installation order (reverse DFS)
install_order = list(reversed(graph.dfs("app")['visited']))
print("Install order:", install_order)
```

### Example 4: Workflow Processing

```python
# Import workflow from JSON
workflow_json = '''
{
    "directed": true,
    "weighted": true,
    "nodes": [
        {"id": "START", "data": {"type": "input"}},
        {"id": "PROCESS", "data": {"type": "compute"}},
        {"id": "END", "data": {"type": "output"}}
    ],
    "edges": [
        {"from": "START", "to": "PROCESS", "weight": 1.0},
        {"from": "PROCESS", "to": "END", "weight": 2.0}
    ]
}
'''

graph = GraphDB()
graph.import_from_json(workflow_json)

# Find all execution paths
paths = graph.find_all_paths("START", "END")
for i, path in enumerate(paths, 1):
    print(f"Path {i}: {' -> '.join(path)}")
```

---

## 🎯 Use Cases

### 1. Social Networks
- Friend recommendations
- Degrees of separation
- Community detection
- Influence propagation

### 2. Navigation & Routing
- GPS route planning
- Network topology
- Shortest path finding
- Alternative route discovery

### 3. Dependency Management
- Package dependencies
- Build order resolution
- Circular dependency detection
- Impact analysis

### 4. Web Crawling
- Site structure mapping
- Link analysis
- Page rank calculation
- Broken link detection

### 5. Workflow Management
- Process flow modeling
- Task scheduling
- Critical path analysis
- Resource allocation

### 6. Knowledge Graphs
- Entity relationships
- Semantic networks
- Ontology representation
- Query answering

### 7. Network Analysis
- Computer networks
- Social media analysis
- Citation networks
- Collaboration graphs

### 8. Game Development
- Pathfinding (NPCs)
- Level connectivity
- Quest dependencies
- Skill trees

---

## 🔧 Advanced Features

### Context Manager Support

```python
with GraphDB(directed=True) as graph:
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B")
    
    result = graph.bfs("A")
    print(result)
# Automatically cleaned up
```

### Node Filtering

```python
# Find high-value nodes
valuable = graph.find_nodes(
    lambda id, data: data.get("value", 0) > 100
)

# Find nodes by type
processing_nodes = graph.find_nodes(
    lambda id, data: data.get("type") == "processor"
)
```

### Path Constraints

```python
# Find paths with length limit
short_paths = graph.find_all_paths("A", "Z", max_length=3)

# Shortest weighted path
optimal = graph.shortest_path("start", "end")
```

### Statistics

```python
stats = graph.get_stats()
# Returns:
{
    "nodes": 100,
    "edges": 250,
    "directed": True,
    "weighted": False,
    "db_entries": 450
}
```

---

## 📊 Performance

| Operation | Time Complexity | Notes |
|-----------|-----------------|-------|
| Add Node | O(1) | Hash table insertion |
| Delete Node | O(E) | Must remove all edges |
| Add Edge | O(1) | Hash table + list append |
| Delete Edge | O(1) | Hash table deletion |
| BFS | O(V + E) | All nodes and edges visited |
| DFS | O(V + E) | All nodes and edges visited |
| Dijkstra | O((V + E) log V) | Priority queue operations |
| Find All Paths | O(V!) | Exponential worst case |

**Memory**: O(V + E) for storing graph

---

## 🧪 Testing

```bash
# Run graph database demo
python3 graph_db.py

# Run all examples
python3 graph_examples.py

# Using make
make run-graph-db
make run-graph-examples
make test-graph
```

---

## 📚 References

- **BFS/DFS**: Classic graph traversal algorithms
- **Dijkstra's Algorithm**: Single-source shortest path
- **Graph Theory**: Fundamental data structure concepts
- **SimpleDB**: Underlying in-memory storage

---

## 🎓 Learning Resources

### Concepts Demonstrated
1. **Graph Data Structures** - Adjacency lists, node/edge storage
2. **Graph Algorithms** - BFS, DFS, Dijkstra, all paths
3. **Hash Tables** - Fast node/edge lookup via SimpleDB
4. **Python FFI** - Using C library from Python
5. **Import/Export** - JSON and text format parsing
6. **Design Patterns** - Factory, strategy, iterator

### Algorithm Complexity
- **Space-Time Tradeoffs** - Memory for speed
- **Big-O Analysis** - Algorithmic efficiency
- **Graph Properties** - Directed vs undirected, weighted vs unweighted

---

## 💾 Storage Details

Graph data is stored in SimpleDB with the following key patterns:

```
node:<id>           → node data (JSON)
adj:<id>            → adjacency list (JSON array)
edge:<from>:<to>    → edge data (JSON)
__meta__:directed   → "true" or "false"
__meta__:weighted   → "true" or "false"
__meta__:node_count → number of nodes
__meta__:edge_count → number of edges
```

This enables O(1) average access to nodes and edges while maintaining full graph structure.

---

**Version**: 1.0  
**Language**: Python 3.x  
**Dependencies**: simple_db_python.py  
**License**: MIT
