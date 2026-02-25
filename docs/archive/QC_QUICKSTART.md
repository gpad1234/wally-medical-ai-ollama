# QC Dashboard Quick Start Guide

## 🚀 Quick Start

### 1. Start the QC Dashboard

```bash
# Make startup script executable
chmod +x start_qc.sh

# Start the dashboard
./start_qc.sh
```

Or manually:

```bash
python3 qc_dashboard.py
```

### 2. Access the Dashboard

Open your browser to: **http://localhost:5001**

### 3. Run Tests

Click any of the layer buttons:
- 🔬 **Test Core Layer** - Test C library functions
- 🔌 **Test Adapter Layer** - Test Python-C bindings
- ⚙️ **Test Service Layer** - Test business logic
- 🌐 **Test API Layer** - Test REST endpoints
- 🚀 **Run All Tests** - Full test suite

## 📊 Dashboard Features

### Real-Time Statistics
- Total tests executed
- Pass/fail counts
- Success rate percentage
- Visual progress bars

### Layer Status
- Current status of each architecture layer
- Latest test results
- Quick access to details

### Test History
- Complete history of test runs
- Filter by layer
- Success rate tracking
- Duration metrics

### Failing Tests
- List of currently failing tests
- Error messages
- Layer information
- Timestamps

## 🔧 Configuration

### Environment Variables

```bash
# Custom port
export QC_PORT=5002

# Enable debug mode
export QC_DEBUG=true
```

### Database Location

Test results are stored in:
- `test_results.db` - SQLite database
- `test_results/` - JSON reports

## 📦 Dependencies

The system automatically installs:
- Flask - Web framework
- Flask-CORS - Cross-origin support
- pytest - Testing framework
- pytest-json-report - JSON output
- pytest-cov - Coverage reporting

## 🔄 Automation

### Auto-Discovery of New Tests

The QC system automatically discovers:
1. Any new test files matching `test_*.py`
2. Tests in the correct layer directory
3. Tests with proper markers

**Example:**
```python
# tests/unit/test_services/test_my_new_service.py
import pytest

@pytest.mark.service
def test_my_new_feature():
    # Your test here
    assert True
```

The test will automatically appear in the next "Test Service Layer" run.

### Continuous Testing

Set up a cron job for automated testing:

```bash
# Edit crontab
crontab -e

# Add entry to run tests every hour
0 * * * * cd /path/to/WALLY-CLEAN && ./start_qc.sh --run-all

# Or test specific layer every 30 minutes
*/30 * * * * cd /path/to/WALLY-CLEAN && python3 -c "from src.services.test_runner_service import TestRunnerService; TestRunnerService().run_tests(layer='core')"
```

### Git Hook Integration

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run tests before commit

echo "Running QC tests..."
python3 -c "
from src.services.test_runner_service import TestRunnerService
runner = TestRunnerService()
result = runner.run_tests()
if result.failed > 0:
    print(f'❌ {result.failed} tests failing!')
    exit(1)
print(f'✅ All tests passed!')
"

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## 📱 API Usage

### Run Tests via API

```bash
# Run core tests
curl -X POST http://localhost:5001/api/qc/run-tests \
  -H "Content-Type: application/json" \
  -d '{"layer": "core"}'

# Get latest status
curl http://localhost:5001/api/qc/status

# Get test history
curl http://localhost:5001/api/qc/history?limit=10

# Get failing tests
curl http://localhost:5001/api/qc/failing-tests
```

### Python Integration

```python
from src.services.test_runner_service import TestRunnerService
from src.services.test_storage_service import TestStorageService

# Initialize
runner = TestRunnerService()
storage = TestStorageService()

# Run tests
result = runner.run_tests(layer='service', coverage=True)

# Check results
if result.failed == 0:
    print(f"✅ All {result.total_tests} tests passed!")
else:
    print(f"❌ {result.failed} tests failed")
    for test in result.test_results:
        if test.status == 'failed':
            print(f"  - {test.test_name}: {test.error_message}")

# Get trends
trends = storage.get_test_trends(layer='service', days=7)
print(f"Average success rate: {trends['average_success_rate']}%")
```

## 🎯 Best Practices

### 1. Test After Every Change
Run the relevant layer tests after making changes:
- Changed C code? → Test Core Layer
- Updated Python adapters? → Test Adapter Layer
- Modified services? → Test Service Layer

### 2. Monitor Trends
Check the dashboard daily for:
- Declining success rates
- Increasing test durations
- New failing tests

### 3. Fix Failures Immediately
Don't let failures accumulate:
- Review failing tests in the dashboard
- Fix or document as known issues
- Rerun to verify fixes

### 4. Use Coverage Reports
Enable coverage for new features:
```bash
curl -X POST http://localhost:5001/api/qc/run-tests \
  -d '{"layer": "service", "coverage": true}'
```

## 🐛 Troubleshooting

### Dashboard Won't Start

```bash
# Check Python version (needs 3.7+)
python3 --version

# Reinstall dependencies
pip3 install -r requirements.txt

# Check port availability
lsof -i :5001
```

### Tests Not Showing Up

```bash
# Verify test discovery
python3 -c "
from src.services.test_runner_service import TestRunnerService
runner = TestRunnerService()
print(runner.discover_tests())
"
```

### Database Errors

```bash
# Remove corrupted database
rm test_results.db

# Restart dashboard (will recreate)
./start_qc.sh
```

### Permission Issues

```bash
# Fix permissions
chmod +x start_qc.sh
chmod -R 755 test_results/
```

## 🎨 Customization

### Add Custom Test Layers

Edit `src/services/test_runner_service.py`:

```python
self.layers = {
    "core": {"path": "tests/unit/test_core", "marker": "core"},
    "adapter": {"path": "tests/unit/test_adapters", "marker": "adapter"},
    "service": {"path": "tests/unit/test_services", "marker": "service"},
    "api": {"path": "tests/unit/test_api", "marker": "api"},
    # Add your custom layer:
    "my_layer": {"path": "tests/unit/test_my_layer", "marker": "my_layer"},
}
```

Register marker in `pytest.ini`:

```ini
markers =
    my_layer: Tests for my custom layer
```

### Change Dashboard Theme

Edit `templates/qc_dashboard.html` CSS variables:

```css
:root {
    --bg-primary: #0f1419;
    --bg-secondary: #161b22;
    --text-primary: #c9d1d9;
    --accent-primary: #58a6ff;
    --success-color: #3fb950;
    --danger-color: #f85149;
}
```

## 📚 Further Reading

- [Full QC System Documentation](../docs/guides/QC_SYSTEM.md)
- [Testing Strategy](../TESTING_STRATEGY.md)
- [pytest Documentation](https://docs.pytest.org/)

## 💡 Tips

- **Keyboard shortcut**: Bookmark `http://localhost:5001` for quick access
- **Mobile access**: Dashboard is responsive, access from any device
- **Export data**: Use API endpoints to export results for reports
- **Integrate CI/CD**: Add QC checks to your deployment pipeline
- **Share results**: Send dashboard link to team members

---

**Need Help?**
Check the logs: `graph_web_ui.log` or open an issue on GitHub.
