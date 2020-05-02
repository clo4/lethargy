"""Declarative, dynamic option parsing."""

# fmt: off
__version__ = "3.1.0"
__all__ = (
    # Options & arguments
    # -------------------
    "take_opt",
    "argv",

    # Error handling
    # --------------
    "show_errors",
    "expect",
    "fail",

    # Exceptions
    # ----------
    "ArgsError",
    "MissingOption",
    "TransformError",
    "OptionError",
)
# fmt: on

from lethargy.errors import ArgsError, MissingOption, OptionError, TransformError
from lethargy.options import take_opt
from lethargy.util import argv, expect, fail, show_errors
