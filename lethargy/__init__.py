"""Declarative, dynamic option parsing."""

# fmt: off
__version__ = "4.0.0-dev"
__all__ = (
    # Options & arguments
    # -------------------
    "take_flag",
    "take_args",
    "take_all",
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
from lethargy.options import take_flag, take_args, take_all
from lethargy.util import argv, expect, fail, show_errors
