"""
Basic usage example for the UV Tests application.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from app.core.utils import get_python_version, get_system_info, format_version_info


def main():
    """Demonstrate basic usage of the application."""
    print("=== UV Tests Application - Basic Usage ===\n")
    
    # Get Python version
    version = get_python_version()
    print(f"Current Python version: {version}")
    
    # Format version info
    formatted = format_version_info(version)
    print(f"Formatted: {formatted}")
    
    # Get system information
    print("\nSystem Information:")
    info = get_system_info()
    for key, value in info.items():
        if key == "path":
            print(f"  {key}: {len(value)} paths")
        else:
            print(f"  {key}: {value}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main() 