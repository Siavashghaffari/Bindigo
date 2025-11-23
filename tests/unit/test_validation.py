"""
Test input validation utilities.
"""

import pytest
from pathlib import Path

from bindigo.utils.validation import (
    is_pdb_id,
    is_smiles,
    validate_protein_input,
    validate_ligand_input,
    validate_binding_site,
    validate_output_path,
)
from bindigo.utils.exceptions import InputError, FileFormatError


class TestPDBIDValidation:
    """Test PDB ID validation."""

    def test_valid_pdb_ids(self):
        """Test valid PDB ID formats."""
        valid_ids = ["1HSG", "3ERT", "4AGQ", "5a1b", "6XYZ"]
        for pdb_id in valid_ids:
            assert is_pdb_id(pdb_id)

    def test_invalid_pdb_ids(self):
        """Test invalid PDB ID formats."""
        invalid_ids = ["ABC", "12345", "ABCD", "1HS", "protein.pdb"]
        for pdb_id in invalid_ids:
            assert not is_pdb_id(pdb_id)


class TestSMILESValidation:
    """Test SMILES validation."""

    def test_valid_smiles(self, valid_smiles):
        """Test valid SMILES strings."""
        assert is_smiles(valid_smiles)
        assert is_smiles("CCO")
        assert is_smiles("c1ccccc1")

    def test_file_paths_not_smiles(self):
        """Test that file paths are not detected as SMILES."""
        assert not is_smiles("ligand.sdf")
        assert not is_smiles("compound.mol2")
        assert not is_smiles("./data/ligand.pdb")


class TestProteinInputValidation:
    """Test protein input validation."""

    def test_valid_pdb_id(self, valid_pdb_id):
        """Test validation of valid PDB ID."""
        input_type, validated = validate_protein_input(valid_pdb_id)
        assert input_type == "pdb_id"
        assert validated == valid_pdb_id.upper()

    def test_invalid_pdb_id_raises_error(self, invalid_pdb_id):
        """Test that invalid PDB ID raises error."""
        with pytest.raises(InputError):
            validate_protein_input(invalid_pdb_id)

    def test_nonexistent_file_raises_error(self):
        """Test that nonexistent file raises error."""
        with pytest.raises(InputError):
            validate_protein_input("nonexistent.pdb")


class TestLigandInputValidation:
    """Test ligand input validation."""

    def test_valid_smiles(self, valid_smiles):
        """Test validation of valid SMILES."""
        input_type, validated = validate_ligand_input(valid_smiles)
        assert input_type == "smiles"
        assert validated == valid_smiles

    def test_nonexistent_file_defaults_to_smiles(self):
        """Test that nonexistent file path is treated as SMILES if valid."""
        input_type, validated = validate_ligand_input("CCO")
        assert input_type == "smiles"


class TestBindingSiteValidation:
    """Test binding site validation."""

    def test_valid_center_and_size(self):
        """Test valid binding site parameters."""
        validate_binding_site((10.0, 20.0, 30.0), 25.0)

    def test_none_center_is_valid(self):
        """Test that None center (auto-detect) is valid."""
        validate_binding_site(None, 20.0)

    def test_invalid_size_raises_error(self):
        """Test that invalid size raises error."""
        with pytest.raises(InputError):
            validate_binding_site(None, 0.0)

        with pytest.raises(InputError):
            validate_binding_site(None, -5.0)

    def test_too_large_size_raises_error(self):
        """Test that too large size raises error."""
        with pytest.raises(InputError):
            validate_binding_site(None, 150.0)

    def test_wrong_number_of_coordinates_raises_error(self):
        """Test that wrong number of coordinates raises error."""
        with pytest.raises(InputError):
            validate_binding_site((10.0, 20.0), 20.0)


class TestOutputPathValidation:
    """Test output path validation."""

    def test_valid_csv_path(self, temp_output_dir):
        """Test valid CSV output path."""
        output_path = temp_output_dir / "results.csv"
        validated = validate_output_path(str(output_path))
        assert validated.suffix == ".csv"

    def test_adds_csv_extension_if_missing(self, temp_output_dir):
        """Test that .csv extension is added if missing."""
        output_path = temp_output_dir / "results"
        validated = validate_output_path(str(output_path))
        assert validated.suffix == ".csv"

    def test_invalid_extension_raises_error(self, temp_output_dir):
        """Test that invalid extension raises error."""
        output_path = temp_output_dir / "results.txt"
        with pytest.raises(InputError):
            validate_output_path(str(output_path))

    def test_nonexistent_directory_raises_error(self):
        """Test that nonexistent directory raises error."""
        with pytest.raises(InputError):
            validate_output_path("/nonexistent/dir/results.csv")
