# Architecture Refactor: Layered File Structure

**Project**: WALLY-CLEAN
**Date**: February 9, 2026
**Goal**: Establish clean layered architecture with Python as the primary interface to C components

---

## 🎯 Design Principles

1. **Clear Layer Separation** - Each layer has a distinct responsibility
2. **Python as Gateway** - All C components accessed through Python wrappers
3. **Dependency Flow** - Upper layers depend on lower layers, never reverse
4. **Testability** - Each layer can be tested independently
5. **Scalability** - Easy to add new components without restructuring

---

## 📐 Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  Web UI, CLI Tools, Examples, Demos                         │
│  Technologies: React, Flask, Python scripts                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    API LAYER (Python)                        │
│  High-level APIs, Business Logic, Orchestration             │
│  Technologies: Python, Flask REST APIs                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    SERVICE LAYER (Python)                    │
│  Graph algorithms, Data processing, Python-specific logic   │
│  Technologies: Pure Python implementations                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    ADAPTER LAYER (Python FFI)                │
│  Python wrappers for C libraries (ctypes)                   │
│  Technologies: Python ctypes, type conversion               │
└─────────────────────────┬───────────────────────────────────┘
                          │ ctypes.CDLL
┌─────────────────────────▼───────────────────────────────────┐
│                    CORE LAYER (C)                            │
│  Data structures, Low-level operations, Performance         │
│  Technologies: C99, Shared libraries (.so/.dylib)           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    SYSTEM LAYER                              │
│  OS primitives, File system, Memory                         │
│  Technologies: POSIX, libc                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Proposed File Structure

```
WALLY-CLEAN/
│
├── src/                          # All source code
│   │
│   ├── core/                     # Layer 5: C Core (lowest level)
│   │   ├── include/              # Public C headers
│   │   │   ├── simple_db.h
│   │   │   ├── linked_list.h
│   │   │   ├── doubly_linked_list.h
│   │   │   └── circular_linked_list.h
│   │   │
│   │   ├── src/                  # C implementations
│   │   │   ├── simple_db.c
│   │   │   ├── linked_list.c
│   │   │   ├── doubly_linked_list.c
│   │   │   └── circular_linked_list.c
│   │   │
│   │   ├── build/                # Build artifacts (gitignored)
│   │   │   ├── lib/              # Compiled .so/.dylib files
│   │   │   └── obj/              # Object files
│   │   │
│   │   └── Makefile              # C build system
│   │
│   ├── adapters/                 # Layer 4: Python-C Bridge (FFI)
│   │   ├── __init__.py
│   │   ├── simple_db.py          # Python wrapper for simple_db.c
│   │   ├── linked_list.py        # Python wrapper for linked_list.c
│   │   └── _loader.py            # Shared library loader utility
│   │
│   ├── services/                 # Layer 3: Business Logic (Python)
│   │   ├── __init__.py
│   │   ├── graph_db.py           # Graph database implementation
│   │   ├── graph_algorithms.py   # BFS, DFS, Dijkstra, etc.
│   │   └── nlp_parser.py         # Natural language query parser
│   │
│   ├── api/                      # Layer 2: REST API (Flask)
│   │   ├── __init__.py
│   │   ├── app.py                # Flask application
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py          # /api/graph/* endpoints
│   │   │   └── nlp.py            # /api/nlp/* endpoints
│   │   │
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── cors.py           # CORS configuration
│   │       └── logging.py        # Request logging
│   │
│   └── web/                      # Layer 1: Frontend (React)
│       ├── package.json
│       ├── vite.config.js
│       ├── public/
│       ├── src/
│       │   ├── components/
│       │   ├── services/         # API client
│       │   ├── store/            # Zustand state
│       │   └── App.jsx
│       └── dist/                 # Build output (gitignored)
│
├── examples/                     # Example programs and demos
│   ├── python/
│   │   ├── graph_examples.py
│   │   └── db_examples.py
│   │
│   ├── c/
│   │   ├── linked_list_demo.c
│   │   ├── array_pointer_demo.c
│   │   └── struct_memory_demo.c
│   │
│   └── notebooks/                # Jupyter notebooks
│       └── graph_tutorial.ipynb
│
├── tests/                        # All tests
│   ├── unit/
│   │   ├── test_core/            # C unit tests
│   │   ├── test_adapters/        # Python wrapper tests
│   │   └── test_services/        # Service layer tests
│   │
│   ├── integration/              # Integration tests
│   │   └── test_api.py
│   │
│   └── performance/              # Benchmarks
│       └── benchmark_graph.py
│
├── docs/                         # Documentation
│   ├── architecture/
│   │   ├── ARCHITECTURE.md
│   │   ├── LAYERS.md
│   │   └── DATA_FLOW.md
│   │
│   ├── guides/
│   │   ├── GRAPH_DB_GUIDE.md
│   │   ├── GRAPH_ALGORITHMS_GUIDE.md
│   │   ├── ARRAY_POINTER_GUIDE.md
│   │   └── FFI_GUIDE.md
│   │
│   ├── api/
│   │   ├── REST_API.md
│   │   └── C_API_REFERENCE.md
│   │
│   └── tutorials/
│       ├── GETTING_STARTED.md
│       └── ADVANCED_USAGE.md
│
├── scripts/                      # Utility scripts
│   ├── build.sh                  # Build all components
│   ├── run.sh                    # Start servers
│   ├── test.sh                   # Run all tests
│   └── deploy.sh                 # Deployment script
│
├── config/                       # Configuration files
│   ├── development.env
│   ├── production.env
│   └── test.env
│
├── .github/                      # GitHub specific
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Python package setup
├── .gitignore
├── README.md
├── LICENSE
└── Makefile                      # Top-level build orchestration
```

