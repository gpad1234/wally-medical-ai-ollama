# Graph Database Web UI - Quick Reference

## 🚀 Start the Server

```bash
make run-web-ui
```

Open browser: **http://127.0.0.1:5000**

---

## 🎯 Key Features

### 1. Interactive Visualization
- Drag nodes to rearrange
- Click nodes to view details
- Auto-fills node ID in query form
- Color-coded highlights for results

### 2. Query Operations

#### Get Node Details
```
Node ID: Alice
→ Click "Get Node Info"
→ Shows: properties, degree, neighbors
```

#### Show Neighbors
```
Node ID: Alice
→ Click "Show Neighbors"
→ Lists all adjacent nodes with edge weights
```

#### Search Nodes
```
Property Key: role
Property Value: Developer
→ Click "Search"
→ Highlights all matching nodes
```

### 3. Traversal Algorithms

#### BFS (Breadth-First Search)
```
Algorithm: BFS
Start: Alice
Target: (optional)
→ Level-by-level exploration
→ Shows visited order and distances
```

#### DFS (Depth-First Search)
```
Algorithm: DFS
Start: Alice
Target: (optional)
→ Depth-first exploration
→ Shows path taken
```

#### Shortest Path (Dijkstra)
```
Algorithm: Shortest Path
Start: Alice
Target: Eve
→ Optimal weighted path
→ Shows total cost
```

#### All Paths
```
Algorithm: All Paths
Start: Alice
Target: Eve
→ Every possible route
→ Sorted by cost
```

### 4. Actions

#### Export
- **JSON**: Full graph with metadata
- **Adjacency List**: Simple text format
- Downloads directly to browser

#### Display
- **List All Nodes**: Complete inventory
- **List All Edges**: All connections
- **Refresh Graph**: Reload visualization

#### Management
- **Reset to Sample**: Restore demo graph

---

## 📊 Sample Queries

### Find All Developers
```
Tab: Query
Search Nodes:
  Key: role
  Value: Developer
Result: Alice, Diana, Frank highlighted
```

### Shortest Path Between People
```
Tab: Query
Traversal Algorithms:
  Algorithm: Shortest Path
  Start: Alice
  Target: Eve
Result: Alice → Frank → Diana → Eve
Cost: 20.0
```

### Explore Network from Alice
```
Tab: Query
Traversal Algorithms:
  Algorithm: BFS
  Start: Alice
  Target: (leave empty)
Result: All reachable nodes in level order
```

### Find All Routes
```
Tab: Query
Traversal Algorithms:
  Algorithm: All Paths
  Start: Alice
  Target: Diana
Result: Multiple paths sorted by cost
```

---

## 🔧 Keyboard Shortcuts

- **Click node** → Auto-fills Node ID field
- **Ctrl+F5** → Hard refresh if stuck

---

## 💡 Tips

1. **Click nodes** in visualization instead of typing IDs
2. **Export before resetting** to save custom graphs
3. **Use BFS** for unweighted shortest paths (faster)
4. **Limit All Paths** to small graphs (exponential complexity)
5. **Search by role/team** to find specific people

---

## 🐛 Troubleshooting

### Port 5000 in use
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9

# Or change port in graph_web_ui.py
```

### Graph not displaying
1. Check browser console (F12)
2. Click "Refresh Graph"
3. Try "Reset to Sample"

### Flask errors
```bash
# Reinstall Flask
pip3 install --upgrade flask
```

---

## 📚 Documentation

- **WEB_UI_README.md** - Complete web UI guide
- **GRAPH_DB_GUIDE.md** - API reference
- **GRAPH_ALGORITHMS_GUIDE.md** - Algorithm theory
- **ADJACENCY_LIST_GUIDE.md** - Graph representation

---

## 🎨 Sample Graph Structure

**Nodes (6):**
- Alice (Developer, Backend) - degree: 2
- Bob (Designer, Frontend) - degree: 3
- Charlie (Manager, Product) - degree: 2
- Diana (Developer, Frontend) - degree: 3
- Eve (DevOps, Infrastructure) - degree: 2
- Frank (Developer, Backend) - degree: 3

**Edges (8):**
- Alice → Bob (weight: 5)
- Alice → Frank (weight: 9)
- Bob → Diana (weight: 8)
- Charlie → Alice (weight: 3)
- Charlie → Bob (weight: 4)
- Diana → Eve (weight: 6)
- Eve → Frank (weight: 7)
- Frank → Diana (weight: 5)


# Yes, since debug mode is off, the server won't auto-reload. Let me restart it:

lsof -ti:5000 | xargs kill -9 2>/dev/null; sleep 1; nohup python3 graph_web_ui.py > server.log 2>&1 &
sleep 3
echo "Server restarted"
curl -s http://127.0.0.1:5000/chat | head -5

sleep 3 && curl -s -X POST http://127.0.0.1:5000/api/graph/edge -H "Content-Type: application/json" -d '{"from":"Alice","to":"George","weight":5}' | python3 -m json.tool

curl -s -X POST http://127.0.0.1:5000/api/graph/edge -H "Content-Type: application/json" -d '{"from":"Alice","to":"Bob","weight":10}' | python3 -m json.tool

---
**Last Updated**: November 17, 2025
