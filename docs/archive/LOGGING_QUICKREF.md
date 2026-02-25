# Quick Reference: Server Error Logging

## ✅ What's Now Enabled

The Graph Database Web UI now logs all server activity to help diagnose errors:

### Log Locations
- **File**: `graph_web_ui.log` (in project directory)
- **Console**: Terminal where server runs

### What Gets Logged
✅ All API requests (endpoint, method)  
✅ Request parameters (JSON body)  
✅ Operation results (paths found, nodes returned)  
✅ **Errors with full stack traces**  
✅ Timing and performance info  

## 🔍 How to View Errors

### Real-time Monitoring
```bash
# Watch logs as they happen
tail -f graph_web_ui.log
```

### Find All Errors
```bash
# Show all ERROR lines
grep ERROR graph_web_ui.log
```

### Show Error Context
```bash
# Show 5 lines after each error (includes stack trace)
grep -A 5 ERROR graph_web_ui.log
```

### Recent Activity
```bash
# Show last 30 log entries
tail -n 30 graph_web_ui.log
```

## 🐛 Error Example

When an error occurs, you'll see detailed logs like:

```
2025-11-17 06:12:02,785 - __main__ - ERROR - Unhandled exception: 'NoneType' object has no attribute 'get'
2025-11-17 06:12:02,794 - __main__ - ERROR - Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/Users/gp/c-work/getting-started/symmetrical-robot/graph_web_ui.py", line 177, in get_neighbors
    'data': neighbor.get('data', {}),
AttributeError: 'NoneType' object has no attribute 'get'
```

This tells you:
- **Timestamp**: When it happened
- **Error Type**: AttributeError
- **Location**: graph_web_ui.py, line 177
- **Function**: get_neighbors
- **Root Cause**: neighbor variable is None

## 📊 Success Logs

Normal operations are logged too:

```
2025-11-17 06:10:57,920 - __main__ - INFO - GET /api/graph/stats
2025-11-17 06:10:57,924 - __main__ - INFO - Stats: 6 nodes, 8 edges
2025-11-17 06:10:57,943 - __main__ - INFO - Visualization data: 6 nodes, 8 edges
2025-11-17 06:13:19,096 - __main__ - INFO - Search found 3 nodes matching key='role', value='Developer'
```

## 🔧 Common Commands

### Search for specific endpoint
```bash
grep "POST /api/graph/bfs" graph_web_ui.log
```

### Count errors
```bash
grep -c ERROR graph_web_ui.log
```

### Clear logs and start fresh
```bash
rm graph_web_ui.log
# Log file will be recreated when server restarts
```

### Save errors to separate file
```bash
grep ERROR graph_web_ui.log > errors.txt
```

## 📝 Log Levels

- **DEBUG**: Detailed info (request data, node details)
- **INFO**: Normal operations (requests, results)
- **ERROR**: Problems with full stack traces
- **WARNING**: Non-critical issues

## 🎯 Tips

1. **Always check logs first** when something doesn't work
2. **Use `tail -f`** to monitor in real-time during testing
3. **Search by timestamp** to find errors around specific time
4. **Look for ERROR** followed by Traceback for full details
5. **Log file is auto-excluded from git** (in .gitignore)

## 📍 Current Status

✅ Server running at: http://127.0.0.1:5000  
✅ Logs written to: `graph_web_ui.log`  
✅ All endpoints have error logging  
✅ Debug mode enabled for detailed info  

## 🚀 Next Steps

1. Open `graph_web_ui.log` in your editor
2. Trigger an error in the UI
3. Check the log for detailed error info
4. Fix the error based on stack trace
5. Flask will auto-reload with the fix

---

**Full documentation**: See `LOGGING_GUIDE.md` for complete details
