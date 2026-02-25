# Testing Strategy: WALLY-CLEAN

**Date:** February 10, 2026
**Goal:** Comprehensive testing for every architectural layer

---

## 🎯 Testing Philosophy

1. **Test every layer independently**
2. **Test layer integration**
3. **Use Python for all testing** (even C layer tests)
4. **Follow AAA pattern** (Arrange, Act, Assert)
5. **Document test cases before writing code**

---

## 📊 Test Coverage Goals

| Layer | Unit Tests | Integration Tests | Coverage Target |
|-------|-----------|-------------------|-----------------|
| Core (C) | ✅ | ✅ | 90%+ |
| Adapters (Python-C) | ✅ | ✅ | 95%+ |
| Services | ⏳ | ⏳ | 90%+ |
| API | ⏳ | ⏳ | 85%+ |
| Web | ⏳ | N/A | 80%+ |

---

## 🧪 Layer 1: Core (C Libraries)

### Test Approach
- Use Python + ctypes to test C functions directly
- Test memory management, edge cases, performance
- Test all public API functions

### Test Cases: SimpleDB

**Basic Operations:**
```
TC-C-001: Database Creation
  - Create database
  - Verify non-NULL pointer returned
  - Verify initial count is 0

TC-C-002: Set Operation
  - Set key-value pair
  - Verify operation returns true
  - Verify count increases

TC-C-003: Get Operation
  - Set a key-value
  - Get the value
  - Verify correct value returned

TC-C-004: Get Non-existent Key
  - Get key that doesn't exist
  - Verify NULL returned

TC-C-005: Delete Operation
  - Set key-value
  - Delete the key
  - Verify returns true
  - Verify key no longer exists

TC-C-006: Delete Non-existent Key
  - Delete key that doesn't exist
  - Verify returns false
```

**Edge Cases:**
```
TC-C-007: Empty Key
  - Set with empty string key
  - Verify behavior (should fail or handle gracefully)

TC-C-008: Empty Value
  - Set with empty string value
  - Verify stored correctly

TC-C-009: Very Long Key
  - Set with 256+ character key
  - Verify handling (truncate or reject)

TC-C-010: Very Long Value
  - Set with 4096+ character value
  - Verify handling

TC-C-011: Special Characters
  - Set with Unicode, newlines, nulls
  - Verify correct storage and retrieval

TC-C-012: Collision Handling
  - Force hash collisions
  - Verify separate chaining works
  - Verify all values retrievable
```

**Stress Tests:**
```
TC-C-013: Large Dataset
  - Insert 10,000 key-value pairs
  - Verify all retrievable
  - Check performance

TC-C-014: Many Updates
  - Update same key 1000 times
  - Verify no memory leaks
  - Verify final value correct

TC-C-015: Clear and Reuse
  - Fill database
  - Clear it
  - Fill again
  - Verify works correctly
```

**Memory Tests:**
```
TC-C-016: Memory Leaks
  - Create and destroy database 1000 times
  - Verify no memory growth

TC-C-017: Large Value Memory
  - Store many large values
  - Verify memory usage reasonable

TC-C-018: Keys Array Memory
  - Call db_keys() multiple times
  - Verify no memory leaks
```

---

## 🐍 Layer 2: Adapters (Python-C Bridge)

### Test Approach
- Test Python API convenience features
- Test type conversions
- Test error handling
- Test Pythonic interfaces

### Test Cases: SimpleDB Adapter

**Python API:**
```
TC-A-001: Context Manager
  - Use 'with SimpleDB() as db'
  - Verify automatic cleanup

TC-A-002: Dict-like Access
  - Use db["key"] = "value"
  - Use db["key"] to retrieve
  - Verify works correctly

TC-A-003: Contains Operator
  - Use "key" in db
  - Verify returns boolean

TC-A-004: Len Function
  - Use len(db)
  - Verify returns count

TC-A-005: Del Operator
  - Use del db["key"]
  - Verify key deleted
  - Verify KeyError on non-existent
```

**Type Handling:**
```
TC-A-006: Unicode Strings
  - Store/retrieve Unicode characters
  - Verify correct encoding/decoding

TC-A-007: Type Errors
  - Try to set with non-string key
  - Verify TypeError raised

TC-A-008: None Values
  - Test behavior with None
  - Verify graceful handling
```

**Integration:**
```
TC-A-009: Adapter-Core Integration
  - Verify adapter calls C functions correctly
  - Verify return values converted properly

TC-A-010: Multiple Instances
  - Create multiple SimpleDB instances
  - Verify independence

TC-A-011: Performance Overhead
  - Measure adapter overhead vs direct C
  - Verify overhead < 10%
```

---

## 📦 Layer 3: Services (Business Logic)

### Test Cases: GraphDB Service

