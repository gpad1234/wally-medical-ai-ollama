# QC Dashboard - Testing Automation System

## ✨ Overview

A comprehensive **Quality Control Dashboard** that provides automated testing with persistent result storage, real-time monitoring, and historical trend analysis for the WALLY-CLEAN project.

## 🎯 Key Features

### 1. **Automated Test Execution**
- One-click testing by architectural layer
- Full test suite execution
- Automated test discovery for new functionality
- No manual test running required

### 2. **Persistent Result Storage**
- SQLite database for reliability
- Complete test history tracking
- Individual test result storage
- Automatic cleanup of old data

### 3. **Real-Time Monitoring**
- Live success rate tracking
- Test duration metrics
- Failure detection and alerts
- Layer-by-layer status

### 4. **Interactive Web Dashboard**
- Modern, responsive UI
- Visual statistics and charts
- Historical trend analysis
- Failing test tracking
- Filter and search capabilities

### 5. **CI/CD Ready**
- REST API for automation
- Programmatic test execution
- Git hook integration
- Cron job support

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the dashboard
./start_qc.sh

# 3. Open browser
open http://localhost:5001
```

## 📁 Files Created

### Core Services
- **[src/services/test_execution_service.py](src/services/test_execution_service.py)** - Executes pytest programmatically
- **[src/services/test_storage_service.py](src/services/test_storage_service.py)** - Persists results using SimpleDB
- **[src/services/test_runner_service.py](src/services/test_runner_service.py)** - SQLite-based test management

### Web Application
- **[qc_dashboard.py](qc_dashboard.py)** - Flask REST API server
- **[templates/qc_dashboard.html](templates/qc_dashboard.html)** - Interactive web UI

### Documentation
- **[QC_QUICKSTART.md](QC_QUICKSTART.md)** - Quick start guide
- **[docs/guides/QC_SYSTEM.md](docs/guides/QC_SYSTEM.md)** - Complete documentation

### Scripts
- **[start_qc.sh](start_qc.sh)** - Startup script

## 🏗️ Architecture

```
┌──────────────────────────────────────────────┐
│         Web Dashboard (Port 5001)            │
│  ┌────────────┐  ┌────────────┐             │
│  │  Test Run  │  │   History  │             │
│  │  Controls  │  │  & Trends  │             │
│  └────────────┘  └────────────┘             │
└──────────────────┬───────────────────────────┘
                   │ REST API
        ┌──────────┴──────────┐
        │                     │
┌───────▼──────────┐  ┌──────▼────────────┐
│  Test Execution  │  │  Test Storage     │
│     Service      │  │     Service       │
│                  │  │                   │
│ • Run pytest     │  │ • SQLite DB       │
│ • Parse results  │  │ • History         │
│ • Layer routing  │  │ • Trends          │
└───────┬──────────┘  └──────┬────────────┘
        │                    │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │   Pytest Tests     │
        │                    │
        │ • Core Layer       │
        │ • Adapter Layer    │
        │ • Service Layer    │
        │ • API Layer        │
        └────────────────────┘
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/qc/status` | GET | Overall QC status |
| `/api/qc/run-tests` | POST | Execute tests |
| `/api/qc/history` | GET | Test run history |
| `/api/qc/run/<id>` | GET | Run details |
| `/api/qc/trends` | GET | Statistical trends |
| `/api/qc/failing-tests` | GET | Current failures |
| `/api/qc/layers` | GET | Available layers |

## 💻 Usage Examples

### Web Interface
```bash
./start_qc.sh
# Click "Test Core Layer" button
```

### Command Line
```bash
# Run core tests
curl -X POST http://localhost:5001/api/qc/run-tests \
  -H "Content-Type: application/json" \
  -d '{"layer": "core"}'
```

### Python API
```python
from src.services.test_runner_service import TestRunnerService

runner = TestRunnerService()
result = runner.run_tests(layer='service')

print(f"Passed: {result.passed}/{result.total_tests}")
print(f"Success Rate: {result.success_rate}%")
```

## 🤖 Automation Features

### 1. **Auto-Discovery**
Automatically finds and registers:
- New test files (`test_*.py`)
- Tests in correct directories
- Proper layer markers

### 2. **Scheduled Testing**
```bash
# Cron job - test every hour
0 * * * * cd /path/to/WALLY-CLEAN && ./start_qc.sh --run-all
```

### 3. **Git Hooks**
```bash
# Pre-commit hook
python3 -c "from src.services.test_runner_service import TestRunnerService; \
            runner = TestRunnerService(); \
            result = runner.run_tests(); \
            exit(0 if result.failed == 0 else 1)"
