"""
Test custom exceptions.
"""

import pytest
from bindigo.utils.exceptions import (
    BindigoError,
    InputError,
    ProteinError,
    LigandError,
    DockingError,
    PredictionError,
    DatabaseError,
    BindingSiteError,
    FileFormatError,
    DependencyError,
)


def test_base_exception():
    """Test base BindigoError."""
    error = BindigoError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_all_exceptions_inherit_from_base():
    """Test that all exceptions inherit from BindigoError."""
    exception_classes = [
        InputError,
        ProteinError,
        LigandError,
        DockingError,
        PredictionError,
        DatabaseError,
        BindingSiteError,
        FileFormatError,
        DependencyError,
    ]

    for exc_class in exception_classes:
        error = exc_class("Test")
        assert isinstance(error, BindigoError)
        assert isinstance(error, Exception)


def test_exceptions_are_raisable():
    """Test that exceptions can be raised and caught."""
    with pytest.raises(InputError):
        raise InputError("Invalid input")

    with pytest.raises(ProteinError):
        raise ProteinError("Protein processing failed")

    with pytest.raises(DockingError):
        raise DockingError("Docking failed")
