# Fibonacci CLI Generator

A professional Python command-line tool for generating Fibonacci sequences with multiple output formats, comprehensive validation, and excellent user experience.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Features

- **Efficient Algorithm**: Iterative Fibonacci generation with O(n) time complexity
- **Multiple Output Formats**: List, inline (comma-separated), and JSON formats
- **Comprehensive Validation**: Handles edge cases and provides clear error messages
- **User-Friendly CLI**: Built with Click framework for intuitive command-line interface
- **Flexible Options**: Count display, verbose mode, and format selection
- **Installable Command**: Use as `fibonacci` or `fib` system-wide command
- **Well-Tested**: >90% code coverage with comprehensive unit and integration tests
- **Performance**: Generates sequences up to 10^6 in under 1 second

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Output Formats](#output-formats)
- [Edge Cases](#edge-cases)
- [Development](#development)
- [Testing](#testing)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/fibonacci-cli.git
cd fibonacci-cli

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install as editable package
pip install -e .
```

### Install from PyPI (when published)

```bash
pip install fibonacci-cli
```

### Verify Installation

```bash
fibonacci --version
# Output: fibonacci, version 1.0.0

fibonacci --help
# Shows complete help information
```

## ⚡ Quick Start

Generate Fibonacci sequence up to 100:

```bash
fibonacci --max-number 100
```

Output:
```
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

Short alias:
```bash
fib -m 100
```

## 📖 Usage

### Basic Command

```bash
fibonacci --max-number <value> [OPTIONS]
```

### Required Arguments

- `--max-number INTEGER` or `-m INTEGER`: Maximum value for the Fibonacci sequence (required)

### Optional Arguments

- `--format [list|inline|json]` or `-f [list|inline|json]`: Output format (default: list)
- `--count` or `-c`: Display the count of numbers in the sequence
- `--verbose` or `-v`: Enable verbose output with detailed information
- `--help` or `-h`: Show help message and exit
- `--version`: Show version information

### Examples

#### Basic Usage

```bash
# Generate sequence up to 100
fibonacci --max-number 100
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

# Using short option
fib -m 50
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

#### With Count Option

```bash
fibonacci --max-number 100 --count
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
Total numbers in sequence: 12
```

#### Different Output Formats

```bash
# Inline format (comma-separated)
fibonacci --max-number 50 --format inline
0, 1, 1, 2, 3, 5, 8, 13, 21, 34

# JSON format with metadata
fibonacci --max-number 20 --format json
{
  "sequence": [0, 1, 1, 2, 3, 5, 8, 13],
  "count": 8,
  "max": 20,
  "largest": 13
}
```

#### Verbose Mode

```bash
fibonacci --max-number 100 --verbose
Generating Fibonacci sequence up to 100...
Sequence generated successfully
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

#### Combined Options

```bash
# JSON format with count
fibonacci -m 1000 -f json -c
{
  "sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987],
  "count": 17,
  "max": 1000,
  "largest": 987
}
Total numbers in sequence: 17
```

### Additional Commands

#### Info Command

Get detailed information about a Fibonacci sequence:

```bash
fibonacci info --max-number 100
{
  "sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
  "count": 12,
  "max": 100,
  "largest": 89,
  "metadata": {
    "algorithm": "iterative",
    "complexity": "O(n) time, O(k) space"
  }
}
```

## 🎨 Output Formats

### List Format (Default)

Python list representation, suitable for copying into code:

```bash
fibonacci -m 50
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Inline Format

Comma-separated values, ideal for readability:

```bash
fibonacci -m 50 --format inline
0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

### JSON Format

Structured data with metadata, perfect for scripting and data processing:

```bash
fibonacci -m 50 --format json
{
  "sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
  "count": 10,
  "max": 50,
  "largest": 34
}
```

## 🔍 Edge Cases

The tool handles various edge cases gracefully:

### Zero and Small Values

```bash
# max_number = 0 returns [0]
fibonacci -m 0
[0]

# max_number = 1 returns [0, 1]
fibonacci -m 1
[0, 1]

# max_number = 2 returns [0, 1, 1, 2]
fibonacci -m 2
[0, 1, 1, 2]
```

### Negative Numbers

```bash
fibonacci -m -10
Error: max_number must be non-negative (got: -10)
```

### Non-Integer Values

```bash
fibonacci -m 3.14
Error: max_number must be an integer (got: 3.14)

fibonacci -m abc
Error: Invalid value for '--max-number': 'abc' is not a valid integer.
```

### Large Values

The tool includes safety checks for extremely large values:

```bash
fibonacci -m 999999999999999
Warning: Generating Fibonacci sequence for very large max_number (999999999999999)
This may take significant time and memory. Continue? [y/N]:
```

### Performance Limits

- Practical limit: 10^15 (with confirmation prompt)
- Recommended maximum: 10^12 for instant results
- Performance: Sequences up to 10^6 generate in under 1 second

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/fibonacci-cli.git
cd fibonacci-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

### Project Structure

```
fibonacci-cli/
├── fibonacci.py            # Core Fibonacci logic
├── fibonacci_cli.py        # CLI application with Click
├── utils.py                # Validation and formatting utilities
├── tests/
│   ├── __init__.py
│   ├── test_fibonacci.py   # Unit tests for core logic
│   └── test_cli.py         # CLI integration tests
├── requirements.txt        # Project dependencies
├── setup.py                # Package configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### Code Quality Tools

```bash
# Format code with black
black .

# Lint with flake8
flake8 fibonacci.py fibonacci_cli.py utils.py

# Type checking with mypy
mypy fibonacci.py fibonacci_cli.py utils.py
```

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/test_fibonacci.py

# CLI tests only
pytest tests/test_cli.py
```

### Test Coverage Goals

- Target: >90% code coverage
- All edge cases covered
- Integration tests for CLI commands
- Unit tests for core algorithms

### Example Test Output

```
tests/test_fibonacci.py ................                    [ 50%]
tests/test_cli.py ....................                      [100%]

---------- coverage: platform linux, python 3.10.0 -----------
Name                  Stmts   Miss  Cover
-----------------------------------------
fibonacci.py             45      2    96%
fibonacci_cli.py         78      4    95%
utils.py                 92      5    95%
-----------------------------------------
TOTAL                   215     11    95%
```

## 📚 API Reference

### Core Functions

#### `generate_fibonacci(max_number: int) -> list`

Generates Fibonacci sequence up to the specified maximum value.

**Parameters:**
- `max_number` (int): Maximum value for the sequence (must be >= 0)

**Returns:**
- `list`: List of Fibonacci numbers up to max_number

**Raises:**
- `ValueError`: If max_number is negative
- `TypeError`: If max_number is not an integer

**Example:**
```python
from fibonacci import generate_fibonacci

sequence = generate_fibonacci(100)
print(sequence)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

#### `fibonacci_info(max_number: int) -> dict`

Returns comprehensive information about the Fibonacci sequence.

**Parameters:**
- `max_number` (int): Maximum value for the sequence

**Returns:**
- `dict`: Dictionary with keys: 'sequence', 'count', 'max', 'largest'

**Example:**
```python
from fibonacci import fibonacci_info

info = fibonacci_info(50)
print(info)
# {
#   'sequence': [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
#   'count': 10,
#   'max': 50,
#   'largest': 34
# }
```

### Utility Functions

#### `format_output(sequence, format_type='list', max_number=None, show_count=False) -> str`

Formats Fibonacci sequence according to specified format.

**Parameters:**
- `sequence` (list): Fibonacci sequence to format
- `format_type` (str): Output format ('list', 'inline', or 'json')
- `max_number` (int, optional): Maximum value used for metadata
- `show_count` (bool): Whether to include count in output

**Returns:**
- `str`: Formatted output string

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black .`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all public functions
- Maintain >90% test coverage
- Add examples to documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) - Python CLI framework
- Tested with [pytest](https://pytest.org/) - Python testing framework
- Inspired by the mathematical beauty of the Fibonacci sequence

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/fibonacci-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fibonacci-cli/discussions)
- **Email**: support@example.com

## 🗺️ Roadmap

- [ ] Add support for generating first N Fibonacci numbers (instead of up to max value)
- [ ] Implement caching for repeated calculations
- [ ] Add export to file functionality (CSV, JSON, TXT)
- [ ] Support for custom starting values (generalized Fibonacci)
- [ ] Web API version with REST endpoints
- [ ] GUI version with interactive visualization

---

**Made with ❤️ by the Fibonacci CLI Team**

*Generate beautiful sequences, one number at a time.*