---

## 🔧 Layer Responsibilities

### Layer 5: Core (C)
**Location**: `src/core/`

**Responsibilities:**
- Low-level data structures (hash tables, linked lists)
- Performance-critical operations
- Memory management
- No Python dependencies

**Files:**
- `src/core/include/*.h` - Public C API headers
- `src/core/src/*.c` - C implementations
- `src/core/Makefile` - Build system

**Example:**
```c
// src/core/include/simple_db.h
#ifndef SIMPLE_DB_H
#define SIMPLE_DB_H

typedef struct Database Database;

Database* db_create(void);
bool db_set(Database *db, const char *key, const char *value);
const char* db_get(Database *db, const char *key);
void db_destroy(Database *db);

#endif
```

---

### Layer 4: Adapters (Python FFI)
**Location**: `src/adapters/`

**Responsibilities:**
- Load C shared libraries
- Wrap C functions with Python interface
- Handle type conversions (Python ↔ C)
- Manage memory ownership
- Provide Pythonic API

**Files:**
- `src/adapters/simple_db.py` - SimpleDB Python wrapper
- `src/adapters/_loader.py` - Shared library loader

**Example:**
```python
# src/adapters/simple_db.py
"""
Python adapter for simple_db C library.
This is the ONLY place where ctypes is used for simple_db.
"""
import ctypes
from typing import Optional
from ._loader import load_library

# Load the C library
_lib = load_library("libsimpledb")

# Define C function signatures
_lib.db_create.argtypes = []
_lib.db_create.restype = ctypes.c_void_p

_lib.db_set.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
_lib.db_set.restype = ctypes.c_bool

_lib.db_get.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.db_get.restype = ctypes.c_char_p

_lib.db_destroy.argtypes = [ctypes.c_void_p]
_lib.db_destroy.restype = None


class SimpleDB:
    """Python wrapper for C simple_db library."""

    def __init__(self):
        self._db = _lib.db_create()
        if not self._db:
            raise MemoryError("Failed to create database")

    def set(self, key: str, value: str) -> bool:
        """Set a key-value pair."""
        return _lib.db_set(
            self._db,
            key.encode('utf-8'),
            value.encode('utf-8')
        )

    def get(self, key: str) -> Optional[str]:
        """Get a value by key."""
        result = _lib.db_get(self._db, key.encode('utf-8'))
        return result.decode('utf-8') if result else None

    def __del__(self):
        if hasattr(self, '_db') and self._db:
            _lib.db_destroy(self._db)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.__del__()
```

