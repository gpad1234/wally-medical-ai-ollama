# How to Identify Failed Tests - Quick Reference

## 🎯 Quick Summary

You have **7 failing tests** in the **SERVICE layer**:
- **File:** [tests/unit/test_services/test_graph_service.py](tests/unit/test_services/test_graph_service.py)
- **Success Rate:** 70% (16 passed, 7 failed out of 23 tests)

---

## 🔍 Methods to Identify Failed Tests

### ⚡ Method 1: Use the Helper Script (Fastest)

```bash
./check_failures.sh
```

**Output includes:**
- Overall status per layer
- List of currently failing tests
- Detailed error messages
- Suggested next steps

---

### 🌐 Method 2: Web Dashboard (Most Visual)

**URL:** http://localhost:5001

**Features:**
- **Statistics Cards** - See total passed/failed counts
- **Layer Status Table** - Shows failures per layer with "View Details" button
- **Failing Tests Section** - Red alert banner listing all failures
- **Test History** - Click on any run to see detailed results

**Steps:**
1. Open http://localhost:5001
2. Scroll to "Layer Status" section
3. Look for layers with failed tests (red numbers)
4. Click "View Details" button or scroll to "Currently Failing Tests"

---

### 🔧 Method 3: API Calls (Most Flexible)

#### Get Overall Status
```bash
curl -s http://localhost:5001/api/qc/status | python3 -m json.tool
```

#### Get Failing Tests
```bash
curl -s http://localhost:5001/api/qc/failing-tests | python3 -m json.tool
```

#### Get Specific Run Details
```bash
# First, get a run ID from history
curl -s http://localhost:5001/api/qc/history | python3 -m json.tool

# Then get detailed results
curl -s "http://localhost:5001/api/qc/run/<RUN_ID>" | python3 -m json.tool
```

#### Filter by Layer
```bash
curl -s "http://localhost:5001/api/qc/history?layer=service" | python3 -m json.tool
```

---

### 🐍 Method 4: Python Script

```python
import requests

# Get failing tests
response = requests.get('http://localhost:5001/api/qc/failing-tests')
data = response.json()

for test in data['data']:
    print(f"❌ {test['name']}")
    print(f"   File: {test['test_id'].split('::')[0]}")
    print(f"   Error: {test['error'][:100]}...")
    print()
```

---

### 🧪 Method 5: Direct pytest (Most Detailed)

```bash
# Run specific layer and see output
pytest -m service -v

# Run specific test file
pytest tests/unit/test_services/test_graph_service.py -v

# Run single test with full output
pytest tests/unit/test_services/test_graph_service.py::test_bfs -vv

# Show local variables on failure
pytest tests/unit/test_services/test_graph_service.py::test_bfs -vv -l
```

---

## 📊 Current Failures Summary

Based on the latest run (suite_20260211_140147_0e3cd934):

| # | Test Name | Error Type | Root Cause |
|---|-----------|------------|------------|
| 1 | `test_bfs` | ValueError | Too many values to unpack (expects 2) |
| 2 | `test_clear_graph` | AttributeError | GraphDB has no 'clear' method |
| 3 | `test_dfs` | KeyError | Accessing index 0 of result.order fails |
| 4 | `test_get_edges` | IndexError | Tuple index out of range (edge[3]) |
| 5 | `test_get_edges_for_node` | IndexError | Tuple index out of range (edge[3]) |
| 6 | `test_get_neighbors` | TypeError | Unhashable type: 'dict' |
| 7 | `test_shortest_path` | AssertionError | Cost is 0 instead of 2.0 |

---

## 🔍 Detailed Failure Analysis

### 1. test_bfs - ValueError
```
File: tests/unit/test_services/test_graph_service.py:172
Error: ValueError: too many values to unpack (expected 2)

Code: order, depths = self.graph.bfs(start)
```
**Fix:** Check what `self.graph.bfs()` returns. It's returning more than 2 values.

### 2. test_clear_graph - AttributeError  
```
File: tests/unit/test_services/test_graph_service.py:279
Error: AttributeError: 'GraphDB' object has no attribute 'clear'

Code: self.graph.clear()
```
**Fix:** Add `clear()` method to GraphDB or use different method.

### 3. test_dfs - KeyError
```
File: tests/unit/test_services/test_graph_service.py:196  
Error: KeyError: 0

Code: assert result.order[0] == "A"
```
**Fix:** `result.order` is a dict, not a list. Should be `result.order[0]` or similar.

### 4 & 5. test_get_edges - IndexError
```
File: tests/unit/test_services/test_graph_service.py:142
Error: IndexError: tuple index out of range

Code: weight=edge[3]
```
**Fix:** Edges tuple doesn't have 4 elements. Check edge format.

### 6. test_get_neighbors - TypeError
```
File: tests/unit/test_services/test_graph_service.py:253
Error: TypeError: unhashable type: 'dict'

Code: assert set(neighbors) == {"B", "C"}
```
**Fix:** Neighbors are dicts, not strings. Can't create set from dicts.

### 7. test_shortest_path - AssertionError
```
File: tests/unit/test_services/test_graph_service.py:211
Error: AssertionError: assert 0 == 2.0

Code: assert result.cost == 2.0
```
**Fix:** Path cost calculation is wrong (returning 0 instead of 2.0).

---

## 🛠️ How to Fix

### Option 1: Fix One Test at a Time

```bash
# 1. Run the specific test to see error
pytest tests/unit/test_services/test_graph_service.py::test_bfs -vv

# 2. Open the test file
code tests/unit/test_services/test_graph_service.py

# 3. Open the source file
code src/services/graph_service.py

# 4. Fix the issue

# 5. Re-run the test
pytest tests/unit/test_services/test_graph_service.py::test_bfs -v

# 6. Verify through dashboard
curl -X POST http://localhost:5001/api/qc/run-tests \
  -H 'Content-Type: application/json' \
  -d '{"layer": "service"}'
```

### Option 2: Fix All Service Tests

```bash
# 1. Open the test file
code tests/unit/test_services/test_graph_service.py

# 2. Run all service tests to see failures
pytest -m service -v

# 3. Fix issues in src/services/graph_service.py

# 4. Re-run and verify
pytest -m service -v
```

---

## 📈 Track Progress

After fixing each test, monitor progress:

```bash
# Run the helper script
./check_failures.sh

# Or check via dashboard
open http://localhost:5001

# Or via API
curl -s http://localhost:5001/api/qc/status | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['data']['layers']['service'])"
```

---

## 🎯 Goal

**Target:** 100% pass rate (23/23 tests passing)  
**Current:** 70% pass rate (16/23 tests passing)  
**Remaining:** Fix 7 failing tests

---

## 💡 Tips

1. **Run tests after each fix** - Don't batch fixes
2. **Use -vv flag** - Shows more details
3. **Check dashboard** - Visual feedback is helpful
4. **Read error messages carefully** - They tell you exactly what's wrong
5. **Look at line numbers** - Error shows exact location

---

## 🔗 Quick Links

- **Dashboard:** http://localhost:5001
- **Test File:** [tests/unit/test_services/test_graph_service.py](tests/unit/test_services/test_graph_service.py)
- **Source File:** [src/services/graph_service.py](src/services/graph_service.py)
- **API Docs:** [docs/guides/QC_SYSTEM.md](docs/guides/QC_SYSTEM.md)

---

**Generated by QC Dashboard** - Last updated: 2026-02-11
