"""
Test Execution Service

Programmatically runs pytest tests and captures results.
"""

import pytest
import json
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class TestResult:
    """Single test result"""
    test_id: str
    name: str
    status: str  # passed, failed, skipped, error
    duration: float
    error_message: Optional[str] = None
    layer: Optional[str] = None
    markers: List[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.markers is None:
            self.markers = []


@dataclass
class TestRunResult:
    """Complete test run result"""
    run_id: str
    timestamp: str
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    layer: Optional[str] = None
    test_results: List[TestResult] = None
    
    def __post_init__(self):
        if self.test_results is None:
            self.test_results = []
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100


class TestExecutionService:
    """
    Service for executing tests and capturing results
    """
    
    def __init__(self, workspace_root: str = None):
        """
        Initialize test execution service
        
        Args:
            workspace_root: Root directory of the workspace (defaults to current dir)
        """
        self.workspace_root = workspace_root or os.getcwd()
        self.results_dir = os.path.join(self.workspace_root, "test_results")
        os.makedirs(self.results_dir, exist_ok=True)
    
    def run_tests_by_layer(self, layer: str, verbose: bool = False) -> TestRunResult:
        """
        Run tests for a specific layer
        
        Args:
            layer: Layer to test (core, adapter, service, api)
            verbose: Enable verbose output
            
        Returns:
            TestRunResult with execution results
        """
        run_id = f"{layer}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Build pytest command
        marker = f"-m {layer}"
        pytest_args = [
            marker,
            "-v" if verbose else "",
            "--tb=short",
            f"--json-report",
            f"--json-report-file={self.results_dir}/{run_id}.json",
            "--json-report-indent=2"
        ]
        pytest_args = [arg for arg in pytest_args if arg]  # Remove empty strings
        
        # Run pytest
        start_time = datetime.utcnow()
        exit_code = pytest.main(pytest_args)
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        # Parse results
        result = self._parse_json_report(run_id, layer, duration)
        
        # Save summary
        self._save_summary(result)
        
        return result
    
    def run_tests_by_path(self, test_path: str, verbose: bool = False) -> TestRunResult:
        """
        Run tests from a specific path
        
        Args:
            test_path: Path to test file or directory
            verbose: Enable verbose output
            
        Returns:
            TestRunResult with execution results
        """
        run_id = f"path_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        pytest_args = [
            test_path,
            "-v" if verbose else "",
            "--tb=short",
            f"--json-report",
            f"--json-report-file={self.results_dir}/{run_id}.json",
            "--json-report-indent=2"
        ]
        pytest_args = [arg for arg in pytest_args if arg]
        
        start_time = datetime.utcnow()
        exit_code = pytest.main(pytest_args)
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        result = self._parse_json_report(run_id, None, duration)
        self._save_summary(result)
        
        return result
    
    def run_all_tests(self, verbose: bool = False) -> TestRunResult:
        """
        Run all tests in the test suite
        
        Args:
            verbose: Enable verbose output
            
        Returns:
            TestRunResult with execution results
        """
        run_id = f"all_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        pytest_args = [
            "tests/",
            "-v" if verbose else "",
            "--tb=short",
            f"--json-report",
            f"--json-report-file={self.results_dir}/{run_id}.json",
            "--json-report-indent=2"
        ]
        pytest_args = [arg for arg in pytest_args if arg]
        
        start_time = datetime.utcnow()
        exit_code = pytest.main(pytest_args)
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        result = self._parse_json_report(run_id, "all", duration)
        self._save_summary(result)
        
        return result
    
    def _parse_json_report(self, run_id: str, layer: Optional[str], duration: float) -> TestRunResult:
        """Parse pytest JSON report"""
        report_path = os.path.join(self.results_dir, f"{run_id}.json")
        
        if not os.path.exists(report_path):
            # Fallback if JSON report plugin not available
            return TestRunResult(
                run_id=run_id,
                timestamp=datetime.utcnow().isoformat(),
                total=0,
                passed=0,
                failed=0,
                skipped=0,
                errors=0,
                duration=duration,
                layer=layer,
                test_results=[]
            )
        
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        # Parse summary
        summary = data.get('summary', {})
        
        # Parse individual tests
        test_results = []
        for test in data.get('tests', []):
            test_result = TestResult(
                test_id=test.get('nodeid', ''),
                name=test.get('nodeid', '').split('::')[-1],
                status=test.get('outcome', 'unknown'),
                duration=test.get('duration', 0.0),
                error_message=self._extract_error_message(test),
                layer=layer,
                markers=[m for m in test.get('keywords', []) if not m.startswith('test_')],
                timestamp=datetime.utcnow().isoformat()
            )
            test_results.append(test_result)
        
        return TestRunResult(
            run_id=run_id,
            timestamp=datetime.utcnow().isoformat(),
            total=summary.get('total', 0),
            passed=summary.get('passed', 0),
            failed=summary.get('failed', 0),
            skipped=summary.get('skipped', 0),
            errors=summary.get('error', 0),
            duration=duration,
            layer=layer,
            test_results=test_results
        )
    
    def _extract_error_message(self, test_data: Dict) -> Optional[str]:
        """Extract error message from test data"""
        call = test_data.get('call', {})
        if 'longrepr' in call:
            return call['longrepr']
        
        setup = test_data.get('setup', {})
        if 'longrepr' in setup:
            return setup['longrepr']
        
        return None
    
    def _save_summary(self, result: TestRunResult):
        """Save test run summary"""
        summary_path = os.path.join(self.results_dir, f"{result.run_id}_summary.json")
        
        with open(summary_path, 'w') as f:
            json.dump(asdict(result), f, indent=2)
    
    def get_test_history(self, limit: int = 50) -> List[TestRunResult]:
        """
        Get test run history
        
        Args:
            limit: Maximum number of runs to return
            
        Returns:
            List of TestRunResult objects
        """
        summaries = []
        
        # Find all summary files
        for filename in sorted(os.listdir(self.results_dir), reverse=True):
            if filename.endswith('_summary.json'):
                filepath = os.path.join(self.results_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Convert dict back to TestRunResult
                    test_results = [TestResult(**tr) for tr in data.get('test_results', [])]
                    data['test_results'] = test_results
                    summaries.append(TestRunResult(**data))
                
                if len(summaries) >= limit:
                    break
        
        return summaries
    
    def get_latest_results_by_layer(self) -> Dict[str, TestRunResult]:
        """Get latest test results for each layer"""
        layers = ['core', 'adapter', 'service', 'api']
        results = {}
        
        for layer in layers:
            history = self.get_test_history(limit=100)
            for result in history:
                if result.layer == layer:
                    results[layer] = result
                    break
        
        return results
    
    def cleanup_old_results(self, days: int = 30):
        """
        Remove test results older than specified days
        
        Args:
            days: Number of days to keep
        """
        cutoff = datetime.utcnow().timestamp() - (days * 86400)
        
        for filename in os.listdir(self.results_dir):
            filepath = os.path.join(self.results_dir, filename)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
