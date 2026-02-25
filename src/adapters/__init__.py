"""
Adapters Package

Python wrappers for C libraries (FFI layer).

This package provides Pythonic interfaces to C data structures
and operations. All ctypes interactions are isolated here.

Available adapters:
- SimpleDB: Key-value hash table database

Usage:
    from adapters import SimpleDB

    db = SimpleDB()
    db.set("key", "value")
    print(db.get("key"))
"""

from .simple_db import SimpleDB, DBStats

__all__ = [
    'SimpleDB',
    'DBStats',
]

__version__ = '1.0.0'
