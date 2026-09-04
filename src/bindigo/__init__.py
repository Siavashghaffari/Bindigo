"""
Bindigo - Protein-Ligand Binding Affinity Prediction

A Python package for predicting protein-ligand binding affinities using
molecular docking (AutoDock Vina) combined with machine learning.

Bindigo 0.1.0 is a command-line tool; there is no public Python API yet.

Example usage:
    Basic prediction from command line:
        $ bindigo predict --protein 1HSG --ligand "CCO" --output results.csv
"""

from bindigo.__version__ import (
    __version__,
    __version_info__,
    __title__,
    __description__,
    __author__,
    __license__,
)

# Package-level exports. Only version metadata is public in 0.1.0; a Python
# API will be added once the prediction pipeline is implemented.
__all__ = [
    "__version__",
    "__version_info__",
    "__title__",
    "__description__",
    "__author__",
    "__license__",
]
