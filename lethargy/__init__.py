from lethargy.errors import ArgsError, MissingOption, OptionError
from lethargy.option import Opt, take_debug, take_verbose
from lethargy.util import argv, eprint, print_if

__version__ = "1.3.0"
__all__ = (
    "ArgsError",
    "MissingOption",
    "Opt",
    "OptionError",
    "argv",
    "eprint",
    "print_if",
    "take_debug",
    "take_verbose",
)
