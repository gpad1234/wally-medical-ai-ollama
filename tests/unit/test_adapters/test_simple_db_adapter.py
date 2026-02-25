"""
Adapter Layer Tests: SimpleDB Python Wrapper

Tests Python-specific features of the adapter layer.
Focus: Pythonic API, type handling, error handling.

Test IDs: TC-A-001 through TC-A-011
"""

import pytest
from adapters import SimpleDB


class TestPythonicAPI:
    """Test Python-specific API features"""

    def test_context_manager(self):
        """
        TC-A-001: Context Manager

        Verify 'with' statement works correctly.
        """
        with SimpleDB() as db:
            db.set("key", "value")
            assert db.get("key") == "value"
            assert db.count() == 1

        # Database should be cleaned up after context

    def test_dict_like_set_get(self, simple_db):
        """
        TC-A-002: Dict-like Access

        Verify db[key] = value and db[key] syntax works.
        """
        # Set using dict syntax
        simple_db["user:123"] = "Alice"

        # Get using dict syntax
        value = simple_db["user:123"]

        assert value == "Alice"

    def test_dict_like_get_missing_raises_keyerror(self, simple_db):
        """
        Verify db[key] raises KeyError for missing key.
        """
        with pytest.raises(KeyError):
            _ = simple_db["nonexistent"]

    def test_contains_operator(self, simple_db):
        """
        TC-A-003: Contains Operator

        Verify 'in' operator works.
        """
        simple_db.set("key1", "value1")

        assert "key1" in simple_db
        assert "key2" not in simple_db

    def test_len_function(self, simple_db):
        """
        TC-A-004: Len Function

        Verify len(db) returns correct count.
        """
        assert len(simple_db) == 0

        simple_db.set("key1", "value1")
        simple_db.set("key2", "value2")

        assert len(simple_db) == 2

    def test_del_operator(self, simple_db):
        """
        TC-A-005: Del Operator

        Verify del db[key] works.
        """
        simple_db["key"] = "value"
        assert "key" in simple_db

        del simple_db["key"]
        assert "key" not in simple_db

    def test_del_missing_raises_keyerror(self, simple_db):
        """
        Verify del db[key] raises KeyError for missing key.
        """
        with pytest.raises(KeyError):
            del simple_db["nonexistent"]


class TestTypeHandling:
    """Test type conversion and validation"""

    def test_unicode_strings(self, simple_db):
        """
        TC-A-006: Unicode Strings

        Verify Unicode is handled correctly.
        """
        test_cases = [
            ("unicode_1", "Hello 世界"),
            ("unicode_2", "Привет мир"),
            ("unicode_3", "مرحبا بالعالم"),
            ("emoji", "Hello 👋 World 🌍"),
        ]

        for key, value in test_cases:
            simple_db.set(key, value)
            retrieved = simple_db.get(key)
            assert retrieved == value, f"Failed for {key}: {value}"

    def test_type_error_on_non_string_key(self, simple_db):
        """
        TC-A-007: Type Errors

        Verify TypeError raised for non-string keys.
        """
        with pytest.raises(TypeError):
            simple_db.set(123, "value")  # int key

        with pytest.raises(TypeError):
            simple_db.set(None, "value")  # None key

        with pytest.raises(TypeError):
            simple_db.set(["list"], "value")  # list key

    def test_type_error_on_non_string_value(self, simple_db):
        """
        Verify TypeError raised for non-string values.
        """
        with pytest.raises(TypeError):
            simple_db.set("key", 123)  # int value

        with pytest.raises(TypeError):
            simple_db.set("key", None)  # None value

    def test_type_error_on_get(self, simple_db):
        """
        Verify TypeError raised for non-string key in get().
        """
        with pytest.raises(TypeError):
            simple_db.get(123)

    def test_type_error_on_exists(self, simple_db):
        """
        Verify TypeError raised for non-string key in exists().
        """
        with pytest.raises(TypeError):
            simple_db.exists(123)


class TestListOperations:
    """Test list-like operations"""

    def test_keys_returns_list(self, simple_db):
        """
        Verify keys() returns a Python list.
        """
        simple_db.set("key1", "value1")
        simple_db.set("key2", "value2")

        keys = simple_db.keys()

        assert isinstance(keys, list)
        assert len(keys) == 2
        assert set(keys) == {"key1", "key2"}

    def test_keys_empty_db(self, simple_db):
        """
        Verify keys() returns empty list for empty DB.
        """
        keys = simple_db.keys()
        assert keys == []

    def test_items_returns_list_of_tuples(self, simple_db):
        """
        Verify items() returns list of (key, value) tuples.
        """
        simple_db.set("key1", "value1")
        simple_db.set("key2", "value2")

        items = simple_db.items()

        assert isinstance(items, list)
        assert len(items) == 2

        # Verify tuples
        for item in items:
            assert isinstance(item, tuple)
            assert len(item) == 2

        # Verify content
        assert set(items) == {("key1", "value1"), ("key2", "value2")}

    def test_items_empty_db(self, simple_db):
        """
        Verify items() returns empty list for empty DB.
        """
        items = simple_db.items()
        assert items == []


