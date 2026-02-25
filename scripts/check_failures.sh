#!/bin/bash
# QC Test Failure Inspector
# Quick script to identify and analyze failed tests

set -e

QC_API="http://localhost:5001/api/qc"

echo "🔍 QC Test Failure Inspector"
echo "=============================="
echo ""

# Function to display section header
section() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 1. Get Overall Status
section "📊 Overall Status"
curl -s "$QC_API/status" | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
layers = data.get('layers', {})
for layer, stats in layers.items():
    total = stats.get('total', 0)
    passed = stats.get('passed', 0)
    failed = stats.get('failed', 0)
    rate = stats.get('success_rate', 0)
    status = '✅' if failed == 0 else '❌'
    print(f'{status} {layer.upper():12s} | Total: {total:3d} | Passed: {passed:3d} | Failed: {failed:3d} | Rate: {rate:5.1f}%')
"

# 2. Get Currently Failing Tests
section "🔴 Currently Failing Tests"
curl -s "$QC_API/failing-tests?limit=20" | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
if not data:
    print('✅ No failing tests!')
else:
    for i, test in enumerate(data, 1):
        print(f\"\\n{i}. {test['name']}\")
        print(f\"   Layer: {test['layer']}\")
        print(f\"   Test ID: {test['test_id']}\")
        if test.get('error'):
            error = test['error'][:150] + '...' if len(test['error']) > 150 else test['error']
            print(f\"   Error: {error}\")
"

# 3. Get Latest Test Run with Failures
section "📋 Latest Test Run Details"
RUN_ID=$(curl -s "$QC_API/history?limit=10" | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
for run in data:
    if run['failed'] > 0:
        print(run['run_id'])
        break
" 2>/dev/null)

if [ -n "$RUN_ID" ]; then
    echo "Run ID: $RUN_ID"
    echo ""
    
    curl -s "$QC_API/run/$RUN_ID" | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
tests = data.get('tests', [])
failed = [t for t in tests if t['status'] == 'failed']

print(f\"Total: {data['total']} | Passed: {data['passed']} | Failed: {data['failed']} | Skipped: {data['skipped']}\")
print(f\"Duration: {data['duration']:.2f}s | Success Rate: {data['success_rate']:.1f}%\")
print(f\"\\nFailed Tests ({len(failed)}):\")
print('=' * 80)

for i, test in enumerate(failed, 1):
    print(f\"\\n{i}. {test['name']}\")
    print(f\"   File: {test['test_id'].split('::')[0]}\")
    print(f\"   Layer: {test['layer']}\")
    print(f\"   Duration: {test['duration']:.3f}s\")
    if test.get('error'):
        # Show first 300 chars of error
        error = test['error'][:300] + '...' if len(test['error']) > 300 else test['error']
        print(f\"   Error:\\n   {error.replace(chr(10), chr(10) + '   ')}\")
"
else
    echo "✅ No failed test runs found in recent history!"
fi

# 4. Summary and Actions
section "💡 Next Steps"
echo "
To fix failing tests:
  1. Review the error messages above
  2. Check the test file location
  3. Run the specific test: pytest <test_file>::<test_name> -v
  4. Fix the issue in the source code
  5. Re-run tests via dashboard or API

To run tests again:
  curl -X POST http://localhost:5001/api/qc/run-tests \\
    -H 'Content-Type: application/json' \\
    -d '{\"layer\": \"service\"}'

To view in browser:
  open http://localhost:5001
"