**Node Operations:**
```
TC-S-001: Add Node
  - Add node with data
  - Verify stored correctly
  - Verify metadata updated

TC-S-002: Add Duplicate Node
  - Add same node twice
  - Verify second add fails

TC-S-003: Delete Node
  - Add node, then delete
  - Verify removed completely
  - Verify edges cleaned up

TC-S-004: Get Node
  - Add node with data
  - Retrieve node
  - Verify data correct
```

**Edge Operations:**
```
TC-S-005: Add Edge
  - Add two nodes
  - Add edge between them
  - Verify adjacency list updated

TC-S-006: Add Edge Non-existent Nodes
  - Try to add edge with missing nodes
  - Verify fails gracefully

TC-S-007: Weighted Edges
  - Add edge with weight
  - Verify weight stored correctly

TC-S-008: Directed vs Undirected
  - Test both graph types
  - Verify edge directionality
```

**Algorithms:**
```
TC-S-009: BFS Traversal
  - Create graph A->B->C
  - BFS from A
  - Verify order: [A, B, C]

TC-S-010: BFS Path Finding
  - Create graph with path
  - Find path A to E
  - Verify shortest path returned

TC-S-011: DFS Traversal
  - Create graph
  - DFS from root
  - Verify depth-first order

TC-S-012: Dijkstra Shortest Path
  - Create weighted graph
  - Find shortest path
  - Verify weight calculated correctly
```

---

## 🌐 Layer 4: API (Flask REST)

### Test Cases: REST Endpoints

**Graph Endpoints:**
```
TC-API-001: GET /api/graph/nodes
  - Request all nodes
  - Verify 200 status
  - Verify JSON response

TC-API-002: POST /api/graph/nodes
  - Create new node
  - Verify 201 status
  - Verify node created

TC-API-003: POST /api/graph/edges
  - Create edge
  - Verify 201 status
  - Verify edge exists

TC-API-004: POST /api/graph/traverse/bfs
  - Request BFS traversal
  - Verify result correct
  - Verify 200 status
```

**Error Handling:**
```
TC-API-005: Invalid JSON
  - Send malformed JSON
  - Verify 400 error

TC-API-006: Missing Parameters
  - Send request without required params
  - Verify 400 error with message

TC-API-007: Non-existent Node
  - Request non-existent node
  - Verify 404 error
```

**CORS:**
```
TC-API-008: CORS Headers
  - Send OPTIONS request
  - Verify CORS headers present

TC-API-009: Cross-Origin Request
  - Send request from allowed origin
  - Verify succeeds
```

---

## 🧰 Test Tools & Setup

### Required Packages
```bash
pip install pytest pytest-cov pytest-mock requests
```

### Test Directory Structure
```
tests/
├── unit/
│   ├── test_core/
│   │   ├── test_simple_db.py
│   │   └── test_linked_list.py
│   ├── test_adapters/
│   │   ├── test_simple_db_adapter.py
│   │   └── test_loader.py
│   └── test_services/
│       ├── test_graph_db.py
│       └── test_graph_algorithms.py
├── integration/
│   ├── test_adapter_core.py
│   ├── test_service_adapter.py
│   └── test_api_full_stack.py
├── performance/
│   ├── benchmark_core.py
│   ├── benchmark_adapter.py
│   └── benchmark_service.py
└── conftest.py  # Pytest fixtures
```

---

## 🚀 Running Tests

### All Tests
```bash
pytest tests/
```

### By Layer
```bash
pytest tests/unit/test_core/
pytest tests/unit/test_adapters/
pytest tests/unit/test_services/
```

### With Coverage
```bash
pytest --cov=src --cov-report=html tests/
```

### Single Test
```bash
pytest tests/unit/test_core/test_simple_db.py::test_db_create
```

---

## 📝 Test Documentation Template

```python
def test_feature_name():
    """
    Test Case: TC-X-###: Feature Description

    Arrange:
        - Setup conditions

    Act:
        - Perform action

    Assert:
        - Verify results

    Edge Cases:
        - List any edge cases tested
    """
    # Test implementation
```

---

## ✅ Success Criteria

**Per Test:**
- [ ] Test passes consistently
- [ ] Test is independent
- [ ] Test is fast (< 1s for unit tests)
- [ ] Test has clear documentation

**Per Layer:**
- [ ] All critical paths tested
- [ ] Edge cases covered
- [ ] Integration points tested
- [ ] Performance acceptable

**Overall:**
- [ ] 90%+ code coverage
- [ ] All tests passing
- [ ] CI/CD pipeline green
- [ ] Documentation complete

---

**Next Steps:**
1. Install pytest and dependencies
2. Create test fixtures
3. Implement Core layer tests
4. Implement Adapter layer tests
5. Run and verify all tests pass

