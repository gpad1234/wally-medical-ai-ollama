# Technical Specification: Web Interface to Python API using JSON-RPC with Flask

## 1. Overview

This document specifies the architecture and implementation of a web-based interface that exposes a Python API through JSON-RPC 2.0 protocol using Flask as the HTTP server.

### 1.1 Purpose
Provide a standardized, language-agnostic interface for interacting with the Graph Database and related services through HTTP using JSON-RPC 2.0 specification.

### 1.2 Scope
- JSON-RPC 2.0 compliant API endpoints
- Flask-based HTTP server
- Graph traversal operations (BFS, DFS)
- Node and edge management
- Database operations
- Error handling and validation
- Request/response logging

---

## 2. Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  (Web UI, CLI, SDK, Mobile Apps, Third-party Tools)     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├─► HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────┐
│             Flask HTTP Server Layer                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Request Handler / JSON-RPC Router               │  │
│  │  - Parameter Validation                          │  │
│  │  - Method Routing                                │  │
│  │  - Error Handling                                │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          Python API Layer (Business Logic)              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Graph Database API                              │  │
│  │  - GraphDB class                                 │  │
│  │  - Traversal algorithms                          │  │
│  │  - Node/Edge operations                          │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Simple Database (persistence layer)             │  │
│  │  - In-memory storage                             │  │
│  │  - Data serialization                            │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### 2.2 Component Breakdown

#### Flask Server
- HTTP request handler
- JSON-RPC request/response routing
- CORS support
- Request logging and debugging

#### JSON-RPC Dispatcher
- Routes JSON-RPC method calls to appropriate handlers
- Validates JSON-RPC 2.0 format
- Manages method versioning
- Error response generation

#### API Methods Layer
- Implements Graph operations
- Implements database operations
- Returns properly formatted responses

---

## 3. JSON-RPC 2.0 Specification

### 3.1 Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  },
  "id": 1
}
```

**Fields:**
- `jsonrpc` (string, required): Must be "2.0"
- `method` (string, required): The name of the method to invoke
- `params` (object or array, optional): Parameters for the method
- `id` (string/number, required for request-response): Request identifier

### 3.2 Response Format

#### Success Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "key": "value"
  },
  "id": 1
}
```

#### Error Response

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Error description",
    "data": {
      "details": "Additional error information"
    }
  },
  "id": 1
}
```

### 3.3 Error Codes

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON was received |
| -32600 | Invalid Request | The JSON sent is not a valid Request object |
| -32601 | Method not found | The method does not exist / is not available |
| -32602 | Invalid params | Invalid method parameter(s) |
| -32603 | Internal error | Internal JSON-RPC error |
| -32000 | Server error | Application-specific error |

---

## 4. API Methods

### 4.1 Graph Operations

#### 4.1.1 `graph.create`
Create a new graph instance.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.create",
  "params": {
    "directed": true,
    "weighted": false
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "graph_id": "graph_123",
    "directed": true,
    "weighted": false,
    "created_at": "2025-11-18T10:30:00Z"
  },
  "id": 1
}
```

#### 4.1.2 `graph.add_node`
Add a node to the graph.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.add_node",
  "params": {
    "graph_id": "graph_123",
    "node_id": "node_1",
    "data": {
      "label": "Node 1",
      "properties": {}
    }
  },
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "node_id": "node_1",
    "message": "Node added successfully"
  },
  "id": 2
}
```

#### 4.1.3 `graph.add_edge`
Add an edge between two nodes.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.add_edge",
  "params": {
    "graph_id": "graph_123",
    "source": "node_1",
    "target": "node_2",
    "weight": 1.0,
    "directed": true
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "edge_id": "edge_1_2",
    "message": "Edge added successfully"
  },
  "id": 3
}
```

#### 4.1.4 `graph.get_node`
Retrieve node information.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.get_node",
  "params": {
    "graph_id": "graph_123",
    "node_id": "node_1"
  },
  "id": 4
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "node_id": "node_1",
    "data": {
      "label": "Node 1"
    },
    "neighbors": ["node_2", "node_3"]
  },
  "id": 4
}
```

#### 4.1.5 `graph.delete_node`
Delete a node from the graph.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.delete_node",
  "params": {
    "graph_id": "graph_123",
    "node_id": "node_1"
  },
  "id": 5
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "message": "Node deleted successfully",
    "removed_edges": 2
  },
  "id": 5
}
```

#### 4.1.6 `graph.delete_edge`
Delete an edge from the graph.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.delete_edge",
  "params": {
    "graph_id": "graph_123",
    "source": "node_1",
    "target": "node_2"
  },
  "id": 6
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "message": "Edge deleted successfully"
  },
  "id": 6
}
```

### 4.2 Graph Traversal Operations

#### 4.2.1 `graph.bfs`
Breadth-First Search traversal.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.bfs",
  "params": {
    "graph_id": "graph_123",
    "start_node": "node_1",
    "max_depth": 10
  },
  "id": 7
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "traversal_type": "BFS",
    "start_node": "node_1",
    "visited_nodes": ["node_1", "node_2", "node_3"],
    "total_visited": 3,
    "execution_time_ms": 1.5,
    "path": ["node_1", "node_2", "node_3"]
  },
  "id": 7
}
```

