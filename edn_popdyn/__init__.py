"""EDNpopdyn: analysis code for the manuscript (bioRxiv).

Importing the package makes the central path configuration available and
wires up the external lab packages (see `edn_popdyn.paths`).
"""

from . import paths  # noqa: F401  (side effect: sets up external package paths)

__all__ = ["paths"]
__version__ = "0.1.0"