```python
# src/adapters/_loader.py
"""
Utility to load C shared libraries.
Handles platform differences (Linux .so, macOS .dylib, Windows .dll)
"""
import os
import ctypes
from pathlib import Path

def load_library(name: str) -> ctypes.CDLL:
    """
    Load a C shared library by name.

    Args:
        name: Library name (e.g., "libsimpledb")

    Returns:
        Loaded library object
    """
    # Determine library extension
    if os.name == 'nt':
        ext = '.dll'
    elif os.uname().sysname == 'Darwin':
        ext = '.dylib'
    else:
        ext = '.so'

    # Find library in build directory
    project_root = Path(__file__).parent.parent.parent
    lib_path = project_root / 'src' / 'core' / 'build' / 'lib' / f'{name}{ext}'

    if not lib_path.exists():
        raise FileNotFoundError(
            f"Library not found: {lib_path}\n"
            f"Run 'make' in src/core/ to build C libraries"
        )

    return ctypes.CDLL(str(lib_path))
```

---

### Layer 3: Services (Python Business Logic)
**Location**: `src/services/`

**Responsibilities:**
- Graph database implementation
- Algorithm implementations (BFS, DFS, etc.)
- Business logic
- Uses adapters to access C layer

**Files:**
- `src/services/graph_db.py` - Graph database
- `src/services/graph_algorithms.py` - Algorithms

**Example:**
```python
# src/services/graph_db.py
"""
Graph Database Service.
Uses SimpleDB adapter to store graph data.
"""
import json
from typing import List, Dict, Optional
from ..adapters.simple_db import SimpleDB


class GraphDB:
    """Graph database built on top of SimpleDB."""

    def __init__(self, directed: bool = True):
        self._db = SimpleDB()  # Uses adapter layer
        self.directed = directed
        self._init_metadata()

    def _init_metadata(self):
        """Initialize metadata."""
        self._db.set("__meta__:directed", str(self.directed))
        self._db.set("__meta__:node_count", "0")

    def add_node(self, node_id: str, data: Optional[Dict] = None) -> bool:
        """Add a node to the graph."""
        key = f"node:{node_id}"

        if self._db.get(key):
            return False  # Already exists

        # Store node data
        node_data = data or {}
        self._db.set(key, json.dumps(node_data))

        # Initialize adjacency list
        self._db.set(f"adj:{node_id}", "[]")

        # Update count
        count = int(self._db.get("__meta__:node_count") or "0")
        self._db.set("__meta__:node_count", str(count + 1))

        return True

    def add_edge(self, from_node: str, to_node: str, weight: float = 1.0) -> bool:
        """Add an edge between nodes."""
        # Verify nodes exist
        if not self._db.get(f"node:{from_node}"):
            return False
        if not self._db.get(f"node:{to_node}"):
            return False

        # Get adjacency list
        adj_key = f"adj:{from_node}"
        adj_list = json.loads(self._db.get(adj_key) or "[]")

        # Add edge
        adj_list.append({"to": to_node, "weight": weight})
        self._db.set(adj_key, json.dumps(adj_list))

        # Store edge data
        edge_key = f"edge:{from_node}:{to_node}"
        self._db.set(edge_key, json.dumps({"weight": weight}))

        return True

    def nodes(self) -> List[str]:
        """Get all node IDs."""
        # In real implementation, iterate through DB keys
        # For now, simplified
        pass
```

```python
# src/services/graph_algorithms.py
"""
Graph algorithms implementation.
Pure Python, uses GraphDB service.
"""
from collections import deque
from typing import List, Dict, Set, Optional
from .graph_db import GraphDB


class GraphAlgorithms:
    """Graph traversal and search algorithms."""

    def __init__(self, graph: GraphDB):
        self.graph = graph

    def bfs(self, start: str, end: Optional[str] = None) -> Dict:
        """
        Breadth-First Search traversal.

        Args:
            start: Starting node ID
            end: Optional ending node ID

        Returns:
            Dictionary with visited nodes, distances, and path
        """
        visited = set()
        distances = {start: 0}
        parent = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            if current == end:
                break

            if current in visited:
                continue

            visited.add(current)

            # Get neighbors from graph
            neighbors = self.graph.get_neighbors(current)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    if neighbor not in distances:
                        distances[neighbor] = distances[current] + 1
                        parent[neighbor] = current

        # Reconstruct path
        path = []
        if end and end in parent:
            node = end
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()

        return {
            'visited': list(visited),
            'distances': distances,
            'path': path
        }

    def dfs(self, start: str) -> List[str]:
        """Depth-First Search traversal."""
        visited = []
        self._dfs_recursive(start, visited, set())
        return visited

    def _dfs_recursive(self, node: str, visited: List, seen: Set):
        """Recursive DFS helper."""
        if node in seen:
            return

        seen.add(node)
        visited.append(node)

        for neighbor in self.graph.get_neighbors(node):
            self._dfs_recursive(neighbor, visited, seen)
```

