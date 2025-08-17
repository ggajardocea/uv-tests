"""
Tests for main application functionality.
"""

import pytest
from app.core.utils import get_python_version, get_system_info, format_version_info


def test_get_python_version():
    """Test get_python_version function."""
    version = get_python_version()
    assert isinstance(version, str)
    assert "Python" in version


def test_get_system_info():
    """Test get_system_info function."""
    info = get_system_info()
    assert isinstance(info, dict)
    assert "python_version" in info
    assert "platform" in info
    assert "executable" in info
    assert "path" in info


def test_format_version_info():
    """Test format_version_info function."""
    test_version = "3.10.0"
    formatted = format_version_info(test_version)
    assert formatted == "Python Version: 3.10.0"


def test_sample_data_fixture(sample_data):
    """Test the sample_data fixture."""
    assert sample_data["test_string"] == "Hello, World!"
    assert sample_data["test_number"] == 42
    assert len(sample_data["test_list"]) == 5 