"""
Adapter Layer Tests: Library Loader

Tests the shared library loader utility.
Focus: Platform detection, library finding, error handling.
"""

import pytest
import sys
from pathlib import Path
from adapters._loader import (
    get_library_extension,
    find_library_path,
    load_library,
    library_info
)


class TestPlatformDetection:
    """Test platform-specific behavior"""

    def test_get_library_extension(self):
        """
        Verify correct library extension for platform.
        """
        ext = get_library_extension()

        if sys.platform == 'win32':
            assert ext == '.dll'
        elif sys.platform == 'darwin':
            assert ext == '.dylib'
        else:
            assert ext == '.so'


class TestLibraryFinding:
    """Test library path resolution"""

    def test_find_simpledb_library(self):
        """
        Verify simpledb library can be found.
        """
        lib_path = find_library_path("simpledb")

        assert lib_path is not None
        assert lib_path.exists()
        assert lib_path.name.startswith("libsimpledb")

    def test_find_with_lib_prefix(self):
        """
        Verify finding works with 'lib' prefix.
        """
        path1 = find_library_path("simpledb")
        path2 = find_library_path("libsimpledb")

        assert path1 == path2

    def test_find_nonexistent_library(self):
        """
        Verify returns None for non-existent library.
        """
        lib_path = find_library_path("nonexistent")
        assert lib_path is None


class TestLibraryLoading:
    """Test library loading"""

    def test_load_simpledb(self):
        """
        Verify simpledb library can be loaded.
        """
        lib = load_library("simpledb")
        assert lib is not None

        # Verify some functions exist
        assert hasattr(lib, 'db_create')
        assert hasattr(lib, 'db_set')
        assert hasattr(lib, 'db_get')

    def test_load_with_different_names(self):
        """
        Verify loading works with different name formats.
        """
        lib1 = load_library("simpledb")
        lib2 = load_library("libsimpledb")
        lib3 = load_library("simple_db")

        # All should succeed
        assert lib1 is not None
        assert lib2 is not None
        assert lib3 is not None

    def test_load_nonexistent_raises_error(self):
        """
        Verify FileNotFoundError raised for non-existent library.
        """
        with pytest.raises(FileNotFoundError) as exc_info:
            load_library("nonexistent")

        error_msg = str(exc_info.value)
        assert "not found" in error_msg.lower()
        assert "make" in error_msg.lower()  # Should suggest building


class TestLibraryInfo:
    """Test library information utility"""

    def test_library_info_existing(self):
        """
        Verify library_info returns correct data for existing library.
        """
        info = library_info("simpledb")

        assert info['exists'] is True
        assert info['path'] is not None
        assert info['size'] > 0
        assert 'simpledb' in info['name']

    def test_library_info_nonexistent(self):
        """
        Verify library_info returns correct data for non-existent library.
        """
        info = library_info("nonexistent")

        assert info['exists'] is False
        assert info['path'] is None
        assert info['size'] == 0


class TestErrorMessages:
    """Test error message quality"""

    def test_helpful_error_message(self):
        """
        Verify error messages are helpful and actionable.
        """
        try:
            load_library("missing_lib")
        except FileNotFoundError as e:
            error_msg = str(e)

            # Should contain useful information
            assert "libmissinglib" in error_msg
            assert "src/core" in error_msg
            assert "make" in error_msg

            # Should suggest solutions
            assert "cd src/core" in error_msg or "Build" in error_msg
