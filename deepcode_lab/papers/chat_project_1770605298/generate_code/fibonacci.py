"""
Core Fibonacci sequence generator module.

This module provides efficient Fibonacci sequence generation using
an iterative approach with O(n) time complexity and O(1) space complexity
(excluding the output list).
"""


def generate_fibonacci(max_number):
    """
    Generate Fibonacci sequence up to a maximum number.
    
    Uses an iterative approach to generate all Fibonacci numbers
    that are less than or equal to the specified maximum number.
    
    Args:
        max_number (int): Maximum value for numbers in the sequence.
                         Must be >= 0.
    
    Returns:
        list: List of Fibonacci numbers up to max_number.
    
    Raises:
        ValueError: If max_number is negative.
        TypeError: If max_number is not an integer.
    
    Examples:
        >>> generate_fibonacci(0)
        [0]
        >>> generate_fibonacci(1)
        [0, 1, 1]
        >>> generate_fibonacci(10)
        [0, 1, 1, 2, 3, 5, 8]
        >>> generate_fibonacci(100)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    
    Time Complexity: O(n) where n is the count of Fibonacci numbers <= max_number
    Space Complexity: O(k) where k is the length of the result sequence
    """
    # Type validation
    if not isinstance(max_number, int):
        raise TypeError(f"max_number must be an integer, got {type(max_number).__name__}")
    
    # Value validation
    if max_number < 0:
        raise ValueError(f"max_number must be non-negative, got {max_number}")
    
    # Handle edge case: max_number is 0
    if max_number == 0:
        return [0]
    
    # Initialize sequence with first two Fibonacci numbers
    sequence = []
    a, b = 0, 1
    
    # Generate sequence iteratively
    while a <= max_number:
        sequence.append(a)
        a, b = b, a + b
    
    return sequence


def fibonacci_count(max_number):
    """
    Count how many Fibonacci numbers are <= max_number.
    
    Args:
        max_number (int): Maximum value to count up to.
    
    Returns:
        int: Count of Fibonacci numbers in the sequence.
    
    Examples:
        >>> fibonacci_count(100)
        12
        >>> fibonacci_count(0)
        1
    """
    return len(generate_fibonacci(max_number))


def fibonacci_info(max_number):
    """
    Get comprehensive information about Fibonacci sequence up to max_number.
    
    Args:
        max_number (int): Maximum value for the sequence.
    
    Returns:
        dict: Dictionary containing sequence, count, max value, and largest number.
    
    Examples:
        >>> info = fibonacci_info(20)
        >>> info['count']
        8
        >>> info['largest']
        13
    """
    sequence = generate_fibonacci(max_number)
    return {
        'sequence': sequence,
        'count': len(sequence),
        'max': max_number,
        'largest': sequence[-1] if sequence else None
    }