```

## 📊 Dashboard Features

### Statistics Dashboard
- **Total Tests** - Count of all tests
- **Passed Tests** - Successful executions
- **Failed Tests** - Failures requiring attention
- **Success Rate** - Percentage with visual progress bar

### Layer Status Table
- Current status per layer
- Latest test counts
- Success rates
- Last run timestamps
- Quick access to details

### Test History
- Complete execution history
- Filter by layer
- Sort by date/status
- View detailed results
- Track trends over time

### Failing Tests Monitor
- List of current failures
- Error messages
- Layer identification
- Timestamps
- Quick navigation to fixes

## 🎨 UI Features

- **Dark Theme** - Easy on the eyes
- **Responsive Design** - Works on all devices
- **Real-Time Updates** - Auto-refresh every 30s
- **Visual Indicators** - Color-coded status
- **Progress Bars** - Success rate visualization
- **Smooth Animations** - Professional feel

## 📈 Benefits

1. **Zero Manual Testing** - All tests run automatically
2. **Historical Tracking** - Never lose test results
3. **Trend Analysis** - Spot quality degradation early
4. **Quick Debugging** - Instant access to errors
5. **Team Visibility** - Share dashboard URL
6. **CI/CD Integration** - Seamless automation
7. **Quality Metrics** - Data-driven decisions

## 🔍 Monitoring Capabilities

### Real-Time
- Currently running tests
- Success/failure counts
- Test duration
- Layer status

### Historical
- Success rate trends
- Test count growth
- Duration patterns
- Failure frequency

### Alerts
- Failing test notifications
- Success rate drops
- Duration spikes
- New test discovery

## 🛠️ Configuration

### Environment Variables
```bash
export QC_PORT=5001          # Dashboard port
export QC_DEBUG=false        # Debug mode
export PYTHONPATH=$(pwd)     # Python path
```

### Database Configuration
- **Location**: `test_results.db`
- **Type**: SQLite3
- **Auto-cleanup**: 90 days retention
- **Backup**: Manual copy recommended

### Test Discovery Paths
```python
{
    "core": "tests/unit/test_core",
    "adapter": "tests/unit/test_adapters",
    "service": "tests/unit/test_services",
    "api": "tests/unit/test_api"
}
```

## 📚 Documentation

- **[QC_QUICKSTART.md](QC_QUICKSTART.md)** - Get started quickly
- **[docs/guides/QC_SYSTEM.md](docs/guides/QC_SYSTEM.md)** - Complete system guide
- **[TESTING_STRATEGY.md](TESTING_STRATEGY.md)** - Overall testing strategy

## 🚦 Status Indicators

| Color | Status | Meaning |
|-------|--------|---------|
| 🟢 Green | Passed | All tests successful |
| 🔴 Red | Failed | Some tests failed |
| 🟡 Yellow | Skipped | Tests were skipped |
| 🔵 Blue | Running | Tests in progress |

## 🎓 Best Practices

1. **Run Before Commits** - Ensure quality
2. **Monitor Daily** - Check dashboard
3. **Fix Failures Fast** - Don't accumulate debt
4. **Track Trends** - Watch success rates
5. **Document Issues** - Known failures
6. **Automate Everything** - Set up CI/CD

## 🔐 Security

- Runs on localhost by default
- No authentication required (local use)
- Database stored locally
- No external data transmission
- Safe for sensitive projects

## 🌟 Future Enhancements

- [ ] WebSocket real-time updates
- [ ] Email/Slack notifications
- [ ] Flaky test detection
- [ ] Performance regression alerts
- [ ] Code coverage visualization
- [ ] Test comparison tool
- [ ] Mobile app
- [ ] Multi-project support

## 🤝 Contributing

To add new test layers:
1. Add tests to `tests/unit/test_<layer>/`
2. Add marker to `pytest.ini`
3. Update `test_runner_service.py` layers dict
4. Tests auto-discovered on next run

## 📞 Support

- Check logs: `graph_web_ui.log`
- Review documentation: `docs/guides/QC_SYSTEM.md`
- Test discovery: Run with verbose flag
- Database issues: Delete `test_results.db` and restart

---

**Start testing smarter, not harder! 🚀**
