"""
Setup configuration for Fibonacci CLI Generator.

This setup file enables the Fibonacci CLI tool to be installed as a Python package
with a command-line entry point, making it accessible system-wide as 'fibonacci'.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements from requirements.txt
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

# Extract only runtime requirements (exclude test dependencies)
runtime_requirements = [
    req for req in requirements 
    if not any(test_pkg in req.lower() for test_pkg in ["pytest", "coverage", "black", "flake8", "mypy"])
]

# Test requirements
test_requirements = [
    req for req in requirements 
    if any(test_pkg in req.lower() for test_pkg in ["pytest", "coverage"])
]

# Development requirements
dev_requirements = test_requirements + [
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

setup(
    name="fibonacci-cli",
    version="1.0.0",
    author="Fibonacci CLI Team",
    author_email="fibonacci-cli@example.com",
    description="A Python CLI tool for generating Fibonacci sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fibonacci-cli",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/fibonacci-cli/issues",
        "Documentation": "https://github.com/yourusername/fibonacci-cli#readme",
        "Source Code": "https://github.com/yourusername/fibonacci-cli",
    },
    
    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*"]),
    py_modules=["fibonacci", "utils", "fibonacci_cli"],
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=runtime_requirements,
    
    # Optional dependencies
    extras_require={
        "test": test_requirements,
        "dev": dev_requirements,
        "color": ["colorama>=0.4.6"],
        "rich": ["rich>=13.0.0"],
        "all": dev_requirements + ["colorama>=0.4.6", "rich>=13.0.0"],
    },
    
    # Entry points for CLI commands
    entry_points={
        "console_scripts": [
            "fibonacci=fibonacci_cli:main",
            "fib=fibonacci_cli:main",  # Short alias
        ],
    },
    
    # Package metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    
    keywords=[
        "fibonacci",
        "cli",
        "command-line",
        "sequence",
        "mathematics",
        "generator",
        "click",
        "tool",
    ],
    
    # Include additional files
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.rst"],
    },
    
    # Zip safety
    zip_safe=False,
    
    # License
    license="MIT",
    
    # Platforms
    platforms=["any"],
)
