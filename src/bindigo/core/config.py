"""
Configuration settings for Bindigo.

Defines default parameters for docking, ML models, and other operations.
"""

from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration container for Bindigo."""

    # Package directories
    PACKAGE_DIR = Path(__file__).parent.parent
    MODELS_DIR = PACKAGE_DIR / "models"
    DATA_DIR = PACKAGE_DIR / "data"

    # Docking parameters (AutoDock Vina)
    DOCKING_EXHAUSTIVENESS = 8
    DOCKING_NUM_MODES = 9
    DOCKING_ENERGY_RANGE = 3  # kcal/mol

    # Binding site detection
    BINDING_SITE_AUTO_DETECT = True
    BINDING_SITE_DEFAULT_SIZE = 20.0  # Angstroms

    # ML model settings
    DEFAULT_MODEL_NAME = "default"
    MODEL_FILE = "default_model.pkl"
    SCALER_FILE = "scaler.pkl"

    # Confidence thresholds (for applicability domain)
    CONFIDENCE_HIGH_THRESHOLD = 0.8
    CONFIDENCE_MEDIUM_THRESHOLD = 0.5

    # Protein preprocessing
    REMOVE_WATER = True
    ADD_HYDROGENS = True
    SELECT_CHAIN = "A"  # Default chain if multi-chain

    # Ligand preprocessing
    LIGAND_ADD_HYDROGENS = True
    LIGAND_GENERATE_3D = True
    LIGAND_CHARGE_METHOD = "gasteiger"

    # Output settings
    SAVE_POSES = True
    OUTPUT_FORMAT = "csv"
    VERBOSE = False

    # Database settings
    PDB_BASE_URL = "https://files.rcsb.org/download/"
    PDB_CACHE_DIR = Path.home() / ".bindigo" / "cache" / "pdb"

    # Performance settings
    MAX_MEMORY_GB = 2.0
    TIMEOUT_SECONDS = 300  # 5 minutes per prediction

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Dictionary of configuration values
        """
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }

    @classmethod
    def update(cls, **kwargs):
        """
        Update configuration values.

        Args:
            **kwargs: Configuration key-value pairs to update
        """
        for key, value in kwargs.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")


# Create default config instance
config = Config()
