#!/usr/bin/env python3
"""
Quality Control Dashboard

Web-based GUI for automated testing, result tracking, and quality metrics.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime
from src.services.test_runner_service import TestRunnerService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize test runner service (handles both execution and storage)
test_runner = TestRunnerService()


@app.route('/')
def index():
    """Render QC dashboard"""
    return render_template('qc_dashboard.html')


@app.route('/api/qc/status')
def get_status():
    """Get overall QC status"""
    try:
        dashboard_data = test_runner.get_dashboard_data()
        latest = dashboard_data.get('latest_suite')
        layer_stats = dashboard_data.get('layer_stats', {})
        
        # Format into stats structure expected by frontend
        stats = {
            'total_runs': len(dashboard_data.get('recent_suites', [])),
            'layers': {}
        }
        
        # Add layer statistics
        for layer, lstats in layer_stats.items():
            if lstats and lstats.get('total', 0) > 0:
                stats['layers'][layer] = {
                    'total': lstats.get('total', 0),
                    'passed': lstats.get('passed', 0),
                    'failed': lstats.get('failed', 0),
                    'success_rate': (lstats.get('passed', 0) / lstats.get('total', 1)) * 100,
                    'last_run': 'N/A'
                }
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/qc/run-tests', methods=['POST'])
def run_tests():
    """Execute tests"""
    try:
        data = request.get_json() or {}
        layer = data.get('layer')
        test_file = data.get('test_path')
        coverage = data.get('coverage', False)
        
        # Run tests and get suite result
        if test_file:
            suite = test_runner.run_tests(test_file=test_file, coverage=coverage)
        elif layer and layer != 'all':
            suite = test_runner.run_tests(layer=layer, coverage=coverage)
        else:
            suite = test_runner.run_tests(coverage=coverage)
        
        return jsonify({
            'success': True,
            'data': {
                'run_id': suite.suite_id,
                'total': suite.total_tests,
                'passed': suite.passed,
                'failed': suite.failed,
                'skipped': suite.skipped,
                'duration': suite.duration,
                'success_rate': (suite.passed / suite.total_tests * 100) if suite.total_tests > 0 else 0
            }
        })
    except Exception as e:
        logger.error(f"Error running tests: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/qc/history')
def get_history():
    """Get test run history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        layer = request.args.get('layer')
        
        all_suites = test_runner.db.get_all_suites(limit=limit)
        
        # Filter by layer if specified
        if layer:
            # Filter based on suite name containing layer
            all_suites = [s for s in all_suites if layer.lower() in s.get('suite_name', '').lower()]
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'run_id': s['suite_id'],
                    'timestamp': s['timestamp'],
                    'layer': layer or 'all',
                    'total': s['total_tests'],
                    'passed': s['passed'],
                    'failed': s['failed'],
                    'skipped': s['skipped'],
                    'duration': s['duration'],
                    'success_rate': (s['passed'] / s['total_tests'] * 100) if s['total_tests'] > 0 else 0
                }
                for s in all_suites
            ]
        })
    except Exception as e:
        logger.error(f"Error getting history: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/qc/run/<run_id>')
def get_run_details(run_id):
    """Get detailed results for a specific run"""
    try:
        suite = test_runner.db.get_latest_suite()
        if not suite or suite['suite_id'] != run_id:
            # Try to find in all suites
            all_suites = test_runner.db.get_all_suites(limit=100)
            suite = next((s for s in all_suites if s['suite_id'] == run_id), None)
        
        if not suite:
            return jsonify({
                'success': False,
                'error': 'Run not found'
            }), 404
        
        test_results = test_runner.db.get_suite_results(run_id)
        
        return jsonify({
            'success': True,
            'data': {
                'run_id': suite['suite_id'],
                'timestamp': suite['timestamp'],
                'layer': 'all',
                'total': suite['total_tests'],
                'passed': suite['passed'],
                'failed': suite['failed'],
                'skipped': suite['skipped'],
                'errors': suite['errors'],
                'duration': suite['duration'],
                'success_rate': (suite['passed'] / suite['total_tests'] * 100) if suite['total_tests'] > 0 else 0,
                'tests': [
                    {
                        'test_id': t['test_id'],
                        'name': t['test_name'],
                        'status': t['status'],
                        'duration': t['duration'],
                        'error': t.get('error_message'),
                        'layer': t['layer'],
                        'markers': []
                    }
                    for t in test_results
                ]
            }
        })
    except Exception as e:
        logger.error(f"Error getting run details: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/qc/trends')
def get_trends():
    """Get test trends"""
    try:
        layer = request.args.get('layer')
        days = request.args.get('days', 7, type=int)
        
        trends = test_runner.db.get_trends(layer=layer, days=days)
        
        # Calculate aggregate statistics
        total_tests = sum(t['total_tests'] for t in trends)
        avg_pass_rate = sum(t['pass_rate'] for t in trends) / len(trends) if trends else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_runs': len(trends),
                'total_tests_executed': total_tests,
                'average_success_rate': avg_pass_rate,
                'history_days': days,
                'layer': layer,
                'trends': trends
            }
        })
    except Exception as e:
        logger.error(f"Error getting trends: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/qc/failing-tests')
def get_failing_tests():
    """Get currently failing tests"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        # Get recent test results
        recent_suites = test_runner.db.get_all_suites(limit=5)
        failing = []
        
        for suite in recent_suites:
            results = test_runner.db.get_suite_results(suite['suite_id'])
            for test in results:
                if test['status'] == 'failed':
                    failing.append({
                        'test_id': test['test_id'],
                        'name': test['test_name'],
                        'layer': test['layer'],
                        'error': test.get('error_message', 'No error message'),
                        'run_id': suite['suite_id'],
                        'timestamp': test['timestamp']
                    })
                    if len(failing) >= limit:
                        break
            if len(failing) >= limit:
                break
        
        return jsonify({
            'success': True,
            'data': failing
        })
    except Exception as e:
        logger.error(f"Error getting failing tests: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/qc/layers')
def get_layers():
    """Get available test layers"""
    return jsonify({
        'success': True,
        'data': {
            'layers': [
                {'id': 'core', 'name': 'Core (C Library)', 'description': 'Low-level C data structures'},
                {'id': 'adapter', 'name': 'Adapter (Python-C)', 'description': 'Python bindings to C layer'},
                {'id': 'service', 'name': 'Service', 'description': 'Business logic layer'},
                {'id': 'api', 'name': 'API', 'description': 'REST API endpoints'},
                {'id': 'all', 'name': 'All Tests', 'description': 'Complete test suite'}
            ]
        }
    })


@app.route('/api/qc/latest-by-layer')
def get_latest_by_layer():
    """Get latest test results for each layer"""
    try:
        layers = ['core', 'adapter', 'service', 'api']
        results = {}
        
        dashboard_data = test_runner.get_dashboard_data()
        layer_stats = dashboard_data.get('layer_stats', {})
        
        # Get recent suites to find latest per layer
        recent_suites = dashboard_data.get('recent_suites', [])
        
        for layer in layers:
            # Find most recent suite for this layer
            layer_suite = next(
                (s for s in recent_suites if layer.lower() in s.get('suite_name', '').lower()),
                None
            )
            
            if layer_suite:
                results[layer] = {
                    'run_id': layer_suite['suite_id'],
                    'timestamp': layer_suite['timestamp'],
                    'total': layer_suite['total_tests'],
                    'passed': layer_suite['passed'],
                    'failed': layer_suite['failed'],
                    'success_rate': (layer_suite['passed'] / layer_suite['total_tests'] * 100) if layer_suite['total_tests'] > 0 else 0,
                    'duration': layer_suite['duration']
                }
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        logger.error(f"Error getting latest by layer: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('QC_PORT', 5001))
    debug = os.environ.get('QC_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting QC Dashboard on port {port}")
    logger.info(f"Access dashboard at: http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
