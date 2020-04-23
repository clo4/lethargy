"""Declarative, dynamic option parsing."""

# fmt: off
__version__ = "2.0.1"
__all__ = (
    # Simplified interface
    # --------------------
    "take_opt",
    "argv",
    "show_errors",
    "fail_on",

    # Original interface
    # ------------------
    "Opt",

    # Utility
    # -------
    "eprint",
    "fail",
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
from lethargy.option import Opt, take_opt
from lethargy.util import argv, eprint, fail, fail_on, print_if, show_errors

# The following options are such a frequent usage of this library that it's
# reasonable to provide them automatically, and remove even more boilerplate.

take_debug = Opt("debug").take_flag
take_verbose = Opt("v", "verbose").take_flag
