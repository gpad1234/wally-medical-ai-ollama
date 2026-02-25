"""
Test Runner Service

Executes pytest tests programmatically and stores results persistently.
Provides automated test discovery and execution for QC GUI.
"""

import subprocess
import json
import pytest
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import sqlite3
from enum import Enum


class TestStatus(Enum):
    """Test execution status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestResult:
    """Single test result"""
    test_id: str
    test_name: str
    test_file: str
    layer: str
    status: str
    duration: float
    error_message: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class TestSuite:
    """Test suite execution summary"""
    suite_id: str
    suite_name: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    timestamp: str
    coverage: Optional[float] = None


class TestResultsDB:
    """Persistent storage for test results using SQLite"""
    
    def __init__(self, db_path: str = "test_results.db"):
        """Initialize test results database"""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Create database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Test suites table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_suites (
                    suite_id TEXT PRIMARY KEY,
                    suite_name TEXT NOT NULL,
                    total_tests INTEGER,
                    passed INTEGER,
                    failed INTEGER,
                    skipped INTEGER,
                    errors INTEGER,
                    duration REAL,
                    coverage REAL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            # Test results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    suite_id TEXT NOT NULL,
                    test_id TEXT NOT NULL,
                    test_name TEXT NOT NULL,
                    test_file TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    status TEXT NOT NULL,
                    duration REAL,
                    error_message TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (suite_id) REFERENCES test_suites(suite_id)
                )
            """)
            
            # Test history index
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_test_history
                ON test_results(test_id, timestamp)
            """)
            
            # Test trends table (aggregated statistics)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_trends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    total_tests INTEGER,
                    pass_rate REAL,
                    avg_duration REAL,
                    UNIQUE(date, layer)
                )
            """)
            
            conn.commit()
    
    def save_suite(self, suite: TestSuite):
        """Save test suite execution"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO test_suites
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                suite.suite_id,
                suite.suite_name,
                suite.total_tests,
                suite.passed,
                suite.failed,
                suite.skipped,
                suite.errors,
                suite.duration,
                suite.coverage,
                suite.timestamp
            ))
            conn.commit()
    
    def save_results(self, suite_id: str, results: List[TestResult]):
        """Save test results"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for result in results:
                cursor.execute("""
                    INSERT INTO test_results
                    (suite_id, test_id, test_name, test_file, layer, status, 
                     duration, error_message, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    suite_id,
                    result.test_id,
                    result.test_name,
                    result.test_file,
                    result.layer,
                    result.status,
                    result.duration,
                    result.error_message,
                    result.timestamp
                ))
            conn.commit()
    
    def get_latest_suite(self) -> Optional[Dict]:
        """Get latest test suite execution"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM test_suites
                ORDER BY timestamp DESC LIMIT 1
            """)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_suite_results(self, suite_id: str) -> List[Dict]:
        """Get all test results for a suite"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM test_results
                WHERE suite_id = ?
                ORDER BY layer, test_name
            """, (suite_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_test_history(self, test_id: str, limit: int = 10) -> List[Dict]:
        """Get historical results for a specific test"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM test_results
                WHERE test_id = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (test_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_layer_stats(self, layer: str, days: int = 30) -> Dict:
        """Get statistics for a specific layer"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    AVG(duration) as avg_duration
                FROM test_results
                WHERE layer = ? 
                AND timestamp >= datetime('now', '-' || ? || ' days')
            """, (layer, days))
            return dict(cursor.fetchone())
    
    def get_all_suites(self, limit: int = 50) -> List[Dict]:
        """Get all test suite executions"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM test_suites
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_trends(self, layer: Optional[str] = None, days: int = 30) -> List[Dict]:
        """Get test trends over time"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if layer:
                cursor.execute("""
                    SELECT 
                        DATE(timestamp) as date,
                        layer,
                        COUNT(*) as total_tests,
                        ROUND(AVG(CASE WHEN status = 'passed' THEN 100.0 ELSE 0 END), 2) as pass_rate,
                        ROUND(AVG(duration), 4) as avg_duration
                    FROM test_results
                    WHERE layer = ? 
                    AND timestamp >= datetime('now', '-' || ? || ' days')
                    GROUP BY DATE(timestamp), layer
                    ORDER BY date DESC
                """, (layer, days))
            else:
                cursor.execute("""
                    SELECT 
                        DATE(timestamp) as date,
                        layer,
                        COUNT(*) as total_tests,
                        ROUND(AVG(CASE WHEN status = 'passed' THEN 100.0 ELSE 0 END), 2) as pass_rate,
                        ROUND(AVG(duration), 4) as avg_duration
                    FROM test_results
                    WHERE timestamp >= datetime('now', '-' || ? || ' days')
                    GROUP BY DATE(timestamp), layer
                    ORDER BY date DESC, layer
                """, (days,))
            
            return [dict(row) for row in cursor.fetchall()]


class TestRunnerService:
    """Service for executing and managing tests"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize test runner service
        
        Args:
            project_root: Project root directory (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self.tests_dir = self.project_root / "tests"
        self.db = TestResultsDB()
        
        # Layer definitions
        self.layers = {
            "core": {"path": "tests/unit/test_core", "marker": "core"},
            "adapter": {"path": "tests/unit/test_adapters", "marker": "adapter"},
            "service": {"path": "tests/unit/test_services", "marker": "service"},
            "api": {"path": "tests/unit/test_api", "marker": "api"},
            "integration": {"path": "tests/integration", "marker": "integration"},
            "performance": {"path": "tests/performance", "marker": "performance"},
        }
    
    def discover_tests(self, layer: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Discover all tests
        
        Args:
            layer: Specific layer to discover (None for all)
            
        Returns:
            Dictionary mapping layers to test files
        """
        discovered = {}
        
        if layer:
            layers_to_check = {layer: self.layers[layer]}
        else:
            layers_to_check = self.layers
        
        for layer_name, layer_info in layers_to_check.items():
            test_path = self.project_root / layer_info["path"]
            if test_path.exists():
                test_files = list(test_path.rglob("test_*.py"))
                discovered[layer_name] = [str(f.relative_to(self.project_root)) 
                                         for f in test_files]
        
        return discovered
    
    def run_tests(
        self,
        layer: Optional[str] = None,
        test_file: Optional[str] = None,
        coverage: bool = False
    ) -> TestSuite:
        """
        Run tests and store results
        
        Args:
            layer: Specific layer to test (None for all)
            test_file: Specific test file (overrides layer)
            coverage: Whether to collect coverage data
            
        Returns:
            TestSuite with execution summary
        """
        import uuid
        
        # Generate suite ID
        suite_id = f"suite_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Determine what to run
        if test_file:
            suite_name = f"File: {test_file}"
            args = [test_file]
        elif layer:
            suite_name = f"Layer: {layer}"
            args = ["-m", self.layers[layer]["marker"]]
        else:
            suite_name = "All Tests"
            args = ["tests/"]
        
        # Create custom plugin to capture results
        class ResultCollector:
            def __init__(self):
                self.results = []
            
            def pytest_runtest_logreport(self, report):
                if report.when == 'call' or (report.when == 'setup' and report.outcome == 'skipped'):
                    result = {
                        'nodeid': report.nodeid,
                        'outcome': report.outcome,
                        'duration': report.duration,
                        'longrepr': str(report.longrepr) if report.longrepr else None
                    }
                    self.results.append(result)
        
        collector = ResultCollector()
        
        # Build pytest args (without json-report plugin)
        pytest_args = [
            "-v",
            "--tb=short",
        ] + args
        
        if coverage:
            pytest_args.extend([
                "--cov=src",
                "--cov-report=json:.coverage.json"
            ])
        
        # Run tests
        start_time = datetime.now()
        result_code = pytest.main(pytest_args, plugins=[collector])
        duration = (datetime.now() - start_time).total_seconds()
        
        # Parse results from collector
        test_results = self._parse_collected_results(collector.results, layer or "all")
        
        # Calculate summary
        passed = sum(1 for r in test_results if r.status == "passed")
        failed = sum(1 for r in test_results if r.status == "failed")
        skipped = sum(1 for r in test_results if r.status == "skipped")
        errors = sum(1 for r in test_results if r.status == "error")
        
        # Get coverage if available
        coverage_pct = None
        if coverage:
            coverage_file = self.project_root / ".coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    cov_data = json.load(f)
                    coverage_pct = cov_data.get("totals", {}).get("percent_covered")
        
        # Create suite summary
        suite = TestSuite(
            suite_id=suite_id,
            suite_name=suite_name,
            total_tests=len(test_results),
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            timestamp=datetime.now().isoformat(),
            coverage=coverage_pct
        )
        
        # Save to database
        self.db.save_suite(suite)
        self.db.save_results(suite_id, test_results)
        
        return suite
    
    def _parse_collected_results(self, results: List[Dict], layer: str) -> List[TestResult]:
        """Parse collected pytest results"""
        test_results = []
        
        for test in results:
            # Extract test info
            nodeid = test.get("nodeid", "")
            test_file = nodeid.split("::")[0] if "::" in nodeid else nodeid
            test_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
            
            # Determine layer from test file path
            test_layer = layer
            if "test_core" in test_file:
                test_layer = "core"
            elif "test_adapters" in test_file:
                test_layer = "adapter"
            elif "test_services" in test_file:
                test_layer = "service"
            elif "test_api" in test_file:
                test_layer = "api"
            elif "integration" in test_file:
                test_layer = "integration"
            elif "performance" in test_file:
                test_layer = "performance"
            
            # Get status
            outcome = test.get("outcome", "unknown")
            status = outcome if outcome in ["passed", "failed", "skipped"] else "error"
            
            # Get error message if failed
            error_msg = None
            if status in ["failed", "error"]:
                error_msg = test.get("longrepr")
                if error_msg and len(error_msg) > 500:
                    error_msg = error_msg[:500] + "..."
            
            test_results.append(TestResult(
                test_id=nodeid,
                test_name=test_name,
                test_file=test_file,
                layer=test_layer,
                status=status,
                duration=test.get("duration", 0.0),
                error_message=error_msg
            ))
        
        return test_results
    
    def _parse_results(self, results_file: Path, layer: str) -> List[TestResult]:
        """Parse pytest JSON report"""
        if not results_file.exists():
            return []
        
        with open(results_file) as f:
            data = json.load(f)
        
        test_results = []
        
        for test in data.get("tests", []):
            # Extract test info
            nodeid = test.get("nodeid", "")
            test_file = nodeid.split("::")[0] if "::" in nodeid else nodeid
            test_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
            
            # Determine layer from test file path
            test_layer = layer
            if "test_core" in test_file:
                test_layer = "core"
            elif "test_adapters" in test_file:
                test_layer = "adapter"
            elif "test_services" in test_file:
                test_layer = "service"
            elif "test_api" in test_file:
                test_layer = "api"
            elif "integration" in test_file:
                test_layer = "integration"
            elif "performance" in test_file:
                test_layer = "performance"
            
            # Get status
            outcome = test.get("outcome", "unknown")
            status = outcome if outcome in ["passed", "failed", "skipped"] else "error"
            
            # Get error message if failed
            error_msg = None
            if status == "failed":
                call = test.get("call", {})
                error_msg = call.get("longrepr", "Unknown error")
            
            test_results.append(TestResult(
                test_id=nodeid,
                test_name=test_name,
                test_file=test_file,
                layer=test_layer,
                status=status,
                duration=test.get("duration", 0.0),
                error_message=error_msg
            ))
        
        return test_results
    
    def get_latest_results(self) -> Optional[Dict]:
        """Get latest test execution results"""
        suite = self.db.get_latest_suite()
        if not suite:
            return None
        
        results = self.db.get_suite_results(suite["suite_id"])
        return {
            "suite": suite,
            "results": results
        }
    
    def get_test_history(self, test_id: str, limit: int = 10) -> List[Dict]:
        """Get historical results for a test"""
        return self.db.get_test_history(test_id, limit)
    
    def get_dashboard_data(self) -> Dict:
        """Get comprehensive dashboard data"""
        latest_suite = self.db.get_latest_suite()
        all_suites = self.db.get_all_suites(limit=10)
        trends = self.db.get_trends(days=30)
        
        # Calculate layer statistics
        layer_stats = {}
        for layer_name in self.layers.keys():
            layer_stats[layer_name] = self.db.get_layer_stats(layer_name)
        
        return {
            "latest_suite": latest_suite,
            "recent_suites": all_suites,
            "trends": trends,
            "layer_stats": layer_stats,
            "layers": list(self.layers.keys())
        }
