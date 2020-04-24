"""Declarative, dynamic option parsing."""

# fmt: off
__version__ = "2.1.0"
__all__ = (
    # Simplified interface
    # --------------------
    "take_opt",
    "argv",
    "expect",
    "show_errors",

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
    "TransformError",
    "OptionError",

    # Legacy
    # ------
    "take_debug",
    "take_verbose",
)
# fmt: on

from lethargy.errors import ArgsError, MissingOption, OptionError, TransformError
from lethargy.option import Opt, take_opt
from lethargy.util import argv, eprint, expect, fail, print_if, show_errors

# The following options will be removed in version 3.0 because take_opt makes
# them redundant. It's clearer and nearly as fast to use `take_opt('debug')`.

take_debug = Opt("debug").take_flag
take_verbose = Opt("v", "verbose").take_flag
