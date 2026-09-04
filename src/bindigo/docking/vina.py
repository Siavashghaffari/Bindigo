"""
AutoDock Vina discovery and availability checks.

Vina is a native binary and cannot be installed by pip, so most users will
reach Bindigo without it. These helpers locate the executable and turn a
missing one into an actionable error rather than a stack trace.
"""

import os
import shutil
from typing import Optional

from bindigo.utils.exceptions import DependencyError

# Environment variable used to point Bindigo at a Vina binary that is not
# on PATH.
VINA_PATH_ENV_VAR = "BINDIGO_VINA_PATH"

# Names the Vina executable ships under, in the order they are tried.
VINA_EXECUTABLE_NAMES = ("vina", "vina.exe", "vina_split")

VINA_INSTALL_HELP = """AutoDock Vina is a native binary and cannot be installed with pip.
Install it with one of the following, then re-run the command:

  conda    conda install -c conda-forge vina
  macOS    brew install autodock-vina
  Linux    download a release binary and put it on your PATH
  Windows  download the .exe and add its folder to your PATH

  Releases: https://github.com/ccsb-scripps/AutoDock-Vina/releases

If Vina is already installed but not on your PATH, point Bindigo at it:

  {env_var}=/full/path/to/vina bindigo predict ...

Check your installation with:  vina --version""".format(
    env_var=VINA_PATH_ENV_VAR
)


def find_vina_executable() -> Optional[str]:
    """
    Locate the AutoDock Vina executable.

    Looks at the ``BINDIGO_VINA_PATH`` environment variable first, then falls
    back to searching PATH.

    Returns:
        Absolute path to the Vina executable, or None if it cannot be found.
    """
    # Explicit override wins, so a user with a non-standard install can always
    # get unstuck without touching PATH.
    override = os.environ.get(VINA_PATH_ENV_VAR)
    if override:
        resolved = shutil.which(override)
        if resolved:
            return resolved
        if os.path.isfile(override) and os.access(override, os.X_OK):
            return os.path.abspath(override)
        return None

    for name in VINA_EXECUTABLE_NAMES:
        resolved = shutil.which(name)
        if resolved:
            return resolved

    return None


def is_vina_available() -> bool:
    """
    Check whether AutoDock Vina can be found.

    Returns:
        True if the Vina executable is available.
    """
    return find_vina_executable() is not None


def check_vina_available() -> str:
    """
    Ensure AutoDock Vina is installed and return its path.

    Returns:
        Absolute path to the Vina executable.

    Raises:
        DependencyError: If Vina cannot be found, with installation
            instructions attached.
    """
    vina_path = find_vina_executable()
    if vina_path:
        return vina_path

    override = os.environ.get(VINA_PATH_ENV_VAR)
    if override:
        message = (
            f"AutoDock Vina was not found at the path given by "
            f"{VINA_PATH_ENV_VAR}: '{override}'. Docking cannot run without it."
        )
    else:
        message = (
            "AutoDock Vina was not found on your PATH. Bindigo needs it to "
            "dock the ligand, so the prediction cannot run without it."
        )

    raise DependencyError(message, details=VINA_INSTALL_HELP)
