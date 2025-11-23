"""
Input validation utilities for Bindigo.

Provides functions to validate user inputs before processing.
"""

import re
from pathlib import Path
from typing import Optional, Tuple

from bindigo.utils.exceptions import InputError, FileFormatError


def is_pdb_id(protein: str) -> bool:
    """
    Check if string is a valid PDB ID format.

    Args:
        protein: String to check

    Returns:
        True if matches PDB ID format (4 alphanumeric characters)
    """
    # PDB IDs are 4 characters: digit followed by 3 alphanumeric
    pattern = r"^[0-9][A-Za-z0-9]{3}$"
    return bool(re.match(pattern, protein))


def is_smiles(ligand: str) -> bool:
    """
    Check if string is likely a SMILES string (basic heuristic).

    Args:
        ligand: String to check

    Returns:
        True if likely a SMILES string
    """
    # Simple heuristic: SMILES contain organic chemistry characters
    # and don't have file extensions
    if "." in ligand and ligand.endswith((".sdf", ".mol2", ".mol", ".pdb")):
        return False

    # SMILES typically contain: C, N, O, S, P, F, Cl, Br, I, bonds, rings
    smiles_chars = set("CNOSPFIHcnospfih123456789()[]=#-+@/\\")
    return any(c in smiles_chars for c in ligand)


def validate_protein_input(protein: str) -> Tuple[str, str]:
    """
    Validate protein input and determine type.

    Args:
        protein: PDB ID or file path

    Returns:
        Tuple of (input_type, validated_input)
        input_type: "pdb_id" or "file"

    Raises:
        InputError: If input is invalid
    """
    # Check if it's a PDB ID
    if is_pdb_id(protein):
        return ("pdb_id", protein.upper())

    # Check if it's a file
    protein_path = Path(protein)
    if protein_path.exists():
        if protein_path.is_file():
            # Validate file extension
            valid_extensions = {".pdb", ".ent", ".cif"}
            if protein_path.suffix.lower() not in valid_extensions:
                raise FileFormatError(
                    f"Unsupported protein file format: {protein_path.suffix}. "
                    f"Supported formats: {', '.join(valid_extensions)}"
                )
            return ("file", str(protein_path.absolute()))
        else:
            raise InputError(f"Protein path is a directory, not a file: {protein}")
    else:
        raise InputError(
            f"Invalid protein input: '{protein}'. "
            "Must be a valid PDB ID (e.g., '1HSG') or path to a PDB file."
        )


def validate_ligand_input(ligand: str) -> Tuple[str, str]:
    """
    Validate ligand input and determine type.

    Args:
        ligand: SMILES string or file path

    Returns:
        Tuple of (input_type, validated_input)
        input_type: "smiles" or "file"

    Raises:
        InputError: If input is invalid
    """
    # Check if it's a file
    ligand_path = Path(ligand)
    if ligand_path.exists():
        if ligand_path.is_file():
            # Validate file extension
            valid_extensions = {".sdf", ".mol2", ".mol", ".pdb"}
            if ligand_path.suffix.lower() not in valid_extensions:
                raise FileFormatError(
                    f"Unsupported ligand file format: {ligand_path.suffix}. "
                    f"Supported formats: {', '.join(valid_extensions)}"
                )
            return ("file", str(ligand_path.absolute()))
        else:
            raise InputError(f"Ligand path is a directory, not a file: {ligand}")

    # Assume it's a SMILES string
    if is_smiles(ligand):
        return ("smiles", ligand)
    else:
        raise InputError(
            f"Invalid ligand input: '{ligand}'. "
            "Must be a valid SMILES string or path to an SDF/MOL2 file."
        )


def validate_binding_site(
    center: Optional[Tuple[float, float, float]], size: float
) -> None:
    """
    Validate binding site parameters.

    Args:
        center: Optional (x, y, z) coordinates
        size: Box size in Angstroms

    Raises:
        InputError: If parameters are invalid
    """
    if center is not None:
        if len(center) != 3:
            raise InputError(
                f"Binding site center must have 3 coordinates (X Y Z), got {len(center)}"
            )

        for coord in center:
            if not isinstance(coord, (int, float)):
                raise InputError(
                    f"Binding site coordinates must be numeric, got {type(coord)}"
                )

    if size <= 0:
        raise InputError(f"Binding site box size must be positive, got {size}")

    if size > 100:
        raise InputError(
            f"Binding site box size too large ({size} Å). "
            "Maximum recommended size is 100 Å."
        )


def validate_output_path(output: str) -> Path:
    """
    Validate output file path.

    Args:
        output: Output file path

    Returns:
        Validated Path object

    Raises:
        InputError: If path is invalid
    """
    output_path = Path(output)

    # Check if parent directory exists
    parent = output_path.parent
    if not parent.exists():
        raise InputError(f"Output directory does not exist: {parent}")

    # Check if file already exists (warn but don't fail)
    if output_path.exists():
        # Will be overwritten - CLI can handle confirmation
        pass

    # Validate extension
    if output_path.suffix.lower() not in {".csv", ""}:
        raise InputError(
            f"Output file must be CSV format (got {output_path.suffix}). "
            "Use .csv extension."
        )

    # Add .csv extension if missing
    if not output_path.suffix:
        output_path = output_path.with_suffix(".csv")

    return output_path
