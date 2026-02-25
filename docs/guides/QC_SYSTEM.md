# Quality Control System Documentation

## Overview

The QC system provides automated testing with persistent result storage and comprehensive analytics.

## Architecture

```
┌─────────────────────────────────────────┐
│         QC Dashboard (Web UI)           │
│  - Test Execution Controls              │
│  - Real-time Status                     │
│  - Historical Trends                    │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
┌───────▼─────────┐  ┌──────▼──────────┐
│ Test Execution  │  │  Test Storage   │
│    Service      │  │    Service      │
│                 │  │                 │
│ - Run pytest    │  │ - SQLite DB     │
│ - Parse results │  │ - History       │
│ - Layer routing │  │ - Analytics     │
└───────┬─────────┘  └──────┬──────────┘
        │                   │
        │    ┌──────────────┘
        │    │
┌───────▼────▼─────────────────────┐
│        Test Suite                │
│  - Unit Tests (by layer)         │
│  - Integration Tests             │
│  - Performance Tests             │
└──────────────────────────────────┘
```

## Components

### 1. Test Execution Service
**File:** `src/services/test_execution_service.py`

Programmatically runs pytest tests and captures detailed results:
- Executes tests by layer, path, or full suite
- Captures test outcomes, durations, and errors
- Generates JSON reports
- Stores results to filesystem

### 2. Test Storage Service
**File:** `src/services/test_storage_service.py`

Persists test results using SimpleDB:
- Stores test run summaries
- Tracks individual test results
- Maintains test history
- Calculates statistics and trends

### 3. Test Runner Service
**File:** `src/services/test_runner_service.py`

Alternative implementation using SQLite for more robust storage:
- SQLite-based persistent storage
- Comprehensive test discovery
- Trend analysis
- Coverage tracking

### 4. QC Dashboard API
**File:** `qc_dashboard.py`

Flask REST API serving the QC web interface:
- `/api/qc/status` - Overall QC status
- `/api/qc/run-tests` - Execute tests (POST)
- `/api/qc/history` - Test run history
- `/api/qc/run/<run_id>` - Detailed results
- `/api/qc/trends` - Statistical trends
- `/api/qc/failing-tests` - Currently failing tests

### 5. Web UI
**File:** `templates/qc_dashboard.html`

Interactive dashboard providing:
- One-click test execution by layer
- Real-time test status
- Success rate visualization
- Layer-by-layer status
- Test history with filtering
- Failing test tracking

## Usage

### Starting the QC Dashboard

```bash
# Basic startup
python qc_dashboard.py

# Custom port
QC_PORT=5002 python qc_dashboard.py

# Debug mode
QC_DEBUG=true python qc_dashboard.py
```

Access the dashboard at: http://localhost:5001

### Running Tests via API

```bash
# Run core layer tests
curl -X POST http://localhost:5001/api/qc/run-tests \
  -H "Content-Type: application/json" \
  -d '{"layer": "core", "verbose": true}'

# Run all tests
curl -X POST http://localhost:5001/api/qc/run-tests \
  -H "Content-Type: application/json" \
  -d '{"layer": "all"}'

# Run specific test file
curl -X POST http://localhost:5001/api/qc/run-tests \
  -H "Content-Type: application/json" \
  -d '{"test_path": "tests/unit/test_services/test_graph_service.py"}'
```

### Programmatic Usage

```python
from src.services.test_execution_service import TestExecutionService
from src.services.test_storage_service import TestStorageService

# Initialize services
executor = TestExecutionService()
storage = TestStorageService()

# Run tests
result = executor.run_tests_by_layer('core', verbose=True)

# Store results
storage.store_test_run(result)

# Query history
history = storage.get_test_history(limit=10, layer='core')

# Get trends
trends = storage.get_test_trends(layer='service', days=30)
```

## Database Schema

### SimpleDB Storage (Key-Value)

```
run:{run_id}                  -> Complete test run JSON
run_index:{timestamp}         -> run_id
layer:{layer}:latest          -> Latest run_id for layer
stats:total_runs              -> Total run count
test:{run_id}:{test_id}       -> Individual test result
```

### SQLite Storage (Relational)

