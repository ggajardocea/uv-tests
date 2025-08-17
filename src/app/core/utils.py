"""
Utility functions for the UV Tests application.
"""

import sys
from typing import Dict, Any


def get_python_version() -> str:
    """Get the current Python version."""
    return sys.version


def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return {
        "python_version": sys.version,
        "platform": sys.platform,
        "executable": sys.executable,
        "path": sys.path
    }


def format_version_info(version: str) -> str:
    """Format version information for display."""
    return f"Python Version: {version}" 