"""Defines mixin classes used by option implementations."""

from lethargy.errors import MissingOption, TransformError


class Named:
    """[mixin] Add helper methods for options with a `names` attribute."""

    names: frozenset

    def prettynames(self):
        """Get a sorted CLI-like representation of the option's names."""
        return "|".join(sorted(sorted(self.names), key=len))

    def index(self, args, exc=None):
        """Get the index of the first occurrence of a name in the arguments."""
        for index, item in enumerate(args):
            if item in self.names:
                return index
        raise exc or IndexError


class Requirable:
    """[mixin] Add helper methods for options with a `required` attribute."""

    required: bool

    def required_error(self):
        """Get an appropriate MissingOption exception if `self.required`, or None."""
        if not self.required:
            return None
        return MissingOption(f"Missing required option '{self}'")


class Transforms:
    """[mixin] Add helper methods for options with a `tfm` attribute."""

    tfm: callable

    def metavar(self):
        """Get the name of the `self.tfm` callable."""
        if isinstance(self.tfm, type):
            return self.tfm.__name__.lower()

        return "value"

    def transform(self, value):
        """Transform a value using `self.tfm`, raise a TransformError[E] on failure."""
        try:
            return self.tfm(value)
        except Exception as exc:
            message = f"Option '{self}' received an invalid value: {value!r}"
            new = TransformError.of(exc)
            raise new(message) from exc
