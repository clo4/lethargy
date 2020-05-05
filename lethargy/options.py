"""Defines the `take_opt` function and all the necessary 'option' protocol logic."""

from lethargy.errors import ArgsError
from lethargy.mixins import Named, Requirable, Transforming
from lethargy.util import argv, falsylist, identity, names_from


def take_flag(name, *, args=argv, mut=True):
    """Take a flag from a list of arguments."""
    option = Flag(names_from(name))
    return take(option, args, mut=mut)


def take_some(name, number, each=identity, *, args=argv, mut=True, required=False):
    """Take an option and its arguments from a list of arguments."""
    if number < 1:
        msg = f"The number of params ({number}) must be greater than 0."
        raise ValueError(msg)

    option = Explicit(names_from(name), number, each, required)
    return take(option, args, mut=mut)


def take_all(name, each=identity, *, args=argv, mut=True):
    """Take an option and all following arguments from a list of arguments."""
    option = Variadic(names_from(name), each)
    return take(option, args, mut=mut)


def take(option, args, *, mut=True):
    """Use an option object to take a range of arguments from a list."""
    try:
        start, end = option.span(args)
    except IndexError:
        return option.missing()

    taken = option.found(args[start:end])

    if mut:
        del args[start:end]

    return taken


class Explicit(Named, Requirable, Transforming):
    """An option that takes a defined number of arguments."""

    def __init__(self, names, number, transform, required):
        self.names = names
        self.number = number
        self._transform = transform
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
        start = self.index_in(args, exc=self.check_required())
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


class Variadic(Named, Transforming):
    """An option that takes all following arguments."""

    def __init__(self, names, transform):
        self.names = names
        self._transform = transform

    def __str__(self):
        names = self.prettynames()
        meta = self.metavar()
        return f"{names} [{meta}]..."

    def found(self, args):
        """Transform each argument found."""
        return [self.transform(arg) for arg in args[1:]]

    @staticmethod
    def missing():
        """Get an empty list."""
        return []

    def span(self, args):
        """Get the index of the option and no final value."""
        return self.index_in(args), None


class Flag(Named):
    """An option that takes no arguments."""

    def __init__(self, names):
        self.names = names

    def __str__(self):
        return self.prettynames()

    @staticmethod
    def found(_):
        """Literal `True`"""
        return True

    @staticmethod
    def missing():
        """Literal `False`"""
        return False

    def span(self, args):
        """Get the index of the flag name and next index."""
        index = self.index_in(args)
        return index, index + 1
