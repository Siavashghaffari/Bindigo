"""
Test AutoDock Vina discovery and availability checks.
"""

import os
import stat

import pytest

from bindigo.docking.vina import (
    VINA_PATH_ENV_VAR,
    check_vina_available,
    find_vina_executable,
    is_vina_available,
)
from bindigo.utils.exceptions import BindigoError, DependencyError


def _make_fake_vina(directory):
    """Create executable files named like a Vina binary and return the dir."""
    paths = []
    for name in ("vina", "vina.exe"):
        path = directory / name
        path.write_text("#!/bin/sh\necho fake vina\n")
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        paths.append(path)
    return paths


@pytest.fixture
def without_vina(monkeypatch, tmp_path):
    """Simulate a system where AutoDock Vina is not installed."""
    empty_dir = tmp_path / "empty_path"
    empty_dir.mkdir()
    monkeypatch.delenv(VINA_PATH_ENV_VAR, raising=False)
    monkeypatch.setenv("PATH", str(empty_dir))
    monkeypatch.chdir(empty_dir)


@pytest.fixture
def with_vina(monkeypatch, tmp_path):
    """Simulate a system where AutoDock Vina is on PATH."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _make_fake_vina(bin_dir)
    monkeypatch.delenv(VINA_PATH_ENV_VAR, raising=False)
    monkeypatch.setenv("PATH", str(bin_dir))
    return bin_dir


class TestFindVinaExecutable:
    """Test locating the Vina executable."""

    def test_returns_none_when_missing(self, without_vina):
        """Vina is not found when it is not installed."""
        assert find_vina_executable() is None

    def test_finds_vina_on_path(self, with_vina):
        """Vina is found when it is on PATH."""
        found = find_vina_executable()
        assert found is not None
        assert "vina" in os.path.basename(found).lower()

    def test_env_var_overrides_path(self, without_vina, monkeypatch, tmp_path):
        """BINDIGO_VINA_PATH points Bindigo at a binary that is not on PATH."""
        custom_dir = tmp_path / "custom"
        custom_dir.mkdir()
        binaries = _make_fake_vina(custom_dir)
        monkeypatch.setenv(VINA_PATH_ENV_VAR, str(binaries[0]))

        found = find_vina_executable()
        assert found is not None
        assert os.path.basename(found).lower().startswith("vina")

    def test_env_var_pointing_nowhere_returns_none(
        self, without_vina, monkeypatch, tmp_path
    ):
        """A bad BINDIGO_VINA_PATH does not silently fall back to PATH."""
        monkeypatch.setenv(VINA_PATH_ENV_VAR, str(tmp_path / "nope" / "vina"))
        assert find_vina_executable() is None


class TestIsVinaAvailable:
    """Test the boolean availability helper."""

    def test_false_when_missing(self, without_vina):
        assert is_vina_available() is False

    def test_true_when_present(self, with_vina):
        assert is_vina_available() is True


class TestCheckVinaAvailable:
    """Test the raising availability check."""

    def test_returns_path_when_present(self, with_vina):
        """The check returns the resolved path when Vina is installed."""
        assert check_vina_available() is not None

    def test_raises_dependency_error_when_missing(self, without_vina):
        """A missing binary raises DependencyError, not an arbitrary error."""
        with pytest.raises(DependencyError):
            check_vina_available()

    def test_dependency_error_is_a_bindigo_error(self, without_vina):
        """The CLI catches BindigoError, so the check must raise one."""
        with pytest.raises(BindigoError):
            check_vina_available()

    def test_message_says_what_is_missing(self, without_vina):
        """The message itself is a short, plain explanation."""
        with pytest.raises(DependencyError) as exc_info:
            check_vina_available()

        message = str(exc_info.value)
        assert "AutoDock Vina" in message
        assert "PATH" in message

    def test_details_are_actionable(self, without_vina):
        """The attached details explain how to install Vina."""
        with pytest.raises(DependencyError) as exc_info:
            check_vina_available()

        details = exc_info.value.details
        assert details is not None
        assert "cannot be installed with pip" in details
        assert "conda install -c conda-forge vina" in details
        assert "github.com/ccsb-scripps/AutoDock-Vina" in details
        assert VINA_PATH_ENV_VAR in details

    def test_message_names_the_bad_override_path(
        self, without_vina, monkeypatch, tmp_path
    ):
        """A bad override path is echoed back so the typo is obvious."""
        bad_path = str(tmp_path / "nope" / "vina")
        monkeypatch.setenv(VINA_PATH_ENV_VAR, bad_path)

        with pytest.raises(DependencyError) as exc_info:
            check_vina_available()

        assert bad_path in str(exc_info.value)
