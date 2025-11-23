"""
Test version information.
"""

import bindigo
from bindigo.__version__ import __version__, __version_info__


def test_version_exists():
    """Test that version exists."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_version_format():
    """Test version format is semantic versioning."""
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)


def test_version_info():
    """Test version_info tuple."""
    assert isinstance(__version_info__, tuple)
    assert len(__version_info__) == 3
    assert all(isinstance(part, int) for part in __version_info__)


def test_package_version():
    """Test that package exports version."""
    assert hasattr(bindigo, "__version__")
    assert bindigo.__version__ == __version__


def test_version_consistency():
    """Test that version matches version_info."""
    expected_version = ".".join(str(i) for i in __version_info__)
    assert __version__ == expected_version
