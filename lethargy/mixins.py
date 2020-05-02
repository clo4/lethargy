"""Defines mixin classes used by option implementations."""

from collections.abc import Callable, Collection

from lethargy.errors import MissingOption, TransformError


class Named:
    """[mixin] Add helper methods for options with a `names` attribute."""

    names: Collection

    def prettynames(self):
        """Get a sorted CLI-like representation of the option's names."""
        return "|".join(sorted(sorted(self.names), key=len))

    def index_in(self, args, exc=None):
        """Get the index of the first occurrence of a name in the arguments."""
        for index, item in enumerate(args):
            if item in self.names:
                return index
        raise exc or IndexError


class Transforming:
    """[mixin] Add helper methods for options with a `_transform` attribute."""

    _transform: Callable
    default_metavar = "value"

    def metavar(self):
        """Get the name of the `self._transform` callable."""
        if isinstance(self._transform, type):
            return self._transform.__name__.lower()

        return self.default_metavar

    def transform(self, value):
        """Transform a value using `self._transform`, fail with TransformError[E]."""
        try:
            return self._transform(value)
        except Exception as exc:
            message = f"Option '{self}' received an invalid value: {value!r}"
            new = TransformError.of(exc)
            raise new(message) from exc


class Requirable:
    """[mixin] Add helper methods for options with a `required` attribute."""

    required: bool

    def check_required(self):
        """Get an appropriate MissingOption exception if `self.required`, or None."""
        if not self.required:
            return None
        return MissingOption(f"Missing required option '{self}'")