---

### Layer 2: API (Flask REST)
**Location**: `src/api/`

**Responsibilities:**
- HTTP endpoints
- Request/response handling
- Authentication (future)
- CORS, logging, middleware

**Files:**
- `src/api/app.py` - Flask application
- `src/api/routes/graph.py` - Graph endpoints

**Example:**
```python
# src/api/app.py
"""
Flask REST API for graph database.
"""
from flask import Flask
from flask_cors import CORS
from .routes import graph, nlp
from .middleware import logging_middleware


def create_app(config=None):
    """Application factory."""
    app = Flask(__name__)

    # Configuration
    if config:
        app.config.update(config)

    # CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
        }
    })

    # Middleware
    app.before_request(logging_middleware.log_request)

    # Register blueprints
    app.register_blueprint(graph.bp, url_prefix='/api/graph')
    app.register_blueprint(nlp.bp, url_prefix='/api/nlp')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5001, debug=False)
```

```python
# src/api/routes/graph.py
"""
Graph API endpoints.
"""
from flask import Blueprint, jsonify, request
from ...services.graph_db import GraphDB
from ...services.graph_algorithms import GraphAlgorithms

bp = Blueprint('graph', __name__)

# Create graph instance (in production, use app context)
graph = GraphDB()
algorithms = GraphAlgorithms(graph)


@bp.route('/nodes', methods=['GET'])
def get_nodes():
    """Get all nodes."""
    nodes = graph.nodes()
    return jsonify({'nodes': nodes})


@bp.route('/nodes', methods=['POST'])
def add_node():
    """Add a new node."""
    data = request.json
    node_id = data.get('id')
    node_data = data.get('data', {})

    if not node_id:
        return jsonify({'error': 'Missing node ID'}), 400

    success = graph.add_node(node_id, node_data)

    if success:
        return jsonify({'success': True, 'id': node_id}), 201
    else:
        return jsonify({'error': 'Node already exists'}), 409


@bp.route('/edges', methods=['POST'])
def add_edge():
    """Add a new edge."""
    data = request.json
    from_node = data.get('from')
    to_node = data.get('to')
    weight = data.get('weight', 1.0)

    if not from_node or not to_node:
        return jsonify({'error': 'Missing from/to nodes'}), 400

    success = graph.add_edge(from_node, to_node, weight)

    if success:
        return jsonify({'success': True}), 201
    else:
        return jsonify({'error': 'Nodes not found'}), 404


@bp.route('/traverse/bfs', methods=['POST'])
def bfs():
    """BFS traversal."""
    data = request.json
    start = data.get('start')
    end = data.get('end')

    if not start:
        return jsonify({'error': 'Missing start node'}), 400

    result = algorithms.bfs(start, end)
    return jsonify(result)
```

---

### Layer 1: Web UI (React)
**Location**: `src/web/`

**Responsibilities:**
- User interface
- API client
- State management
- Visualization

**Files:**
- `src/web/src/services/api.js` - API client
- `src/web/src/components/` - React components

**Example:**
```javascript
// src/web/src/services/api.js
/**
 * API client for graph database backend.
 */
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5001/api';

export const graphApi = {
  // Nodes
  getNodes: async () => {
    const response = await axios.get(`${API_BASE}/graph/nodes`);
    return response.data.nodes;
  },

  addNode: async (id, data = {}) => {
    const response = await axios.post(`${API_BASE}/graph/nodes`, {
      id,
      data
    });
    return response.data;
  },

  // Edges
  addEdge: async (from, to, weight = 1.0) => {
    const response = await axios.post(`${API_BASE}/graph/edges`, {
      from,
      to,
      weight
    });
    return response.data;
  },

  // Algorithms
  bfs: async (start, end = null) => {
    const response = await axios.post(`${API_BASE}/graph/traverse/bfs`, {
      start,
      end
    });
    return response.data;
  }
};
```

