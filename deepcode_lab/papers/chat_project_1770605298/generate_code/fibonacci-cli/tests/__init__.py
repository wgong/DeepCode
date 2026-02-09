"""
Fibonacci CLI Test Suite
=========================

This package contains comprehensive unit and integration tests for the Fibonacci CLI Generator.

Test Modules:
- test_fibonacci.py: Unit tests for core Fibonacci generation logic
- test_cli.py: Integration tests for CLI commands and options

Test Coverage Goals:
- Overall coverage: >90%
- Core logic (fibonacci.py): 100%
- CLI interface (fibonacci_cli.py): >85%
- Utilities (utils.py): >90%

Running Tests:
--------------
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test module
pytest tests/test_fibonacci.py
pytest tests/test_cli.py

# Run with verbose output
pytest -v

# Run specific test function
pytest tests/test_fibonacci.py::test_generate_fibonacci_basic
"""

import sys
from pathlib import Path

# Add parent directory to path to allow importing project modules
# This ensures tests can import fibonacci, utils, and fibonacci_cli
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Shared test fixtures and utilities
# ===================================

def get_test_data_path():
    """
    Returns the path to test data directory if it exists.
    
    Returns:
        Path: Path object pointing to tests/data directory
    """
    return Path(__file__).parent / "data"


# Common test constants
# =====================

# Expected Fibonacci sequences for various max_number values
EXPECTED_SEQUENCES = {
    0: [0],
    1: [0, 1, 1],
    2: [0, 1, 1, 2],
    5: [0, 1, 1, 2, 3, 5],
    10: [0, 1, 1, 2, 3, 5, 8],
    20: [0, 1, 1, 2, 3, 5, 8, 13],
    50: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
    100: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
    1000: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987],
}

# Edge case test values
EDGE_CASES = {
    "zero": 0,
    "one": 1,
    "small": 10,
    "medium": 1000,
    "large": 1000000,
}

# Invalid input test cases
INVALID_INPUTS = {
    "negative": -1,
    "negative_large": -100,
    "string": "not_a_number",
    "float": 10.5,
    "none": None,
}

# CLI exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_INTERRUPT = 130


# Test helper functions
# =====================

def is_fibonacci_sequence(sequence):
    """
    Validates that a sequence follows Fibonacci rules.
    
    Args:
        sequence (list): List of integers to validate
        
    Returns:
        bool: True if sequence is valid Fibonacci, False otherwise
    """
    if not sequence:
        return False
    
    if len(sequence) == 1:
        return sequence[0] == 0
    
    if len(sequence) == 2:
        return sequence == [0, 1]
    
    # Check that each number is sum of previous two
    for i in range(2, len(sequence)):
        if sequence[i] != sequence[i-1] + sequence[i-2]:
            return False
    
    return True


def verify_sequence_properties(sequence, max_number):
    """
    Verifies that a Fibonacci sequence meets all expected properties.
    
    Args:
        sequence (list): Generated Fibonacci sequence
        max_number (int): Maximum value constraint
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check sequence is not empty
    if not sequence:
        return False, "Sequence is empty"
    
    # Check first element is 0
    if sequence[0] != 0:
        return False, f"First element should be 0, got {sequence[0]}"
    
    # Check all elements are <= max_number
    for num in sequence:
        if num > max_number:
            return False, f"Element {num} exceeds max_number {max_number}"
    
    # Check Fibonacci property
    if not is_fibonacci_sequence(sequence):
        return False, "Sequence does not follow Fibonacci rules"
    
    # Check that next Fibonacci number would exceed max_number
    if len(sequence) >= 2:
        next_fib = sequence[-1] + sequence[-2]
        if next_fib <= max_number:
            return False, f"Sequence incomplete: next Fibonacci {next_fib} <= {max_number}"
    
    return True, "Valid"


def format_test_output(test_name, passed, details=""):
    """
    Formats test output for readable console display.
    
    Args:
        test_name (str): Name of the test
        passed (bool): Whether test passed
        details (str): Additional details about the test
        
    Returns:
        str: Formatted test output string
    """
    status = "✓ PASS" if passed else "✗ FAIL"
    output = f"{status}: {test_name}"
    if details:
        output += f"\n  Details: {details}"
    return output


# Version information
__version__ = "1.0.0"
__author__ = "Fibonacci CLI Team"
__test_suite__ = "Fibonacci CLI Test Suite"

# Export commonly used test utilities
__all__ = [
    "EXPECTED_SEQUENCES",
    "EDGE_CASES",
    "INVALID_INPUTS",
    "EXIT_SUCCESS",
    "EXIT_ERROR",
    "EXIT_INTERRUPT",
    "is_fibonacci_sequence",
    "verify_sequence_properties",
    "format_test_output",
    "get_test_data_path",
]
