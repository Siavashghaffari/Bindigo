"""
Test package imports.
"""

import pytest


def test_import_bindigo():
    """Test that bindigo package can be imported."""
    import bindigo
    assert bindigo is not None


def test_import_version():
    """Test that version info can be imported."""
    from bindigo import __version__
    assert __version__ is not None


def test_import_cli_main():
    """Test that CLI main can be imported."""
    from bindigo.cli.main import cli
    assert cli is not None


def test_import_utils_validation():
    """Test that validation utilities can be imported."""
    from bindigo.utils.validation import validate_protein_input
    assert validate_protein_input is not None


def test_import_utils_exceptions():
    """Test that exceptions can be imported."""
    from bindigo.utils.exceptions import BindigoError
    assert BindigoError is not None


def test_import_core_config():
    """Test that config can be imported."""
    from bindigo.core.config import config
    assert config is not None


def test_import_core_pipeline():
    """Test that pipeline can be imported."""
    from bindigo.core.pipeline import run_prediction
    assert run_prediction is not None


def test_all_submodules_importable():
    """Test that all submodules can be imported."""
    submodules = [
        "bindigo.cli",
        "bindigo.core",
        "bindigo.preprocessing",
        "bindigo.docking",
        "bindigo.ml",
        "bindigo.database",
        "bindigo.visualization",
        "bindigo.utils",
    ]

    for module_name in submodules:
        module = __import__(module_name, fromlist=[""])
        assert module is not None
