"""
I/O utilities for Bindigo.

Provides functions for reading and writing files.
"""

import csv
from pathlib import Path
from typing import Dict, List, Any
import json


def write_csv(filepath: Path, data: List[Dict[str, Any]], headers: List[str]) -> None:
    """
    Write data to CSV file.

    Args:
        filepath: Output file path
        data: List of dictionaries containing row data
        headers: List of column headers

    Raises:
        IOError: If writing fails
    """
    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        raise IOError(f"Failed to write CSV file {filepath}: {e}")


def read_csv(filepath: Path) -> List[Dict[str, Any]]:
    """
    Read CSV file into list of dictionaries.

    Args:
        filepath: Input file path

    Returns:
        List of dictionaries, one per row

    Raises:
        IOError: If reading fails
    """
    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        raise IOError(f"Failed to read CSV file {filepath}: {e}")


def write_json(filepath: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Write data to JSON file.

    Args:
        filepath: Output file path
        data: Dictionary to write
        indent: Indentation level for pretty printing

    Raises:
        IOError: If writing fails
    """
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=indent)
    except Exception as e:
        raise IOError(f"Failed to write JSON file {filepath}: {e}")


def read_json(filepath: Path) -> Dict[str, Any]:
    """
    Read JSON file into dictionary.

    Args:
        filepath: Input file path

    Returns:
        Dictionary containing JSON data

    Raises:
        IOError: If reading fails
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Failed to read JSON file {filepath}: {e}")


def ensure_directory(dirpath: Path) -> None:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        dirpath: Directory path to ensure

    Raises:
        IOError: If directory creation fails
    """
    try:
        dirpath.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise IOError(f"Failed to create directory {dirpath}: {e}")
