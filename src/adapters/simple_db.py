"""
SimpleDB Python Adapter

Python wrapper for the C simple_db library.
This is the ONLY module that uses ctypes for simple_db.

All upper layers (services, API) should import from here, not use ctypes directly.
"""

import ctypes
from typing import Optional, List, Dict, Any
from ._loader import load_library


# ============================================================================
# LOAD C LIBRARY
# ============================================================================

# Load the shared library
_lib = load_library("simpledb")


# ============================================================================
# C TYPE DEFINITIONS
# ============================================================================

class DBStats(ctypes.Structure):
    """
    Database statistics structure (matches C DBStats).
    """
    _fields_ = [
        ("total_entries", ctypes.c_size_t),
        ("total_collisions", ctypes.c_size_t),
        ("max_chain_length", ctypes.c_size_t),
        ("used_buckets", ctypes.c_size_t),
    ]

    def to_dict(self) -> Dict[str, int]:
        """Convert to Python dictionary."""
        return {
            'total_entries': self.total_entries,
            'total_collisions': self.total_collisions,
            'max_chain_length': self.max_chain_length,
            'used_buckets': self.used_buckets,
        }


# ============================================================================
# C FUNCTION SIGNATURES
# ============================================================================

# Lifecycle
_lib.db_create.argtypes = []
_lib.db_create.restype = ctypes.c_void_p

_lib.db_destroy.argtypes = [ctypes.c_void_p]
_lib.db_destroy.restype = None

# CRUD operations
_lib.db_set.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
_lib.db_set.restype = ctypes.c_bool

_lib.db_get.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.db_get.restype = ctypes.c_char_p

_lib.db_delete.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.db_delete.restype = ctypes.c_bool

_lib.db_exists.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.db_exists.restype = ctypes.c_bool

# Utility operations
_lib.db_count.argtypes = [ctypes.c_void_p]
_lib.db_count.restype = ctypes.c_size_t

_lib.db_clear.argtypes = [ctypes.c_void_p]
_lib.db_clear.restype = None

_lib.db_keys.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]
_lib.db_keys.restype = ctypes.POINTER(ctypes.c_char_p)

_lib.db_stats.argtypes = [ctypes.c_void_p]
_lib.db_stats.restype = DBStats

_lib.db_print.argtypes = [ctypes.c_void_p]
_lib.db_print.restype = None


# ============================================================================
# PYTHON WRAPPER CLASS
# ============================================================================

