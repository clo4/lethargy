"""Module specifically to contain exception subclasses."""


class TransformError(Exception):
    """Tranforming an option raised an exception."""

    @classmethod
    def of(cls, exc):
        """Create a subclass of the original exception and TransformError."""
        # The exception needs to be a subclass of both the raised exception
        # and TransformError. This allows manually handling specific
        # exception types, _and_ automatically handling all exceptions that
        # get raised during transformation.
        exc_type = type(exc)
        name = f"{cls.__name__}[{exc_type.__name__}]"
        return type(name, (cls, exc_type), {})


class OptionError(Exception):
    """Superclass of ArgsError and MissingOption."""


class ArgsError(OptionError):
    """Too few arguments provided to an option."""


class MissingOption(OptionError):
    """Expecting an option, but unable to find it."""
