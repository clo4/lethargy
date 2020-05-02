"""Defines the `take_opt` function and all the necessary 'option' protocol logic."""

from warnings import warn

from lethargy.errors import ArgsError
from lethargy.mixins import Named, Requirable, Transforming
from lethargy.util import argv, falsylist, identity, into_list, tryname


def take_opt(name, number=None, call=None, *, args=argv, required=False, mut=True):
    """Take an option from the arguments."""
    transformer = call or identity

    # NOTE: Using 'name or ""' is a hacky solution. Better solution one day ~
    names = frozenset(map(tryname, into_list(name or "")))

    if not number:
        option = Flag(names)

        # Let the user know they're calling the function wrong, but don't be a
        # nuisance and raise an error - they won't cause anything to break.
        if call:
            warn(f"Bad argument ({call}): flags take no values to transform.")
        if required:
            warn(f"Bad argument (required={required}): flags cannot be required.")

    elif number is ...:
        option = Variadic(names, transformer)

        # Variadic options are inherently optional. Requiring an option to be
        # present but not giving it anything ultimately results in the same
        # value as you'd get omitting it entirely, but because it's required
        # you end up getting a lot more annoyed. Very bad user experience.
        if required:
            warn(f"Bad argument (required={required}): variadic options are optional.")

    elif number > 0:
        option = Explicit(names, number, transformer, required)

    else:
        msg = f"The number of params ({number}) must be None, greedy (...), or over 0."
        raise ValueError(msg)

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

    def missing(self):
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

    def found(self, _):
        """Literal `True`"""
        return True

    def missing(self):
        """Literal `False`"""
        return False

    def span(self, args):
        """Get the index of the flag name and next index."""
        index = self.index_in(args)
        return index, index + 1
