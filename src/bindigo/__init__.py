"""
Bindigo - Protein-Ligand Binding Affinity Prediction

A Python package for predicting protein-ligand binding affinities using
molecular docking (AutoDock Vina) combined with machine learning.

Example usage:
    Basic prediction from command line:
        $ bindigo predict --protein 1HSG --ligand "CCO" --output results.csv

    Python API (v1.1+):
        from bindigo import BindingPredictor
        predictor = BindingPredictor()
        result = predictor.predict(protein="1HSG", ligand="CCO")
"""

from bindigo.__version__ import (
    __version__,
    __version_info__,
    __title__,
    __description__,
    __author__,
    __license__,
)

# Package-level exports (will be populated as modules are implemented)
__all__ = [
    "__version__",
    "__version_info__",
    "__title__",
    "__description__",
    "__author__",
    "__license__",
]

# Python API exports (v1.1+)
# from bindigo.core.predictor import BindingPredictor
# __all__.append("BindingPredictor")
