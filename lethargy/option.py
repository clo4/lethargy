"""Defines the `take_opt` function and all the necessary 'option' protocol logic."""

from lethargy.errors import ArgsError, MissingOption, TransformError
from lethargy.util import argv, falsylist, identity, into_list, tryname

# Functions   |
# ---------   v


def take(option, args, *, mut=True):
    """Use an option object to take a range of arguments from a list."""
    try:
        start, end = option.span(args)
    except IndexError:
        return option.missing()

    taken = args[start:end]

    if mut:
        del args[start:end]

    return option.found(taken)


def take_opt(name, number=None, into=None, *, args=argv, required=False, mut=True):
    """Take an option from the arguments."""
    names = frozenset(map(tryname, into_list(name)))
    tfm = into or identity

    if not number:
        option = Flag(names)

    elif number is ...:
        option = Variadic(names, tfm, required)

    elif number > 0:
        option = Explicit(names, number, tfm, required)

    else:
        msg = f"The number of params ({number}) must be greedy (...) or greater than 0"
        raise ValueError(msg)

    return take(option, args, mut=mut)


# Mixins   |
# ------   v


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


# Concrete option implementations   |
# -------------------------------   v


class Explicit(Named, Transforms, Requirable):
    """An option that takes a defined number of arguments."""

    def __init__(self, names, number, tfm, required):
        self.names = names
        self.number = number
        self.tfm = tfm
        self.required = required

    def __str__(self):
        meta = self.metavar()
        parts = [self.prettynames()] + [f"<{meta}>"] * self.number
        return " ".join(parts)

    def found(self, args):
        """Get either single or multiple transformed values based on `self.number`."""
        if self.number == 1:
            return self.transform(args[1])
        return [self.transform(arg) for arg in args[1:]]

    def missing(self):
        """Get either one `None` or an appropriately sized, falsy list of `None`s."""
        if self.number == 1:
            return None
        return falsylist([None] * self.number)

    def span(self, args):
        """Get the start and end indices of the option and its arguments."""
        start = self.index(args, exc=self.required_error())
        end = start + self.number + 1

        # There can't be fewer items than the number of expected values!
        if len(args) < end:
            some, s = self.number, "s" if self.number != 1 else ""
            number_found = len(args) - 1 - start
            n = number_found or "none"
            msg = f"Expected {some} argument{s} for option '{self}', but found {n}"
            if number_found:
                these = ", ".join(map(repr, args[start + 1 : end]))
                msg += f" ({these})"
            raise ArgsError(msg)

        return start, end


class Variadic(Named, Transforms, Requirable):
    """An option that takes all following arguments."""

    def __init__(self, names, tfm, required):
        self.names = names
        self.tfm = tfm
        self.required = required

    def __str__(self):
        names = self.prettynames()
        meta = self.metavar()
        return f"{names} [{meta}]..."

    def found(self, args):
        """Transform each argument found."""
        return [self.transform(arg) for arg in args[1:]]

    def missing(self):
        """Get an empty list."""
        return []

    def span(self, args):
        """Get the index of the option and no final value."""
        return self.index(args, exc=self.required_error()), None


class Flag(Named):
    """An option that takes no arguments."""

    def __init__(self, names):
        self.names = names

    def __str__(self):
        return self.prettynames()

    def found(self, _):
        """Literal `True`"""
        return True

    def missing(self):
        """Literal `False`"""
        return False

    def span(self, args):
        """Get the index of the flag name and next index."""
        index = self.index(args)
        return index, index + 1
