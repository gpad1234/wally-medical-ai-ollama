# Guide: Adding and Deleting Nodes and Edges

## Web API Endpoints

The Graph Database Web UI now supports adding and deleting nodes and edges via REST API.

### Add a Node

**Endpoint:** `POST /api/graph/node`

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/graph/node \
  -H "Content-Type: application/json" \
  -d '{
    "id": "George",
    "data": {
      "role": "Tester",
      "team": "QA"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Node George added",
  "node": {
    "id": "George",
    "data": {"role": "Tester", "team": "QA"}
  }
}
```

### Delete a Node

**Endpoint:** `DELETE /api/graph/node/<node_id>`

**Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/graph/node/George
```

**Response:**
```json
{
  "success": true,
  "message": "Node George deleted"
}
```

**Note:** Deleting a node also removes all edges connected to it.

### Add an Edge

**Endpoint:** `POST /api/graph/edge`

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/graph/edge \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Alice",
    "to": "George",
    "weight": 5.0
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Edge added: Alice -> George",
  "edge": {
    "from": "Alice",
    "to": "George",
    "weight": 5.0
  }
}
```

**Note:** Weight is optional and defaults to 1.0

### Delete an Edge

**Endpoint:** `DELETE /api/graph/edge/<from_node>/<to_node>`

**Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/graph/edge/Alice/George
```

**Response:**
```json
{
  "success": true,
  "message": "Edge deleted: Alice -> George"
}
```

## Python API (Direct Use)

You can also use the graph database directly in Python:

```python
from graph_db import GraphDB

# Create graph
graph = GraphDB(directed=True, weighted=True)

# Add nodes
graph.add_node("Alice", {"role": "Developer", "team": "Backend"})
graph.add_node("Bob", {"role": "Designer", "team": "Frontend"})
graph.add_node("Charlie", {"role": "Manager", "team": "Product"})

# Add edges
graph.add_edge("Alice", "Bob", weight=3.0)
graph.add_edge("Bob", "Charlie", weight=2.5)
graph.add_edge("Alice", "Charlie", weight=4.0)

# Check if node exists
if graph.node_exists("Alice"):
    print("Alice exists!")

# Get node data
node = graph.get_node("Alice")
print(f"Node: {node}")  # {'id': 'Alice', 'data': {'role': 'Developer', ...}}

# Delete edge
graph.delete_edge("Alice", "Bob")

# Delete node (also deletes all its edges)
graph.delete_node("Charlie")

# Get all nodes
nodes = graph.get_all_nodes()
print(f"Nodes: {nodes}")  # ['Alice', 'Bob']

# Get all edges
edges = graph.get_all_edges()
print(f"Edges: {edges}")  # [('Bob', 'Charlie', 2.5)]
```

## Complete Example: Building a Social Network

```python
from graph_db import GraphDB

# Create undirected, unweighted graph for social network
social = GraphDB(directed=False, weighted=False)

# Add people
people = [
    ("Alice", {"age": 30, "city": "NYC"}),
    ("Bob", {"age": 25, "city": "SF"}),
    ("Carol", {"age": 28, "city": "NYC"}),
    ("Dave", {"age": 35, "city": "LA"}),
    ("Eve", {"age": 27, "city": "NYC"})
]

for person_id, data in people:
    social.add_node(person_id, data)

# Add friendships (mutual because undirected)
friendships = [
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Dave"),
    ("Carol", "Eve"),
    ("Dave", "Eve")
]

for person1, person2 in friendships:
    social.add_edge(person1, person2)

# Find Alice's friends
alice_neighbors = social.get_neighbors("Alice")
print(f"Alice's friends: {[n['to'] for n in alice_neighbors]}")

# Find people in NYC
def in_nyc(node_id, node_data):
    return node_data.get('data', {}).get('city') == 'NYC'

nyc_people = social.find_nodes(in_nyc)
print(f"People in NYC: {nyc_people}")

# Find path from Alice to Eve
result = social.shortest_path("Alice", "Eve")
print(f"Path from Alice to Eve: {result['path']}")
print(f"Distance: {result['distance']}")

# Remove a friendship
social.delete_edge("Bob", "Dave")

# Remove a person (and all their friendships)
social.delete_node("Carol")
```

## JavaScript (Browser Console)

You can test the API from the browser console while viewing the web UI:

### Add Node
```javascript
fetch('/api/graph/node', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    id: 'George',
    data: {role: 'Tester', team: 'QA'}
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

### Add Edge
```javascript
fetch('/api/graph/edge', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    from: 'Alice',
    to: 'George',
    weight: 5.0
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

### Delete Node
```javascript
fetch('/api/graph/node/George', {
  method: 'DELETE'
})
.then(r => r.json())
.then(d => console.log(d));
```

### Delete Edge
```javascript
fetch('/api/graph/edge/Alice/George', {
  method: 'DELETE'
})
.then(r => r.json())
.then(d => console.log(d));
```

After adding/deleting, refresh the visualization:
```javascript
location.reload();  // Or call initializeVisualization()
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- **200**: Success
- **400**: Bad request (missing parameters)
- **404**: Not found (node/edge doesn't exist)
- **409**: Conflict (node/edge already exists)
- **500**: Internal server error

Example error response:
```json
{
  "error": "Node Alice already exists"
}
```

## Tips

1. **Node IDs must be unique** - Use meaningful identifiers
2. **Nodes must exist before adding edges** - Create nodes first
3. **Deleting a node removes all its edges** - Be careful!
4. **Weights are optional** - Default is 1.0
5. **Check the logs** - Server logs all operations to `graph_web_ui.log`

## Quick Reference

| Operation | Method | Endpoint | Body |
|-----------|--------|----------|------|
| Add Node | POST | `/api/graph/node` | `{"id": "X", "data": {...}}` |
| Delete Node | DELETE | `/api/graph/node/<id>` | - |
| Add Edge | POST | `/api/graph/edge` | `{"from": "X", "to": "Y", "weight": 1.0}` |
| Delete Edge | DELETE | `/api/graph/edge/<from>/<to>` | - |

## Testing

Test the endpoints with curl:

```bash
# Add a node
curl -X POST http://127.0.0.1:5000/api/graph/node \
  -H "Content-Type: application/json" \
  -d '{"id":"Test", "data":{"type":"example"}}'

# Verify it was added
curl http://127.0.0.1:5000/api/graph/nodes | python3 -m json.tool

# Delete it
curl -X DELETE http://127.0.0.1:5000/api/graph/node/Test

# Verify it was deleted
curl http://127.0.0.1:5000/api/graph/nodes | python3 -m json.tool
```
