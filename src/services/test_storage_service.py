"""
Test Storage Service

Persists test results to database for historical tracking and analysis.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from src.adapters.simple_db import SimpleDB
from src.services.test_execution_service import TestResult, TestRunResult


class TestStorageService:
    """
    Service for persisting and querying test results
    """
    
    def __init__(self, db_path: str = "test_results.db"):
        """
        Initialize test storage service
        
        Args:
            db_path: Path to the database file (used for naming, SimpleDB is in-memory)
        """
        self.db = SimpleDB()
        self.db_path = db_path  # Store for reference but SimpleDB is in-memory
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database structure"""
        # Store test runs as JSON
        # Key format: run:{run_id}
        # Key format: run_index:{timestamp} -> run_id
        # Key format: layer:{layer}:latest -> run_id
        # Key format: stats:total_runs -> count
        pass
    
    def store_test_run(self, result: TestRunResult):
        """
        Store a test run result
        
        Args:
            result: TestRunResult to store
        """
        # Store the complete run
        run_key = f"run:{result.run_id}"
        self.db.set(run_key, json.dumps(self._serialize_result(result)))
        
        # Index by timestamp
        index_key = f"run_index:{result.timestamp}"
        self.db.set(index_key, result.run_id)
        
        # Update latest for layer
        if result.layer:
            layer_key = f"layer:{result.layer}:latest"
            self.db.set(layer_key, result.run_id)
        
        # Update statistics
        self._update_stats(result)
        
        # Store individual test results
        for test_result in result.test_results:
            test_key = f"test:{result.run_id}:{test_result.test_id}"
            self.db.set(test_key, json.dumps(self._serialize_test(test_result)))
    
    def get_test_run(self, run_id: str) -> Optional[TestRunResult]:
        """
        Get a specific test run
        
        Args:
            run_id: ID of the run to retrieve
            
        Returns:
            TestRunResult or None if not found
        """
        run_key = f"run:{run_id}"
        data = self.db.get(run_key)
        
        if not data:
            return None
        
        return self._deserialize_result(json.loads(data))
    
    def get_latest_run_by_layer(self, layer: str) -> Optional[TestRunResult]:
        """
        Get the latest test run for a specific layer
        
        Args:
            layer: Layer name (core, adapter, service, api)
            
        Returns:
            TestRunResult or None
        """
        layer_key = f"layer:{layer}:latest"
        run_id = self.db.get(layer_key)
        
        if not run_id:
            return None
        
        return self.get_test_run(run_id)
    
    def get_test_history(self, limit: int = 50, layer: Optional[str] = None) -> List[TestRunResult]:
        """
        Get test run history
        
        Args:
            limit: Maximum number of runs to return
            layer: Optional layer filter
            
        Returns:
            List of TestRunResult objects
        """
        # Get all run indices
        all_keys = self.db.keys()
        run_indices = [k for k in all_keys if k.startswith("run_index:")]
        run_indices.sort(reverse=True)  # Most recent first
        
        results = []
        for index_key in run_indices[:limit * 2]:  # Get extra in case of filtering
            run_id = self.db.get(index_key)
            if run_id:
                result = self.get_test_run(run_id)
                if result and (layer is None or result.layer == layer):
                    results.append(result)
                    if len(results) >= limit:
                        break
        
        return results
    
    def get_test_trends(self, layer: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
        """
        Get test trends over time
        
        Args:
            layer: Optional layer filter
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend data
        """
        history = self.get_test_history(limit=100, layer=layer)
        
        # Calculate trends
        total_runs = len(history)
        total_passed = sum(r.passed for r in history)
        total_failed = sum(r.failed for r in history)
        total_tests = sum(r.total for r in history)
        
        avg_success_rate = sum(r.success_rate for r in history) / total_runs if total_runs > 0 else 0
        avg_duration = sum(r.duration for r in history) / total_runs if total_runs > 0 else 0
        
        # Get latest results
        latest = history[0] if history else None
        
        return {
            'total_runs': total_runs,
            'total_tests_executed': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'average_success_rate': round(avg_success_rate, 2),
            'average_duration': round(avg_duration, 2),
            'latest_run': self._serialize_result(latest) if latest else None,
            'history_days': days,
            'layer': layer
        }
    
    def get_failing_tests(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get currently failing tests
        
        Args:
            limit: Maximum number of tests to return
            
        Returns:
            List of failing test information
        """
        failing = []
        
        # Get recent runs
        history = self.get_test_history(limit=10)
        
        for run in history:
            for test in run.test_results:
                if test.status == 'failed':
                    failing.append({
                        'test_id': test.test_id,
                        'name': test.name,
                        'layer': test.layer,
                        'error': test.error_message,
                        'run_id': run.run_id,
                        'timestamp': test.timestamp
                    })
                    
                    if len(failing) >= limit:
                        return failing
        
        return failing
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall test statistics"""
        stats_key = "stats:total_runs"
        total_runs = self.db.get(stats_key) or "0"
        
        # Get latest results by layer
        layers = ['core', 'adapter', 'service', 'api']
        layer_stats = {}
        
        for layer in layers:
            latest = self.get_latest_run_by_layer(layer)
            if latest:
                layer_stats[layer] = {
                    'total': latest.total,
                    'passed': latest.passed,
                    'failed': latest.failed,
                    'success_rate': latest.success_rate,
                    'last_run': latest.timestamp
                }
        
        return {
            'total_runs': int(total_runs),
            'layers': layer_stats,
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def _update_stats(self, result: TestRunResult):
        """Update overall statistics"""
        stats_key = "stats:total_runs"
        current = int(self.db.get(stats_key) or "0")
        self.db.set(stats_key, str(current + 1))
    
    def _serialize_result(self, result: TestRunResult) -> Dict:
        """Convert TestRunResult to dict for storage"""
        if result is None:
            return None
        
        return {
            'run_id': result.run_id,
            'timestamp': result.timestamp,
            'total': result.total,
            'passed': result.passed,
            'failed': result.failed,
            'skipped': result.skipped,
            'errors': result.errors,
            'duration': result.duration,
            'layer': result.layer,
            'success_rate': result.success_rate,
            'test_results': [self._serialize_test(t) for t in result.test_results]
        }
    
    def _serialize_test(self, test: TestResult) -> Dict:
        """Convert TestResult to dict for storage"""
        return {
            'test_id': test.test_id,
            'name': test.name,
            'status': test.status,
            'duration': test.duration,
            'error_message': test.error_message,
            'layer': test.layer,
            'markers': test.markers,
            'timestamp': test.timestamp
        }
    
    def _deserialize_result(self, data: Dict) -> TestRunResult:
        """Convert dict to TestRunResult"""
        test_results = [TestResult(**t) for t in data.get('test_results', [])]
        data['test_results'] = test_results
        return TestRunResult(**data)
    
    def cleanup_old_data(self, days: int = 90):
        """
        Remove test data older than specified days
        
        Args:
            days: Number of days to retain
        """
        cutoff = datetime.utcnow().timestamp() - (days * 86400)
        cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
        
        # Get all run indices
        all_keys = self.db.keys()
        run_indices = [k for k in all_keys if k.startswith("run_index:")]
        
        for index_key in run_indices:
            timestamp = index_key.replace("run_index:", "")
            if timestamp < cutoff_iso:
                run_id = self.db.get(index_key)
                if run_id:
                    # Delete the run
                    self.db.delete(f"run:{run_id}")
                    # Delete the index
                    self.db.delete(index_key)
                    # Delete individual test results
                    test_keys = [k for k in all_keys if k.startswith(f"test:{run_id}:")]
                    for test_key in test_keys:
                        self.db.delete(test_key)
