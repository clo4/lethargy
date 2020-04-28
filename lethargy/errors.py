"""Module specifically to contain exception subclasses."""


class TransformError(Exception):
    """Tranforming an option raised an exception."""

    @classmethod
    def of(cls, other):
        # The exception needs to be a subclass of both the raised exception
        # and TransformError. This allows manually handling specific
        # exception types, _and_ automatically handling all exceptions that
        # get raised during transformation.
        name = f"{cls.__name__}[{type(other).__name__}]"
        return type(name, (cls, type(other)), {})


class OptionError(Exception):
    """Superclass of ArgsError and MissingOption."""


class ArgsError(OptionError):
    """Too few arguments provided to an option."""


class MissingOption(OptionError):
    """Expecting an option, but unable to find it."""