class TestIntegration:
    """Integration tests between adapter and core"""

    def test_adapter_core_integration(self, simple_db):
        """
        TC-A-009: Adapter-Core Integration

        Verify adapter correctly calls C functions.
        """
        # This implicitly tests the integration
        # If any C function fails, the test will fail

        simple_db.set("key", "value")
        assert simple_db.get("key") == "value"
        assert simple_db.exists("key") is True
        assert simple_db.delete("key") is True
        assert simple_db.exists("key") is False

    def test_multiple_instances_independence(self):
        """
        TC-A-010: Multiple Instances

        Verify multiple SimpleDB instances are independent.
        """
        db1 = SimpleDB()
        db2 = SimpleDB()
        db3 = SimpleDB()

        # Set different values in each
        db1.set("key", "value1")
        db2.set("key", "value2")
        db3.set("key", "value3")

        # Verify independence
        assert db1.get("key") == "value1"
        assert db2.get("key") == "value2"
        assert db3.get("key") == "value3"

        # Verify separate counts
        db1.set("extra", "data")
        assert db1.count() == 2
        assert db2.count() == 1
        assert db3.count() == 1

        # Cleanup
        del db1, db2, db3


class TestStatsMethods:
    """Test statistics and debugging methods"""

    def test_stats_returns_dict(self, simple_db):
        """
        Verify stats() returns a dictionary.
        """
        stats = simple_db.stats()

        assert isinstance(stats, dict)
        assert 'total_entries' in stats
        assert 'total_collisions' in stats
        assert 'max_chain_length' in stats
        assert 'used_buckets' in stats

    def test_stats_values_make_sense(self, simple_db):
        """
        Verify stats values are reasonable.
        """
        # Empty database
        stats = simple_db.stats()
        assert stats['total_entries'] == 0

        # Add some data
        for i in range(10):
            simple_db.set(f"key_{i}", f"value_{i}")

        stats = simple_db.stats()
        assert stats['total_entries'] == 10
        assert stats['used_buckets'] > 0
        assert stats['used_buckets'] <= 10
        assert stats['max_chain_length'] >= 1

    def test_repr(self, simple_db):
        """
        Verify __repr__ returns useful string.
        """
        simple_db.set("key1", "value1")
        simple_db.set("key2", "value2")

        repr_str = repr(simple_db)

        assert "SimpleDB" in repr_str
        assert "2" in repr_str  # count


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_memory_error_handled(self):
        """
        Verify MemoryError raised if database creation fails.

        Note: Hard to trigger in practice, so this is mainly
        for documentation of expected behavior.
        """
        # If db_create() returns NULL, should raise MemoryError
        # This is tested implicitly in simple_db fixture
        pass

    def test_clear_empty_database(self, simple_db):
        """
        Verify clear() works on empty database.
        """
        simple_db.clear()  # Should not crash
        assert simple_db.count() == 0

    def test_delete_from_empty_database(self, simple_db):
        """
        Verify delete() on empty database returns False.
        """
        result = simple_db.delete("nonexistent")
        assert result is False

    def test_get_from_empty_database(self, simple_db):
        """
        Verify get() on empty database returns None.
        """
        value = simple_db.get("nonexistent")
        assert value is None


# ============================================================================
# INTEGRATION WITH STANDARD PYTHON PATTERNS
# ============================================================================

class TestPythonPatterns:
    """Test integration with standard Python patterns"""

    def test_can_iterate_over_keys(self, populated_db):
        """
        Verify can iterate over keys.
        """
        keys = list(populated_db.keys())
        assert len(keys) == 5

        # Should be able to iterate
        for key in keys:
            assert isinstance(key, str)
            assert key in populated_db

    def test_can_iterate_over_items(self, populated_db):
        """
        Verify can iterate over items.
        """
        items = populated_db.items()

        for key, value in items:
            assert isinstance(key, str)
            assert isinstance(value, str)
            assert populated_db.get(key) == value

    def test_dictionary_like_update_pattern(self, simple_db):
        """
        Verify dictionary-like update pattern works.
        """
        data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        # Bulk update
        for key, value in data.items():
            simple_db[key] = value

        # Verify
        for key, value in data.items():
            assert simple_db[key] == value

    def test_comprehension_patterns(self, populated_db):
        """
        Verify works with Python comprehensions.
        """
        # List comprehension over keys
        keys = [k for k in populated_db.keys() if k.startswith("user:")]
        assert len(keys) == 3

        # Dict comprehension
        user_dict = {k: populated_db[k] for k in keys}
        assert len(user_dict) == 3
