"""Declarative, dynamic option parsing."""

# fmt: off
__version__ = "2.0.1"
__all__ = (
    # Simplified interface
    # --------------------
    "args",
    "flag",

    # Original interface
    # ------------------
    "Opt",
    "argv",

    # Utility
    # -------
    "eprint",
    "print_if",

    # Technical stuff
    # ---------------
    "ArgsError",
    "MissingOption",
    "OptionError",

    # Legacy
    # ------
    "take_debug",
    "take_verbose",
)
# fmt: on

from lethargy.errors import ArgsError, MissingOption, OptionError
from lethargy.option import Opt, args, flag
from lethargy.util import argv, eprint, print_if

# The following options are such a frequent usage of this library that it's
# reasonable to provide them automatically, and remove even more boilerplate.

take_debug = Opt("debug").take_flag
take_verbose = Opt("v", "verbose").take_flag