#### 4.2.2 `graph.dfs`
Depth-First Search traversal.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.dfs",
  "params": {
    "graph_id": "graph_123",
    "start_node": "node_1",
    "max_depth": 10
  },
  "id": 8
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "traversal_type": "DFS",
    "start_node": "node_1",
    "visited_nodes": ["node_1", "node_2", "node_4"],
    "total_visited": 3,
    "execution_time_ms": 0.8,
    "path": ["node_1", "node_2", "node_4"]
  },
  "id": 8
}
```

#### 4.2.3 `graph.shortest_path`
Find shortest path between two nodes.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "graph.shortest_path",
  "params": {
    "graph_id": "graph_123",
    "source": "node_1",
    "target": "node_5"
  },
  "id": 9
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "source": "node_1",
    "target": "node_5",
    "path": ["node_1", "node_2", "node_3", "node_5"],
    "distance": 3,
    "exists": true
  },
  "id": 9
}
```

### 4.3 Database Operations

#### 4.3.1 `db.set`
Set a key-value pair in the database.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "db.set",
  "params": {
    "key": "user:123",
    "value": "Alice"
  },
  "id": 10
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "key": "user:123",
    "message": "Value set successfully"
  },
  "id": 10
}
```

#### 4.3.2 `db.get`
Get a value from the database.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "db.get",
  "params": {
    "key": "user:123"
  },
  "id": 11
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "key": "user:123",
    "value": "Alice",
    "exists": true
  },
  "id": 11
}
```

#### 4.3.3 `db.delete`
Delete a key from the database.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "db.delete",
  "params": {
    "key": "user:123"
  },
  "id": 12
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "key": "user:123",
    "message": "Key deleted successfully"
  },
  "id": 12
}
```

#### 4.3.4 `db.clear`
Clear all data from the database.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "db.clear",
  "params": {},
  "id": 13
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "message": "Database cleared successfully"
  },
  "id": 13
}
```

#### 4.3.5 `db.count`
Get the count of keys in the database.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "db.count",
  "params": {},
  "id": 14
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "count": 42,
    "message": "42 keys in database"
  },
  "id": 14
}
```

### 4.4 System Operations

#### 4.4.1 `system.info`
Get system information.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "system.info",
  "params": {},
  "id": 15
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "version": "1.0.0",
    "api_version": "2.0",
    "name": "Graph Database API",
    "uptime_seconds": 3600
  },
  "id": 15
}
```

#### 4.4.2 `system.status`
Get server status.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "system.status",
  "params": {},
  "id": 16
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "running",
    "timestamp": "2025-11-18T10:35:00Z",
    "active_graphs": 5,
    "db_records": 256
  },
  "id": 16
}
```

---

## 5. HTTP Endpoints

### 5.1 Primary Endpoint

**Endpoint:** `POST /api/rpc`

**Content-Type:** `application/json`

**Description:** Handles all JSON-RPC 2.0 requests

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "graph.create",
    "params": {"directed": true, "weighted": false},
    "id": 1
  }'
```

### 5.2 Batch Requests

**Endpoint:** `POST /api/rpc`

**Description:** Multiple JSON-RPC requests in a single HTTP request

**Request:**
```json
[
  {
    "jsonrpc": "2.0",
    "method": "graph.create",
    "params": {"directed": true},
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "method": "system.info",
    "params": {},
    "id": 2
  }
]
```

**Response:**
```json
[
  {
    "jsonrpc": "2.0",
    "result": {"graph_id": "graph_123", "directed": true},
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "result": {"version": "1.0.0", "api_version": "2.0"},
    "id": 2
  }
]
```

### 5.3 Health Check Endpoint

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-18T10:35:00Z"
}
```

---

## 6. Implementation Details

### 6.1 Flask Application Structure

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import json
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# JSON-RPC Method Registry
rpc_methods = {
    'graph.create': handle_graph_create,
    'graph.add_node': handle_graph_add_node,
    'graph.add_edge': handle_graph_add_edge,
    'graph.get_node': handle_graph_get_node,
    'graph.delete_node': handle_graph_delete_node,
    'graph.delete_edge': handle_graph_delete_edge,
    'graph.bfs': handle_graph_bfs,
    'graph.dfs': handle_graph_dfs,
    'db.set': handle_db_set,
    'db.get': handle_db_get,
    'db.delete': handle_db_delete,
    'system.info': handle_system_info,
    'system.status': handle_system_status,
}

@app.route('/api/rpc', methods=['POST'])
def rpc_handler():
    """
    Main JSON-RPC 2.0 request handler
    """
    # Implementation details in section 6.2
    pass

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 6.2 Request Handler Implementation

```python
def handle_rpc_request(data):
    """
    Process a single JSON-RPC request
    """
    try:
        # Validate JSON-RPC 2.0 format
        if 'jsonrpc' not in data or data['jsonrpc'] != '2.0':
            return error_response(-32600, 'Invalid Request', data.get('id'))
        
        if 'method' not in data:
            return error_response(-32600, 'Invalid Request', data.get('id'))
        
        method_name = data['method']
        params = data.get('params', {})
        request_id = data.get('id')
        
        # Check if method exists
        if method_name not in rpc_methods:
            return error_response(-32601, 'Method not found', request_id)
        
        # Call method
        handler = rpc_methods[method_name]
        result = handler(params)
        
        # Return success response
        if request_id is not None:
            return {
                'jsonrpc': '2.0',
                'result': result,
                'id': request_id
            }
        
    except ValueError as e:
        return error_response(-32602, 'Invalid params', data.get('id'), str(e))
    except Exception as e:
        return error_response(-32603, 'Internal error', data.get('id'), str(e))