class SimpleDB:
    """
    Python wrapper for C SimpleDB library.

    A simple key-value store backed by a hash table implemented in C.

    Features:
    - String keys and values
    - O(1) average case for get/set/delete
    - Context manager support (with statement)
    - Pythonic API

    Example:
        >>> db = SimpleDB()
        >>> db.set("user:123", "Alice")
        True
        >>> db.get("user:123")
        'Alice'
        >>> db.delete("user:123")
        True

    Or use as context manager:
        >>> with SimpleDB() as db:
        ...     db.set("key", "value")
        ...     print(db.get("key"))
        value
    """

    def __init__(self):
        """
        Create a new database instance.

        Raises:
            MemoryError: If database creation fails
        """
        self._db = _lib.db_create()
        if not self._db:
            raise MemoryError("Failed to create database")

    def __del__(self):
        """Destructor - cleanup database."""
        if hasattr(self, '_db') and self._db:
            _lib.db_destroy(self._db)
            self._db = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.__del__()
        return False

    # ========================================================================
    # CRUD OPERATIONS
    # ========================================================================

    def set(self, key: str, value: str) -> bool:
        """
        Set a key-value pair (insert or update).

        Args:
            key: Key string
            value: Value string

        Returns:
            True on success, False on error

        Example:
            >>> db.set("user:123", "Alice")
            True
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("Key and value must be strings")

        return _lib.db_set(
            self._db,
            key.encode('utf-8'),
            value.encode('utf-8')
        )

    def get(self, key: str) -> Optional[str]:
        """
        Get value by key.

        Args:
            key: Key to look up

        Returns:
            Value string if found, None otherwise

        Example:
            >>> db.set("key", "value")
            >>> db.get("key")
            'value'
            >>> db.get("nonexistent")
            None
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        result = _lib.db_get(self._db, key.encode('utf-8'))
        return result.decode('utf-8') if result else None

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair.

        Args:
            key: Key to delete

        Returns:
            True if deleted, False if key not found

        Example:
            >>> db.set("key", "value")
            >>> db.delete("key")
            True
            >>> db.delete("key")
            False
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        return _lib.db_delete(self._db, key.encode('utf-8'))

    def exists(self, key: str) -> bool:
        """
        Check if key exists in database.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise

        Example:
            >>> db.set("key", "value")
            >>> db.exists("key")
            True
            >>> db.exists("nonexistent")
            False
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        return _lib.db_exists(self._db, key.encode('utf-8'))

    # ========================================================================
    # UTILITY OPERATIONS
    # ========================================================================

    def count(self) -> int:
        """
        Get number of key-value pairs in database.

        Returns:
            Number of entries

        Example:
            >>> db.set("key1", "value1")
            >>> db.set("key2", "value2")
            >>> db.count()
            2
        """
        return _lib.db_count(self._db)

    def clear(self) -> None:
        """
        Remove all entries from database.

        Example:
            >>> db.set("key", "value")
            >>> db.clear()
            >>> db.count()
            0
        """
        _lib.db_clear(self._db)

    def keys(self) -> List[str]:
        """
        Get list of all keys in database.

        Returns:
            List of key strings

        Example:
            >>> db.set("key1", "value1")
            >>> db.set("key2", "value2")
            >>> sorted(db.keys())
            ['key1', 'key2']
        """
        count = ctypes.c_size_t()
        keys_ptr = _lib.db_keys(self._db, ctypes.byref(count))

        if not keys_ptr:
            return []

        # Extract keys
        keys = []
        for i in range(count.value):
            key_bytes = keys_ptr[i]
            if key_bytes:
                keys.append(key_bytes.decode('utf-8'))

        # Note: C library handles freeing the array
        return keys

    def items(self) -> List[tuple]:
        """
        Get list of all (key, value) pairs.

        Returns:
            List of (key, value) tuples

        Example:
            >>> db.set("key1", "value1")
            >>> db.set("key2", "value2")
            >>> sorted(db.items())
            [('key1', 'value1'), ('key2', 'value2')]
        """
        items = []
        for key in self.keys():
            value = self.get(key)
            if value is not None:
                items.append((key, value))
        return items

    def stats(self) -> Dict[str, int]:
        """
        Get database statistics.

        Returns:
            Dictionary with statistics:
            - total_entries: Number of key-value pairs
            - total_collisions: Number of hash collisions
            - max_chain_length: Longest collision chain
            - used_buckets: Non-empty hash buckets

        Example:
            >>> db.set("key", "value")
            >>> stats = db.stats()
            >>> stats['total_entries']
            1
        """
        c_stats = _lib.db_stats(self._db)
        return c_stats.to_dict()

    def print_debug(self) -> None:
        """
        Print database contents to stdout (for debugging).

        Example:
            >>> db.set("key", "value")
            >>> db.print_debug()
            Database Contents:
            key -> value
        """
        _lib.db_print(self._db)

    # ========================================================================
    # PYTHON SPECIAL METHODS
    # ========================================================================

    def __len__(self) -> int:
        """
        Get number of entries (supports len(db)).

        Example:
            >>> db.set("key", "value")
            >>> len(db)
            1
        """
        return self.count()

    def __contains__(self, key: str) -> bool:
        """
        Check if key exists (supports 'key in db').

        Example:
            >>> db.set("key", "value")
            >>> "key" in db
            True
        """
        return self.exists(key)

    def __getitem__(self, key: str) -> str:
        """
        Get value by key (supports db[key]).

        Raises:
            KeyError: If key not found

        Example:
            >>> db.set("key", "value")
            >>> db["key"]
            'value'
        """
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        """
        Set value by key (supports db[key] = value).

        Example:
            >>> db["key"] = "value"
            >>> db["key"]
            'value'
        """
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """
        Delete key (supports del db[key]).

        Raises:
            KeyError: If key not found

        Example:
            >>> db["key"] = "value"
            >>> del db["key"]
            >>> "key" in db
            False
        """
        if not self.delete(key):
            raise KeyError(key)

    def __repr__(self) -> str:
        """String representation."""
        return f"<SimpleDB entries={self.count()}>"


# ============================================================================
# MODULE TEST
# ============================================================================

if __name__ == '__main__':
    print("SimpleDB Python Adapter Test")
    print("=" * 50)

    # Create database
    db = SimpleDB()
    print(f"✅ Created database: {db}")

    # Test set/get
    db.set("user:123", "Alice")
    db.set("user:456", "Bob")
    print(f"✅ Added 2 entries")

    # Test get
    print(f"✅ get('user:123') = {db.get('user:123')}")

    # Test exists
    print(f"✅ exists('user:123') = {db.exists('user:123')}")
    print(f"✅ exists('user:999') = {db.exists('user:999')}")

    # Test count
    print(f"✅ count() = {db.count()}")

    # Test keys
    print(f"✅ keys() = {db.keys()}")

    # Test stats
    stats = db.stats()
    print(f"✅ stats() = {stats}")

    # Test Python special methods
    print(f"✅ len(db) = {len(db)}")
    print(f"✅ 'user:123' in db = {'user:123' in db}")
    print(f"✅ db['user:123'] = {db['user:123']}")

    # Test delete
    db.delete("user:123")
    print(f"✅ Deleted user:123, count = {db.count()}")

    # Test clear
    db.clear()
    print(f"✅ Cleared database, count = {db.count()}")

    print("\n" + "=" * 50)
    print("All tests passed! ✅")
