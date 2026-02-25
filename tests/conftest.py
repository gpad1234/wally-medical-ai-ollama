"""
Pytest Configuration and Shared Fixtures

This file is automatically loaded by pytest and provides
shared fixtures available to all test modules.
"""

import pytest
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))


# ============================================================================
# CORE LAYER FIXTURES
# ============================================================================

@pytest.fixture
def simple_db():
    """
    Fixture: Create a SimpleDB instance for testing.

    Automatically cleans up after test.

    Usage:
        def test_something(simple_db):
            simple_db.set("key", "value")
            assert simple_db.get("key") == "value"
    """
    from adapters import SimpleDB

    db = SimpleDB()
    yield db

    # Cleanup
    db.clear()
    del db


@pytest.fixture
def populated_db():
    """
    Fixture: SimpleDB with pre-populated test data.

    Data:
        user:1 -> Alice
        user:2 -> Bob
        user:3 -> Charlie
        item:1 -> Laptop
        item:2 -> Phone
    """
    from adapters import SimpleDB

    db = SimpleDB()

    # Add test data
    db.set("user:1", "Alice")
    db.set("user:2", "Bob")
    db.set("user:3", "Charlie")
    db.set("item:1", "Laptop")
    db.set("item:2", "Phone")

    yield db

    # Cleanup
    db.clear()
    del db


# ============================================================================
# SERVICE LAYER FIXTURES (for future use)
# ============================================================================

@pytest.fixture
def graph_db():
    """
    Fixture: GraphDB instance for testing.

    Will be implemented when services layer is created.
    """
    pytest.skip("GraphDB fixture not yet implemented")


@pytest.fixture
def sample_graph():
    """
    Fixture: GraphDB with sample graph structure.

    Graph:
        A -> B -> D
        A -> C -> D
        D -> E
    """
    pytest.skip("Sample graph fixture not yet implemented")


# ============================================================================
# API LAYER FIXTURES (for future use)
# ============================================================================

@pytest.fixture
def api_client():
    """
    Fixture: Flask test client for API testing.

    Will be implemented when API layer is created.
    """
    pytest.skip("API client fixture not yet implemented")


# ============================================================================
# TEST DATA GENERATORS
# ============================================================================

@pytest.fixture
def random_keys():
    """
    Fixture: Generate random keys for testing.

    Returns:
        Function that generates N random keys
    """
    import random
    import string

    def _generator(n=10, length=16):
        keys = []
        for _ in range(n):
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            keys.append(key)
        return keys

    return _generator


@pytest.fixture
def large_dataset():
    """
    Fixture: Generate large dataset for stress testing.

    Returns:
        Dictionary with 1000 key-value pairs
    """
    return {
        f"key_{i:04d}": f"value_{i:04d}"
        for i in range(1000)
    }


# ============================================================================
# PERFORMANCE TESTING UTILITIES
# ============================================================================

@pytest.fixture
def timer():
    """
    Fixture: Simple timer for performance testing.

    Usage:
        def test_performance(timer):
            with timer:
                # code to time
            assert timer.elapsed < 0.1  # Must complete in < 100ms
    """
    import time

    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.elapsed = None

        def __enter__(self):
            self.start_time = time.time()
            return self

        def __exit__(self, *args):
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time

    return Timer()


# ============================================================================
# PYTEST HOOKS
# ============================================================================

def pytest_configure(config):
    """
    Pytest configuration hook.
    Called before test collection.
    """
    print("\n" + "="*70)
    print("  WALLY-CLEAN Test Suite")
    print("="*70)


def pytest_collection_modifyitems(config, items):
    """
    Modify test items after collection.
    Can be used to add markers, skip tests, etc.
    """
    # Example: Mark slow tests
    for item in items:
        if "stress" in item.nodeid or "performance" in item.nodeid:
            item.add_marker(pytest.mark.slow)
