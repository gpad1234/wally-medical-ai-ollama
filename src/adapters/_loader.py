"""
Shared Library Loader Utility

Handles loading C shared libraries with platform detection.
Supports Linux (.so), macOS (.dylib), and Windows (.dll).
"""

import os
import sys
import ctypes
from pathlib import Path
from typing import Optional


def get_library_extension() -> str:
    """
    Get the shared library extension for current platform.

    Returns:
        '.dll' on Windows
        '.dylib' on macOS
        '.so' on Linux/other
    """
    if sys.platform == 'win32':
        return '.dll'
    elif sys.platform == 'darwin':
        return '.dylib'
    else:
        return '.so'


def find_library_path(lib_name: str) -> Optional[Path]:
    """
    Find a shared library in the core build directory.

    Args:
        lib_name: Library name (e.g., "libsimpledb" or "simpledb")

    Returns:
        Path to library file, or None if not found

    Search order:
        1. src/core/build/lib/
        2. Environment variable WALLY_LIB_PATH
    """
    # Ensure lib_name starts with 'lib'
    if not lib_name.startswith('lib'):
        lib_name = f'lib{lib_name}'

    ext = get_library_extension()
    filename = f'{lib_name}{ext}'

    # Get project root (assumes this file is in src/adapters/)
    this_file = Path(__file__).resolve()
    project_root = this_file.parent.parent.parent  # Go up 3 levels

    # Search path 1: core build directory
    default_path = project_root / 'src' / 'core' / 'build' / 'lib' / filename
    if default_path.exists():
        return default_path

    # Search path 2: environment variable
    env_path = os.environ.get('WALLY_LIB_PATH')
    if env_path:
        env_lib_path = Path(env_path) / filename
        if env_lib_path.exists():
            return env_lib_path

    return None


def load_library(lib_name: str) -> ctypes.CDLL:
    """
    Load a C shared library.

    Args:
        lib_name: Library name without extension
                  (e.g., "libsimpledb", "simpledb", or "simple_db")

    Returns:
        Loaded ctypes.CDLL library object

    Raises:
        FileNotFoundError: If library not found
        OSError: If library cannot be loaded

    Example:
        >>> lib = load_library("simpledb")
        >>> lib.db_create()
    """
    # Normalize library name
    lib_name = lib_name.replace('_', '').replace('-', '')

    # Find library path
    lib_path = find_library_path(lib_name)

    if lib_path is None:
        # Build helpful error message
        ext = get_library_extension()
        expected_name = f'lib{lib_name}{ext}'
        error_msg = (
            f"Library '{expected_name}' not found.\n\n"
            f"Searched locations:\n"
            f"  1. src/core/build/lib/{expected_name}\n"
            f"  2. $WALLY_LIB_PATH/{expected_name} (if set)\n\n"
            f"To fix:\n"
            f"  1. Build C libraries: cd src/core && make\n"
            f"  2. Or set WALLY_LIB_PATH environment variable\n"
        )
        raise FileNotFoundError(error_msg)

    try:
        # Load the library
        lib = ctypes.CDLL(str(lib_path))
        return lib
    except OSError as e:
        raise OSError(
            f"Failed to load library '{lib_path}': {e}\n"
            f"The library may be corrupted or incompatible."
        ) from e


def library_info(lib_name: str) -> dict:
    """
    Get information about a library.

    Args:
        lib_name: Library name

    Returns:
        Dictionary with library information:
        - name: Library name
        - path: Full path to library
        - size: File size in bytes
        - exists: Whether library exists
    """
    lib_path = find_library_path(lib_name)

    if lib_path and lib_path.exists():
        return {
            'name': lib_name,
            'path': str(lib_path),
            'size': lib_path.stat().st_size,
            'exists': True
        }
    else:
        return {
            'name': lib_name,
            'path': None,
            'size': 0,
            'exists': False
        }


# Module test
if __name__ == '__main__':
    print("Library Loader Utility")
    print("=" * 50)
    print(f"Platform: {sys.platform}")
    print(f"Library extension: {get_library_extension()}")
    print()

    # Test loading simpledb
    try:
        lib = load_library("simpledb")
        print("✅ Successfully loaded libsimpledb")
        print(f"   Path: {find_library_path('libsimpledb')}")
    except FileNotFoundError as e:
        print("❌ Failed to load libsimpledb")
        print(f"   {e}")
