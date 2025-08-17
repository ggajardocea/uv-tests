# API Documentation

## Core Module

### `app.core.utils`

Utility functions for the application.

#### `get_python_version() -> str`

Returns the current Python version as a string.

**Returns:**
- `str`: Python version information

**Example:**
```python
from app.core.utils import get_python_version
version = get_python_version()
print(version)  # Python 3.10.0
```

#### `get_system_info() -> Dict[str, Any]`

Returns a dictionary containing system information.

**Returns:**
- `Dict[str, Any]`: Dictionary with system information including:
  - `python_version`: Current Python version
  - `platform`: Operating system platform
  - `executable`: Path to Python executable
  - `path`: Python module search path

**Example:**
```python
from app.core.utils import get_system_info
info = get_system_info()
print(info["platform"])  # linux
```

#### `format_version_info(version: str) -> str`

Formats version information for display.

**Parameters:**
- `version` (str): Version string to format

**Returns:**
- `str`: Formatted version string

**Example:**
```python
from app.core.utils import format_version_info
formatted = format_version_info("3.10.0")
print(formatted)  # Python Version: 3.10.0
``` 