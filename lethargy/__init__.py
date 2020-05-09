"""Highly maintainable option parsing for imperative, small-to-medium-sized scripts."""

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
    "expecting",
    "fail",
    # Exceptions
    # ----------
    "ArgsError",
    "MissingOption",
    "TransformError",
    "OptionError",
)

from lethargy.errors import ArgsError, MissingOption, OptionError, TransformError
from lethargy.options import take_flag, take_args, take_all
from lethargy.util import argv, expecting, fail, show_errors