```sql
-- Test suites
CREATE TABLE test_suites (
    suite_id TEXT PRIMARY KEY,
    suite_name TEXT,
    total_tests INTEGER,
    passed INTEGER,
    failed INTEGER,
    skipped INTEGER,
    errors INTEGER,
    duration REAL,
    coverage REAL,
    timestamp TEXT
);

-- Test results
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY,
    suite_id TEXT,
    test_id TEXT,
    test_name TEXT,
    test_file TEXT,
    layer TEXT,
    status TEXT,
    duration REAL,
    error_message TEXT,
    timestamp TEXT
);

-- Test trends
CREATE TABLE test_trends (
    id INTEGER PRIMARY KEY,
    date TEXT,
    layer TEXT,
    total_tests INTEGER,
    pass_rate REAL,
    avg_duration REAL
);
```

## Test Automation

### Automatic Test Discovery

The system automatically discovers tests based on:
- Directory structure (`tests/unit/test_*`)
- Layer markers (`@pytest.mark.core`, etc.)
- File naming (`test_*.py`)

### Scheduled Testing

Set up cron jobs for automated testing:

```bash
# Test all layers every hour
0 * * * * cd /path/to/wally && python -c "from src.services.test_runner_service import TestRunnerService; TestRunnerService().run_tests()"

# Test core layer every 15 minutes
*/15 * * * * cd /path/to/wally && python -c "from src.services.test_runner_service import TestRunnerService; TestRunnerService().run_tests(layer='core')"
```

### CI/CD Integration

```yaml
# .github/workflows/qc.yml
name: Quality Control

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run QC Tests
        run: |
          python -c "
          from src.services.test_runner_service import TestRunnerService
          runner = TestRunnerService()
          result = runner.run_tests(coverage=True)
          print(f'Tests: {result.passed}/{result.total_tests} passed')
          exit(0 if result.failed == 0 else 1)
          "
```

## API Response Examples

### Test Run Result

```json
{
  "success": true,
  "data": {
    "run_id": "core_20260211_143022",
    "total": 45,
    "passed": 43,
    "failed": 2,
    "skipped": 0,
    "duration": 2.34,
    "success_rate": 95.6
  }
}
```

### Test History

```json
{
  "success": true,
  "data": [
    {
      "run_id": "all_20260211_143500",
      "timestamp": "2026-02-11T14:35:00",
      "layer": "all",
      "total": 120,
      "passed": 115,
      "failed": 5,
      "skipped": 0,
      "duration": 8.42,
      "success_rate": 95.8
    }
  ]
}
```

### Trends

```json
{
  "success": true,
  "data": {
    "total_runs": 156,
    "total_tests_executed": 18720,
    "total_passed": 17893,
    "total_failed": 827,
    "average_success_rate": 95.58,
    "average_duration": 6.23,
    "history_days": 7,
    "layer": "core"
  }
}
```

## Best Practices

1. **Run tests before commits**
   ```bash
   python -c "from src.services.test_runner_service import TestRunnerService; TestRunnerService().run_tests()" && git commit -m "..."
   ```

2. **Monitor failing tests daily**
   - Check QC dashboard for red indicators
   - Review error messages
   - Fix or document known failures

3. **Track success rate trends**
   - Aim for >95% success rate
   - Investigate sudden drops
   - Celebrate improvements

4. **Use layer-by-layer testing during development**
   - Test changed layer immediately
   - Run full suite before merge

5. **Archive old results**
   ```python
   storage.cleanup_old_data(days=90)
   ```

## Troubleshooting

### Tests not discovered
- Check `pytest.ini` configuration
- Verify test file naming (`test_*.py`)
- Ensure markers are registered

### Database errors
- Check database file permissions
- Verify SimpleDB initialization
- Check disk space

### UI not loading
- Verify Flask is running on correct port
- Check browser console for errors
- Ensure CORS is enabled

### Slow test execution
- Review test fixtures
- Check for unnecessary waits
- Consider parallel execution

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Test coverage visualization
- [ ] Flaky test detection
- [ ] Performance regression detection
- [ ] Email/Slack notifications
- [ ] Test result comparison
- [ ] CI/CD integration hooks
- [ ] Advanced filtering and search
- [ ] Export to CSV/PDF
- [ ] Mobile-responsive UI
