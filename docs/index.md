# UV Tests Application

Welcome to the UV Tests application! This is a Python project that demonstrates best practices for project structure and testing.

## Features

- Clean, organized project structure
- Comprehensive testing setup with pytest
- Utility functions for system information
- Modern Python packaging with uv

## Quick Start

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Project Structure

```
uv-tests/
├── src/app/           # Main application package
├── tests/             # Test files
├── docs/              # Documentation
├── scripts/           # Utility scripts
├── requirements/       # Additional requirements
└── examples/          # Example usage
```

## Development

This project uses:
- **uv** for dependency management
- **pytest** for testing
- **Python 3.10+** as the target version 