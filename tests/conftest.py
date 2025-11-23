"""
Pytest configuration and fixtures for Bindigo tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_pdb_id():
    """Return a valid PDB ID for testing."""
    return "1HSG"


@pytest.fixture
def valid_smiles():
    """Return a valid SMILES string for testing."""
    return "CC(=O)Nc1ccc(O)cc1"  # Acetaminophen


@pytest.fixture
def invalid_smiles():
    """Return an invalid SMILES string for testing."""
    return "CC(=O"  # Unmatched parenthesis


@pytest.fixture
def invalid_pdb_id():
    """Return an invalid PDB ID for testing."""
    return "ABCD"  # Invalid format: doesn't start with digit


@pytest.fixture
def temp_output_dir(tmp_path):
    """Return a temporary directory for test outputs."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
