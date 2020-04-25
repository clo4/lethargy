"""Module specifically to contain exception subclasses."""


class TransformError(Exception):
    """Tranforming an option raised an exception."""


class OptionError(Exception):
    """Superclass of ArgsError and MissingOption."""


class ArgsError(OptionError):
    """Too few arguments provided to an option."""


class MissingOption(OptionError):
    """Expecting an option, but unable to find it."""
