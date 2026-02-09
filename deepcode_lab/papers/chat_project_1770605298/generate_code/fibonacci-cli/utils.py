"""
Utility functions for Fibonacci CLI tool.

This module provides validation, formatting, and helper functions
for the Fibonacci sequence generator CLI application.
"""

import json
from typing import Any, Dict, List, Union


def validate_max_number(value: Any) -> int:
    """
    Validate the max_number parameter for Fibonacci generation.
    
    Args:
        value: The value to validate (should be convertible to int)
        
    Returns:
        int: The validated integer value
        
    Raises:
        ValueError: If value is negative or cannot be converted to int
        TypeError: If value is None or invalid type
    """
    if value is None:
        raise TypeError("max_number cannot be None")
    
    try:
        max_num = int(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"max_number must be an integer, got: {type(value).__name__}") from e
    
    if max_num < 0:
        raise ValueError(f"max_number must be non-negative (>= 0), got: {max_num}")
    
    return max_num


def format_sequence_list(sequence: List[int]) -> str:
    """
    Format Fibonacci sequence as a Python list string.
    
    Args:
        sequence: List of Fibonacci numbers
        
    Returns:
        str: Formatted string representation like "[0, 1, 1, 2, 3, 5]"
    """
    return str(sequence)


def format_sequence_inline(sequence: List[int]) -> str:
    """
    Format Fibonacci sequence as comma-separated inline string.
    
    Args:
        sequence: List of Fibonacci numbers
        
    Returns:
        str: Comma-separated string like "0, 1, 1, 2, 3, 5"
    """
    return ", ".join(map(str, sequence))


def format_sequence_json(sequence: List[int], max_number: int, include_metadata: bool = True) -> str:
    """
    Format Fibonacci sequence as JSON string.
    
    Args:
        sequence: List of Fibonacci numbers
        max_number: The maximum number used to generate the sequence
        include_metadata: Whether to include count and max in output
        
    Returns:
        str: JSON formatted string with sequence and metadata
    """
    if include_metadata:
        data = {
            "sequence": sequence,
            "count": len(sequence),
            "max": max_number
        }
    else:
        data = {"sequence": sequence}
    
    return json.dumps(data, indent=2)


def format_output(sequence: List[int], format_type: str = "list", 
                  max_number: int = None, show_count: bool = False) -> str:
    """
    Format Fibonacci sequence according to specified format type.
    
    Args:
        sequence: List of Fibonacci numbers
        format_type: Output format - 'list', 'inline', or 'json'
        max_number: The maximum number used (required for json format)
        show_count: Whether to append count information
        
    Returns:
        str: Formatted output string
        
    Raises:
        ValueError: If format_type is invalid or max_number missing for json
    """
    valid_formats = ["list", "inline", "json"]
    if format_type not in valid_formats:
        raise ValueError(f"Invalid format type '{format_type}'. Must be one of: {valid_formats}")
    
    # Generate base output
    if format_type == "list":
        output = format_sequence_list(sequence)
    elif format_type == "inline":
        output = format_sequence_inline(sequence)
    elif format_type == "json":
        if max_number is None:
            raise ValueError("max_number is required for json format")
        output = format_sequence_json(sequence, max_number)
    
    # Add count if requested (not for json, as it's already included)
    if show_count and format_type != "json":
        count_line = f"\nTotal numbers: {len(sequence)}"
        output += count_line
    
    return output


def get_error_message(error: Exception, context: str = "") -> str:
    """
    Generate user-friendly error message from exception.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
        
    Returns:
        str: Formatted error message for display to user
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"Error in {context}: {error_msg}"
    else:
        return f"{error_type}: {error_msg}"


def validate_format_type(format_type: str) -> str:
    """
    Validate the output format type parameter.
    
    Args:
        format_type: The format type to validate
        
    Returns:
        str: The validated format type (lowercase)
        
    Raises:
        ValueError: If format_type is not valid
    """
    valid_formats = ["list", "inline", "json"]
    format_lower = format_type.lower()
    
    if format_lower not in valid_formats:
        raise ValueError(
            f"Invalid format '{format_type}'. "
            f"Valid options are: {', '.join(valid_formats)}"
        )
    
    return format_lower


def create_success_response(sequence: List[int], max_number: int) -> Dict[str, Any]:
    """
    Create a standardized success response dictionary.
    
    Args:
        sequence: The generated Fibonacci sequence
        max_number: The maximum number parameter used
        
    Returns:
        dict: Response dictionary with status, data, and metadata
    """
    return {
        "status": "success",
        "data": {
            "sequence": sequence,
            "count": len(sequence),
            "max_number": max_number,
            "largest_value": sequence[-1] if sequence else None
        }
    }


def create_error_response(error: Exception, max_number: Any = None) -> Dict[str, Any]:
    """
    Create a standardized error response dictionary.
    
    Args:
        error: The exception that occurred
        max_number: The max_number value that caused the error (if applicable)
        
    Returns:
        dict: Response dictionary with status, error info, and context
    """
    return {
        "status": "error",
        "error": {
            "type": type(error).__name__,
            "message": str(error),
            "max_number": max_number
        }
    }


def is_valid_integer_string(value: str) -> bool:
    """
    Check if a string can be converted to a valid integer.
    
    Args:
        value: String to check
        
    Returns:
        bool: True if string represents a valid integer, False otherwise
    """
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def truncate_sequence_display(sequence: List[int], max_display: int = 50) -> str:
    """
    Truncate long sequences for display purposes.
    
    Args:
        sequence: List of Fibonacci numbers
        max_display: Maximum number of elements to display
        
    Returns:
        str: Formatted string with truncation indicator if needed
    """
    if len(sequence) <= max_display:
        return format_sequence_inline(sequence)
    
    truncated = sequence[:max_display]
    remaining = len(sequence) - max_display
    return f"{format_sequence_inline(truncated)} ... ({remaining} more)"


# Constants for validation
MIN_MAX_NUMBER = 0
MAX_SAFE_INTEGER = 10**15  # Practical limit for Fibonacci generation


def validate_max_number_range(max_number: int) -> None:
    """
    Validate that max_number is within safe operational range.
    
    Args:
        max_number: The maximum number to validate
        
    Raises:
        ValueError: If max_number is outside safe range
    """
    if max_number < MIN_MAX_NUMBER:
        raise ValueError(f"max_number must be at least {MIN_MAX_NUMBER}")
    
    if max_number > MAX_SAFE_INTEGER:
        raise ValueError(
            f"max_number {max_number} exceeds safe limit of {MAX_SAFE_INTEGER}. "
            f"This may cause performance issues."
        )