def error_response(code, message, request_id, data=None):
    """
    Generate JSON-RPC error response
    """
    response = {
        'jsonrpc': '2.0',
        'error': {
            'code': code,
            'message': message
        }
    }
    if data:
        response['error']['data'] = {'details': data}
    if request_id is not None:
        response['id'] = request_id
    return response
```

### 6.3 Error Handling Strategy

1. **Input Validation:** Validate all incoming parameters before processing
2. **Type Checking:** Ensure parameters match expected types
3. **Range Validation:** Check for valid ranges and constraints
4. **Exception Handling:** Catch and convert exceptions to JSON-RPC errors
5. **Logging:** Log all errors for debugging and monitoring

### 6.4 CORS Configuration

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 7. Security Considerations

### 7.1 Input Validation
- Validate all incoming parameters
- Implement type checking
- Sanitize string inputs
- Limit request size

### 7.2 Authentication & Authorization
- Implement API key authentication for production
- Use HTTPS in production environment
- Add rate limiting for API endpoints
- Implement request signing for sensitive operations

### 7.3 Error Information Disclosure
- Avoid exposing internal system details in error messages
- Log detailed errors server-side only
- Return generic error messages to clients in production

### 7.4 Data Validation
- Validate node_id and edge parameters
- Prevent injection attacks
- Validate graph_id format
- Enforce parameter constraints

---

## 8. Performance Considerations

### 8.1 Response Times
- Optimize graph traversal algorithms
- Cache frequently accessed data
- Implement pagination for large result sets
- Use asynchronous operations for long-running tasks

### 8.2 Scalability
- Use connection pooling for database
- Implement request queuing for high concurrency
- Monitor memory usage
- Use efficient data structures

### 8.3 Monitoring & Metrics
- Track API response times
- Monitor error rates
- Log request patterns
- Collect performance metrics

---

## 9. Testing Strategy

### 9.1 Unit Tests
- Test individual JSON-RPC method handlers
- Test error response generation
- Test parameter validation

### 9.2 Integration Tests
- Test end-to-end JSON-RPC requests
- Test batch request handling
- Test error scenarios
- Test graph operations

### 9.3 Test Coverage
```python
# Example test
def test_graph_create():
    response = make_rpc_request({
        'jsonrpc': '2.0',
        'method': 'graph.create',
        'params': {'directed': True, 'weighted': False},
        'id': 1
    })
    assert response['result']['graph_id'] is not None
    assert response['result']['directed'] == True
```

---

## 10. Documentation & Examples

### 10.1 API Documentation
- OpenAPI/Swagger specification
- Interactive API explorer
- Method reference documentation
- Error code reference

### 10.2 Client Examples
- Python client library
- JavaScript/Node.js examples
- cURL examples
- Postman collection

### 10.3 Deployment Guide
- Installation instructions
- Configuration options
- Environment setup
- Production deployment

---

## 11. Future Enhancements

1. **WebSocket Support:** Real-time graph updates via WebSocket
2. **GraphQL Interface:** Alternative GraphQL API
3. **Event Streaming:** Subscribe to graph change events
4. **Authentication:** JWT/OAuth2 integration
5. **Caching Layer:** Redis integration for performance
6. **Analytics:** Usage statistics and monitoring dashboard
7. **Versioning:** API versioning strategy
8. **Rate Limiting:** Implement rate limiting per client

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| JSON-RPC | JSON Remote Procedure Call, a stateless, light-weight remote procedure call protocol |
| RPC | Remote Procedure Call |
| Flask | Python web framework for building web applications |
| API | Application Programming Interface |
| HTTP | HyperText Transfer Protocol |
| CORS | Cross-Origin Resource Sharing |
| Traversal | Algorithm to visit all nodes in a graph |
| BFS | Breadth-First Search algorithm |
| DFS | Depth-First Search algorithm |

---

## Document Information

- **Version:** 1.0
- **Created:** 2025-11-18
- **Status:** Final
- **Author:** AI Assistant
- **Last Updated:** 2025-11-18

