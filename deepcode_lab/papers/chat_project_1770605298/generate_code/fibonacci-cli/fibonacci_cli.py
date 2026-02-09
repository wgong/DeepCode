#!/usr/bin/env python3
"""
Fibonacci CLI - Command-line tool for generating Fibonacci sequences

This module provides the main CLI interface using Click framework for generating
Fibonacci sequences up to a specified maximum number with various output formats.

Usage:
    fibonacci --max-number 100
    fibonacci --max-number 100 --count
    fibonacci --max-number 50 --format inline
    fibonacci --max-number 20 --format json
"""

import sys
import click
from typing import Optional

# Import core Fibonacci logic
try:
    from fibonacci import generate_fibonacci, fibonacci_info
except ImportError:
    # Handle case where fibonacci.py is in parent directory
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from fibonacci import generate_fibonacci, fibonacci_info

# Import utility functions
from utils import (
    validate_max_number,
    validate_format_type,
    format_output,
    get_error_message,
    create_error_response,
    create_success_response,
    MAX_SAFE_INTEGER
)


# CLI Configuration
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--max-number',
    '-m',
    type=int,
    required=True,
    help='Maximum value for Fibonacci sequence (must be >= 0).',
    metavar='INTEGER'
)
@click.option(
    '--format',
    '-f',
    'output_format',
    type=click.Choice(['list', 'inline', 'json'], case_sensitive=False),
    default='list',
    help='Output format: list (default), inline (comma-separated), or json.',
    show_default=True
)
@click.option(
    '--count',
    '-c',
    is_flag=True,
    default=False,
    help='Display the count of numbers in the sequence.'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    default=False,
    help='Enable verbose output with additional information.'
)
@click.version_option(version='1.0.0', prog_name='Fibonacci CLI')
def fibonacci_command(max_number: int, output_format: str, count: bool, verbose: bool):
    """
    Generate Fibonacci sequence up to MAX_NUMBER.
    
    The Fibonacci sequence starts with 0 and 1, and each subsequent number
    is the sum of the previous two numbers. This tool generates all Fibonacci
    numbers that are less than or equal to the specified maximum value.
    
    Examples:
    
        \b
        # Generate Fibonacci numbers up to 100
        $ fibonacci --max-number 100
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        
        \b
        # Show count of numbers
        $ fibonacci --max-number 100 --count
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        Total numbers: 12
        
        \b
        # Inline format (comma-separated)
        $ fibonacci --max-number 50 --format inline
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34
        
        \b
        # JSON format with metadata
        $ fibonacci --max-number 20 --format json
        {"sequence": [0, 1, 1, 2, 3, 5, 8, 13], "count": 8, "max": 20}
    
    Edge Cases:
        - max_number = 0: Returns [0]
        - max_number = 1: Returns [0, 1, 1]
        - Negative numbers: Error (Fibonacci sequence starts at 0)
    """
    try:
        # Verbose mode: Show input parameters
        if verbose:
            click.echo(f"Input Parameters:", err=True)
            click.echo(f"  Max Number: {max_number}", err=True)
            click.echo(f"  Format: {output_format}", err=True)
            click.echo(f"  Show Count: {count}", err=True)
            click.echo("", err=True)
        
        # Validate max_number
        try:
            validated_max = validate_max_number(max_number)
        except (ValueError, TypeError) as e:
            raise click.BadParameter(str(e), param_hint='--max-number')
        
        # Check for extremely large values (performance warning)
        if validated_max > MAX_SAFE_INTEGER:
            click.echo(
                f"Warning: max_number ({validated_max}) exceeds recommended limit "
                f"({MAX_SAFE_INTEGER}). Generation may be slow.",
                err=True
            )
            if not click.confirm("Do you want to continue?", default=False):
                click.echo("Operation cancelled.", err=True)
                sys.exit(1)
        
        # Validate format type
        try:
            validated_format = validate_format_type(output_format)
        except ValueError as e:
            raise click.BadParameter(str(e), param_hint='--format')
        
        # Generate Fibonacci sequence
        if verbose:
            click.echo("Generating Fibonacci sequence...", err=True)
        
        sequence = generate_fibonacci(validated_max)
        
        if verbose:
            click.echo(f"Generated {len(sequence)} numbers.", err=True)
            click.echo("", err=True)
        
        # Format and display output
        formatted_output = format_output(
            sequence=sequence,
            format_type=validated_format,
            max_number=validated_max,
            show_count=count
        )
        
        click.echo(formatted_output)
        
        # Display count if requested (for non-JSON formats)
        if count and validated_format != 'json':
            click.echo(f"Total numbers: {len(sequence)}")
        
        # Verbose mode: Show additional statistics
        if verbose:
            click.echo("", err=True)
            click.echo("Statistics:", err=True)
            click.echo(f"  Sequence Length: {len(sequence)}", err=True)
            click.echo(f"  Largest Number: {sequence[-1] if sequence else 0}", err=True)
            click.echo(f"  Smallest Number: {sequence[0] if sequence else 0}", err=True)
        
        # Exit with success code
        sys.exit(0)
        
    except click.BadParameter:
        # Re-raise Click exceptions to let Click handle them
        raise
    
    except ValueError as e:
        # Handle validation errors
        error_msg = get_error_message(e, context="validation")
        click.echo(f"Error: {error_msg}", err=True)
        if verbose:
            click.echo(f"Details: {str(e)}", err=True)
        sys.exit(1)
    
    except TypeError as e:
        # Handle type errors
        error_msg = get_error_message(e, context="type validation")
        click.echo(f"Error: {error_msg}", err=True)
        if verbose:
            click.echo(f"Details: {str(e)}", err=True)
        sys.exit(1)
    
    except MemoryError:
        # Handle memory errors for very large sequences
        click.echo(
            f"Error: Insufficient memory to generate Fibonacci sequence up to {max_number}. "
            f"Try a smaller value.",
            err=True
        )
        sys.exit(1)
    
    except KeyboardInterrupt:
        # Handle user interruption gracefully
        click.echo("\nOperation cancelled by user.", err=True)
        sys.exit(130)  # Standard exit code for SIGINT
    
    except Exception as e:
        # Handle unexpected errors
        error_msg = get_error_message(e, context="execution")
        click.echo(f"Unexpected error: {error_msg}", err=True)
        if verbose:
            click.echo(f"Exception type: {type(e).__name__}", err=True)
            click.echo(f"Details: {str(e)}", err=True)
        sys.exit(1)


