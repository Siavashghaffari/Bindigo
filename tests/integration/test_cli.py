"""
Integration tests for CLI commands.
"""

import pytest
from click.testing import CliRunner

from bindigo.cli.main import cli


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


class TestMainCLI:
    """Test main CLI functionality."""

    def test_version_option(self, runner):
        """Test --version option."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help_option(self, runner):
        """Test --help option."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Bindigo" in result.output
        assert "predict" in result.output
        assert "info" in result.output

    def test_no_command_shows_help(self, runner):
        """Test that running with no command shows help."""
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert "Commands:" in result.output


class TestPredictCommand:
    """Test predict command."""

    def test_predict_help(self, runner):
        """Test predict --help."""
        result = runner.invoke(cli, ["predict", "--help"])
        assert result.exit_code == 0
        assert "Predict protein-ligand binding affinity" in result.output
        assert "--protein" in result.output
        assert "--ligand" in result.output
        assert "--output" in result.output

    def test_predict_missing_required_args(self, runner):
        """Test predict with missing required arguments."""
        result = runner.invoke(cli, ["predict"])
        assert result.exit_code != 0
        assert "Error" in result.output or "Missing" in result.output

    def test_predict_with_invalid_protein(self, runner, tmp_path):
        """Test predict with invalid protein input."""
        output = tmp_path / "results.csv"
        result = runner.invoke(
            cli,
            [
                "predict",
                "--protein",
                "INVALID",
                "--ligand",
                "CCO",
                "--output",
                str(output),
            ],
        )
        # Should fail validation
        assert result.exit_code != 0


class TestInfoCommand:
    """Test info command."""

    def test_info_version(self, runner):
        """Test info --version."""
        result = runner.invoke(cli, ["info", "--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
        assert "Bindigo Package Information" in result.output

    def test_info_models(self, runner):
        """Test info --models."""
        result = runner.invoke(cli, ["info", "--models"])
        assert result.exit_code == 0
        assert "Available ML Models" in result.output

    def test_info_cite(self, runner):
        """Test info --cite."""
        result = runner.invoke(cli, ["info", "--cite"])
        assert result.exit_code == 0
        assert "Citation" in result.output
        assert "AutoDock Vina" in result.output

    def test_info_no_flags_shows_all(self, runner):
        """Test info with no flags shows all information."""
        result = runner.invoke(cli, ["info"])
        assert result.exit_code == 0
        assert "Version" in result.output
        assert "Available ML Models" in result.output
        assert "Citation" in result.output
