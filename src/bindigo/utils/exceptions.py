"""
Custom exceptions for Bindigo.

Provides descriptive error types for different failure modes.
"""


class BindigoError(Exception):
    """Base exception for all Bindigo errors."""

    pass


class InputError(BindigoError):
    """Raised when input validation fails."""

    pass


class ProteinError(BindigoError):
    """Raised when protein processing fails."""

    pass


class LigandError(BindigoError):
    """Raised when ligand processing fails."""

    pass


class DockingError(BindigoError):
    """Raised when docking fails."""

    pass


class PredictionError(BindigoError):
    """Raised when ML prediction fails."""

    pass


class DatabaseError(BindigoError):
    """Raised when database fetching fails."""

    pass


class BindingSiteError(BindigoError):
    """Raised when binding site detection fails."""

    pass


class FileFormatError(BindigoError):
    """Raised when file format is invalid or unsupported."""

    pass


class DependencyError(BindigoError):
    """Raised when a required dependency is missing or incompatible."""

    pass
