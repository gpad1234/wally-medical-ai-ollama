# Web UI Logging Guide

## Overview

The Graph Database Web UI now includes comprehensive error logging to help diagnose and fix issues quickly.

## Logging Features

### 1. **Dual Output**
- **Console**: All logs appear in the terminal where the server runs
- **File**: All logs are also written to `graph_web_ui.log` in the project directory

### 2. **Log Levels**
- **INFO**: Normal operations (requests, results)
- **DEBUG**: Detailed debugging information (request data, node details)
- **ERROR**: Errors and exceptions with full stack traces

### 3. **What Gets Logged**

#### API Requests
Every API endpoint logs:
```
INFO - GET /api/graph/stats
INFO - POST /api/graph/bfs
DEBUG - BFS request data: {'start': 'Alice', 'target': 'Bob'}
```

#### Results
Success results are logged:
```
INFO - BFS result: visited=4, path=['Alice', 'Bob']
INFO - Found 3 paths between Alice and Frank
INFO - Visualization data: 6 nodes, 8 edges
```

#### Errors
Detailed error information:
```
ERROR - Error in get_visualization_data: 'id'
ERROR - Traceback (most recent call last):
  File "graph_web_ui.py", line 381, in get_visualization_data
    'id': node['id'],
KeyError: 'id'
```

## Log File Location

```
/Users/gp/c-work/getting-started/symmetrical-robot/graph_web_ui.log
```

**Note**: This file is listed in `.gitignore` and won't be committed to version control.

## How to Use Logs

### 1. **Monitor in Real-Time**
Watch logs as they're written:
```bash
tail -f graph_web_ui.log
```

### 2. **Search for Errors**
Find all error messages:
```bash
grep ERROR graph_web_ui.log
```

### 3. **Search for Specific Endpoint**
Find logs for a specific API call:
```bash
grep "POST /api/graph/bfs" graph_web_ui.log
```

### 4. **View Recent Activity**
See last 50 log lines:
```bash
tail -n 50 graph_web_ui.log
```

### 5. **Clear Old Logs**
Delete the log file to start fresh:
```bash
rm graph_web_ui.log
```
The file will be recreated when you restart the server.

## Logged Endpoints

All endpoints include error logging:

### Read Operations
- `GET /api/graph/stats` - Graph statistics
- `GET /api/graph/nodes` - All nodes
- `GET /api/graph/edges` - All edges
- `GET /api/graph/node/<id>` - Single node details
- `GET /api/graph/neighbors/<id>` - Node neighbors
- `GET /api/graph/visualization` - Visualization data
- `GET /api/graph/export/json` - JSON export
- `GET /api/graph/export/adjacency` - Adjacency list export

### Traversal Operations
- `POST /api/graph/bfs` - Breadth-first search
- `POST /api/graph/dfs` - Depth-first search
- `POST /api/graph/shortest_path` - Shortest path (Dijkstra/BFS)
- `POST /api/graph/all_paths` - Find all paths

### Search and Actions
- `POST /api/graph/search` - Search nodes by criteria
- `POST /api/graph/reset` - Reset to sample graph

## Example Log Output

```
2025-11-17 06:15:23,456 - __main__ - INFO - Initializing sample graph...
2025-11-17 06:15:23,457 - __main__ - INFO - Starting Flask server on http://127.0.0.1:5000
2025-11-17 06:15:30,123 - __main__ - INFO - GET /api/graph/stats
2025-11-17 06:15:30,125 - __main__ - INFO - Stats: 6 nodes, 8 edges
2025-11-17 06:15:32,456 - __main__ - INFO - GET /api/graph/visualization
2025-11-17 06:15:32,458 - __main__ - DEBUG - Found 6 node IDs: ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
2025-11-17 06:15:32,460 - __main__ - INFO - Visualization data: 6 nodes, 8 edges
2025-11-17 06:15:45,789 - __main__ - INFO - POST /api/graph/bfs
2025-11-17 06:15:45,790 - __main__ - DEBUG - BFS request data: {'start': 'Alice', 'target': 'Frank'}
2025-11-17 06:15:45,792 - __main__ - INFO - BFS result: visited=6, path=['Alice', 'Bob', 'Charlie', 'Frank']
```

## Debugging Tips

### Problem: API returns 500 error
**Solution**: Check the log file for the full stack trace
```bash
grep -A 10 "ERROR" graph_web_ui.log
```

### Problem: Unexpected data in visualization
**Solution**: Enable DEBUG level logging to see node details
The DEBUG level is already enabled and will show:
- Exact request data received
- Node IDs found
- Node data retrieved
- Paths calculated

### Problem: Performance issues
**Solution**: Check log timestamps to find slow operations
```bash
grep "INFO -" graph_web_ui.log | tail -n 20
```

## Log Format

Each log entry contains:
1. **Timestamp**: `2025-11-17 06:15:23,456`
2. **Logger**: `__main__`
3. **Level**: `INFO`, `DEBUG`, `ERROR`
4. **Message**: The log message

Example:
```
2025-11-17 06:15:45,792 - __main__ - INFO - BFS result: visited=6, path=['Alice', 'Bob']
```

## Error Handling

All endpoints now have try-except blocks that:
1. Log the error with full stack trace
2. Return a JSON error response to the client
3. Include the error message in the response

Example error response:
```json
{
  "error": "Internal server error: 'id'"
}
```

## Best Practices

1. **Keep logs during development** - Don't delete until issue is resolved
2. **Check logs after errors** - Always review the log file when something goes wrong
3. **Monitor in real-time** - Use `tail -f` when testing
4. **Search efficiently** - Use `grep` to find specific errors or endpoints
5. **Clear periodically** - Delete old logs when no longer needed

## Configuration

The logging is configured in `graph_web_ui.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('graph_web_ui.log'),
        logging.StreamHandler()
    ]
)
```

To change log level to INFO only (less verbose):
```python
level=logging.INFO  # Instead of logging.DEBUG
```

## Troubleshooting

### Log file not created
- Make sure the server has started at least once
- Check write permissions in the directory
- Look for error messages in the console

### Too much output
- Change log level from DEBUG to INFO
- Filter output: `grep -v DEBUG graph_web_ui.log`

### Can't find specific error
- Search by endpoint: `grep "POST /api/graph/bfs" graph_web_ui.log`
- Search by time: Check timestamp ranges
- Search by keyword: `grep -i "error" graph_web_ui.log`