---

## 🔄 Data Flow Example

### Adding a Node (Full Stack)

```
1. USER ACTION (Layer 1 - React)
   └─> User clicks "Add Node" button
   └─> src/web/src/components/Graph/AddNodeButton.jsx

2. API CALL (Layer 1 - React)
   └─> graphApi.addNode("Alice", {age: 30})
   └─> src/web/src/services/api.js
   └─> HTTP POST to http://127.0.0.1:5001/api/graph/nodes

3. API ENDPOINT (Layer 2 - Flask)
   └─> src/api/routes/graph.py::add_node()
   └─> Validates request
   └─> Calls graph.add_node("Alice", {age: 30})

4. SERVICE LAYER (Layer 3 - Python)
   └─> src/services/graph_db.py::add_node()
   └─> Business logic: format data, update metadata
   └─> Calls self._db.set("node:Alice", '{"age": 30}')

5. ADAPTER LAYER (Layer 4 - Python FFI)
   └─> src/adapters/simple_db.py::set()
   └─> Type conversion: str → bytes
   └─> Calls _lib.db_set(self._db, b"node:Alice", b'{"age": 30}')

6. CORE LAYER (Layer 5 - C)
   └─> src/core/src/simple_db.c::db_set()
   └─> Compute hash
   └─> Allocate memory
   └─> Insert into hash table
   └─> Return true

7. RESPONSE FLOW (Back up)
   └─> true → Python → Flask → JSON → React → UI update
```

---

## 🔨 Build System

### Top-Level Makefile
```makefile
# Makefile (root directory)
# Orchestrates building all components

.PHONY: all clean build-core build-python build-web test run

all: build-core build-python build-web

# Build C core libraries
build-core:
	@echo "Building C core libraries..."
	$(MAKE) -C src/core

# Install Python packages
build-python:
	@echo "Installing Python packages..."
	pip install -e .

# Build React frontend
build-web:
	@echo "Building React frontend..."
	cd src/web && npm install && npm run build

# Run all tests
test:
	@echo "Running tests..."
	pytest tests/

# Clean all build artifacts
clean:
	$(MAKE) -C src/core clean
	rm -rf src/web/dist
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Development mode
run:
	@echo "Starting development servers..."
	./scripts/run.sh
```

### Core Makefile
```makefile
# src/core/Makefile
# Build C libraries

CC = gcc
CFLAGS = -Wall -Wextra -g -O2 -fPIC
LDFLAGS = -shared

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LIB_EXT = .dylib
else
    LIB_EXT = .so
endif

BUILD_DIR = build
LIB_DIR = $(BUILD_DIR)/lib
OBJ_DIR = $(BUILD_DIR)/obj

# Libraries to build
LIBS = $(LIB_DIR)/libsimpledb$(LIB_EXT) \
       $(LIB_DIR)/liblinkedlist$(LIB_EXT)

all: $(BUILD_DIR) $(LIBS)

$(BUILD_DIR):
	mkdir -p $(LIB_DIR) $(OBJ_DIR)

# SimpleDB library
$(LIB_DIR)/libsimpledb$(LIB_EXT): $(OBJ_DIR)/simple_db.o
	$(CC) $(LDFLAGS) $^ -o $@

$(OBJ_DIR)/simple_db.o: src/simple_db.c include/simple_db.h
	$(CC) $(CFLAGS) -c $< -o $@

# Linked List library
$(LIB_DIR)/liblinkedlist$(LIB_EXT): $(OBJ_DIR)/linked_list.o
	$(CC) $(LDFLAGS) $^ -o $@

$(OBJ_DIR)/linked_list.o: src/linked_list.c include/linked_list.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean
```

---

## 📦 Python Package Setup

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name='wally-graph',
    version='1.0.0',
    packages=find_packages(where='src', exclude=['web']),
    package_dir={'': 'src'},
    install_requires=[
        'flask>=3.0.0',
        'flask-cors>=4.0.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'wally-server=api.app:main',
        ]
    }
)
```

---

## 🧪 Testing Strategy

### Unit Tests by Layer

```python
# tests/unit/test_adapters/test_simple_db.py
"""Test SimpleDB adapter."""
import pytest
from src.adapters.simple_db import SimpleDB

