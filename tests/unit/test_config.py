"""
Test configuration settings.
"""

from pathlib import Path
from bindigo.core.config import Config, config


def test_config_has_required_attributes():
    """Test that config has all required attributes."""
    required_attrs = [
        "PACKAGE_DIR",
        "MODELS_DIR",
        "DATA_DIR",
        "DOCKING_EXHAUSTIVENESS",
        "BINDING_SITE_DEFAULT_SIZE",
        "DEFAULT_MODEL_NAME",
    ]
    for attr in required_attrs:
        assert hasattr(Config, attr)


def test_package_dir_exists():
    """Test that package directory exists."""
    assert Config.PACKAGE_DIR.exists()
    assert Config.PACKAGE_DIR.is_dir()


def test_models_dir_path():
    """Test models directory path."""
    assert Config.MODELS_DIR == Config.PACKAGE_DIR / "models"


def test_data_dir_path():
    """Test data directory path."""
    assert Config.DATA_DIR == Config.PACKAGE_DIR / "data"


def test_docking_parameters():
    """Test docking parameters have valid values."""
    assert Config.DOCKING_EXHAUSTIVENESS > 0
    assert Config.DOCKING_NUM_MODES > 0
    assert Config.DOCKING_ENERGY_RANGE > 0


def test_binding_site_defaults():
    """Test binding site default values."""
    assert Config.BINDING_SITE_AUTO_DETECT is True
    assert Config.BINDING_SITE_DEFAULT_SIZE > 0


def test_confidence_thresholds():
    """Test confidence threshold values."""
    assert 0 < Config.CONFIDENCE_HIGH_THRESHOLD <= 1
    assert 0 < Config.CONFIDENCE_MEDIUM_THRESHOLD <= 1
    assert Config.CONFIDENCE_HIGH_THRESHOLD > Config.CONFIDENCE_MEDIUM_THRESHOLD


def test_config_to_dict():
    """Test config conversion to dictionary."""
    config_dict = Config.to_dict()
    assert isinstance(config_dict, dict)
    assert "DOCKING_EXHAUSTIVENESS" in config_dict
    assert "DEFAULT_MODEL_NAME" in config_dict


def test_config_instance_exists():
    """Test that default config instance exists."""
    assert config is not None
    assert isinstance(config, Config)