# Additional helper command for testing
@click.command(name='fibonacci-info')
@click.option(
    '--max-number',
    '-m',
    type=int,
    required=True,
    help='Maximum value for Fibonacci sequence.'
)
def fibonacci_info_command(max_number: int):
    """
    Display detailed information about Fibonacci sequence up to MAX_NUMBER.
    
    This command provides comprehensive metadata including sequence,
    count, largest number, and other statistics in JSON format.
    """
    try:
        validated_max = validate_max_number(max_number)
        info = fibonacci_info(validated_max)
        
        # Format as JSON
        import json
        output = json.dumps(info, indent=2)
        click.echo(output)
        sys.exit(0)
        
    except (ValueError, TypeError) as e:
        click.echo(f"Error: {get_error_message(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {get_error_message(e)}", err=True)
        sys.exit(1)


# CLI Group (for potential future subcommands)
@click.group()
def cli():
    """Fibonacci CLI Tool - Generate and analyze Fibonacci sequences."""
    pass


# Register commands
cli.add_command(fibonacci_command, name='generate')
cli.add_command(fibonacci_info_command, name='info')


# Main entry point
def main():
    """Main entry point for the CLI application."""
    # Use the main fibonacci_command as default
    fibonacci_command()


if __name__ == '__main__':
    main()