def test_create_db():
    db = SimpleDB()
    assert db is not None

def test_set_get():
    with SimpleDB() as db:
        assert db.set("key1", "value1")
        assert db.get("key1") == "value1"

def test_get_nonexistent():
    with SimpleDB() as db:
        assert db.get("nonexistent") is None
```

```python
# tests/unit/test_services/test_graph_db.py
"""Test GraphDB service."""
import pytest
from src.services.graph_db import GraphDB

def test_add_node():
    graph = GraphDB()
    assert graph.add_node("A", {"label": "Node A"})
    assert not graph.add_node("A")  # Duplicate

def test_add_edge():
    graph = GraphDB()
    graph.add_node("A")
    graph.add_node("B")
    assert graph.add_edge("A", "B", weight=1.5)
```

---

## 📚 Import Patterns

### Correct Import Usage

```python
# Layer 1 (Web) - N/A (JavaScript)

# Layer 2 (API) imports Layer 3 (Services)
from ...services.graph_db import GraphDB
from ...services.graph_algorithms import GraphAlgorithms

# Layer 3 (Services) imports Layer 4 (Adapters)
from ..adapters.simple_db import SimpleDB
from ..adapters.linked_list import LinkedList

# Layer 4 (Adapters) imports nothing (uses ctypes)
import ctypes
from ._loader import load_library

# Layer 5 (Core) - Pure C (no imports)
```

### Anti-Pattern (Don't Do This!)
```python
# ❌ BAD: Adapter importing Service
# src/adapters/simple_db.py
from ..services.graph_db import GraphDB  # WRONG!

# ❌ BAD: Core importing anything
# src/core/src/simple_db.c
#include <Python.h>  // WRONG! Core should be pure C
```

---

## 🚀 Migration Plan

### Step 1: Create New Structure (1-2 days)
```bash
# Create directories
mkdir -p src/{core/{include,src,build/{lib,obj}},adapters,services,api/routes,web}
mkdir -p examples/{python,c}
mkdir -p tests/{unit,integration,performance}
mkdir -p docs/{architecture,guides,api,tutorials}
mkdir -p scripts config
```

### Step 2: Move C Files (1 day)
```bash
# Move C headers
mv *.h src/core/include/

# Move C source
mv *.c src/core/src/

# Move Makefile
mv Makefile src/core/
```

### Step 3: Create Adapters (2-3 days)
- Extract ctypes code from current Python files
- Create clean adapter layer
- Add _loader.py utility

### Step 4: Refactor Python (2-3 days)
- Split graph_db.py into service layer
- Create API layer with Flask routes
- Update imports

### Step 5: Move Frontend (1 day)
- Move graph-ui/ to src/web/
- Update paths in package.json

### Step 6: Documentation (2 days)
- Move all .md files to docs/
- Update paths in documentation

### Step 7: Testing (3-4 days)
- Set up pytest structure
- Add unit tests for each layer
- Add integration tests

### Step 8: Build System (1-2 days)
- Create top-level Makefile
- Update core Makefile
- Create build/run scripts

---

## ✅ Benefits of This Architecture

1. **Clear Separation** - Each layer has one job
2. **Testable** - Can test each layer independently
3. **Maintainable** - Easy to find and modify code
4. **Scalable** - Easy to add new features
5. **Professional** - Industry-standard structure
6. **Python Gateway** - All C access through Python adapters
7. **Type Safety** - FFI layer handles all conversions
8. **Documentation** - Structure is self-documenting

---

## 📝 Next Steps

1. Review this architecture proposal
2. Approve or suggest modifications
3. Begin Step 1: Create directory structure
4. Gradually migrate files layer by layer
5. Test at each step

---

**Questions to Consider:**

1. Should we keep C examples in `examples/c/` or separate `demos/` directory?
2. Should tests live in `tests/` or alongside code (e.g., `src/tests/`)?
3. Do we need a separate `lib/` directory at root for distribution?
4. Should we use setuptools or poetry for Python packaging?

---

**Last Updated:** February 9, 2026
**Version:** 1.0
