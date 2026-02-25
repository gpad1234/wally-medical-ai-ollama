#!/bin/bash
# Clear QC Dashboard Test History

DB_PATH="/Users/gp/claude-code/startup-one/WALLY-CLEAN/test_results.db"

echo "QC Dashboard - Clear History"
echo "=============================="
echo ""
echo "Select option:"
echo "1) Clear ALL history"
echo "2) Keep last 10 runs"
echo "3) Keep last 20 runs"
echo "4) View history count"
echo "5) Cancel"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo "Clearing ALL history..."
        sqlite3 "$DB_PATH" << EOF
DELETE FROM test_results;
DELETE FROM test_suites;
DELETE FROM test_trends;
VACUUM;
EOF
        echo "✅ All history cleared!"
        ;;
    2)
        echo "Keeping last 10 runs..."
        sqlite3 "$DB_PATH" << EOF
DELETE FROM test_results WHERE suite_id IN (
  SELECT suite_id FROM test_suites 
  ORDER BY timestamp DESC 
  LIMIT -1 OFFSET 10
);
DELETE FROM test_suites WHERE suite_id NOT IN (
  SELECT suite_id FROM test_suites 
  ORDER BY timestamp DESC 
  LIMIT 10
);
VACUUM;
EOF
        echo "✅ Kept last 10 runs, older history cleared!"
        ;;
    3)
        echo "Keeping last 20 runs..."
        sqlite3 "$DB_PATH" << EOF
DELETE FROM test_results WHERE suite_id IN (
  SELECT suite_id FROM test_suites 
  ORDER BY timestamp DESC 
  LIMIT -1 OFFSET 20
);
DELETE FROM test_suites WHERE suite_id NOT IN (
  SELECT suite_id FROM test_suites 
  ORDER BY timestamp DESC 
  LIMIT 20
);
VACUUM;
EOF
        echo "✅ Kept last 20 runs, older history cleared!"
        ;;
    4)
        echo ""
        echo "Current History:"
        echo "----------------"
        sqlite3 "$DB_PATH" << EOF
.mode column
SELECT 
    COUNT(*) as total_runs,
    SUM(total_tests) as total_tests,
    SUM(passed) as total_passed,
    SUM(failed) as total_failed,
    ROUND(AVG(success_rate), 2) as avg_success_rate
FROM test_suites;
EOF
        echo ""
        echo "Recent Runs:"
        sqlite3 "$DB_PATH" << EOF
.mode column
.headers on
SELECT 
    SUBSTR(suite_id, 1, 30) as suite_id,
    total_tests,
    passed,
    failed,
    ROUND(success_rate, 1) as success_rate,
    datetime(timestamp, 'unixepoch', 'localtime') as timestamp
FROM test_suites
ORDER BY timestamp DESC
LIMIT 10;
EOF
        ;;
    5)
        echo "Cancelled."
        exit 0
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac
