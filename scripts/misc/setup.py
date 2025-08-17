#!/usr/bin/env python3
"""
Setup script for UV Tests application.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: str) -> bool:
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("Setting up UV Tests application...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if not run_command("uv sync"):
        print("Failed to install dependencies")
        sys.exit(1)
    
    # Install development dependencies
    print("\nInstalling development dependencies...")
    if not run_command("uv add --dev pytest"):
        print("Failed to install pytest")
        sys.exit(1)
    
    # Run tests to verify setup
    print("\nRunning tests to verify setup...")
    if not run_command("python -m pytest tests/ -v"):
        print("Some tests failed, but setup is complete")
    
    print("\n✓ Setup complete! You can now:")
    print("  - Run the app: python main.py")
    print("  - Run tests: pytest")
    print("  - View docs: cat docs/index.md")


if __name__ == "__main__":
    main() 