# pylint: disable=invalid-name

import functools
import sys
from copy import copy

# Lethargy provides its own argv so you don't have to import sys or worry
# about mutating the original.
argv = sys.argv.copy()


class OptionError(Exception):
    """Superclass of ArgsError and MissingOption"""


class ArgsError(OptionError):
    """Too few arguments provided to an option"""


class MissingOption(OptionError):
    """Expecting an option, but unable to find it"""


def stab(text):
    """Stab a string, with a skewer of appropriate length.

        >>> stab('x')
        '-x'
        >>> stab('xyz')
        '--xyz'
        >>> stab('abc xyz')
        '--abc-xyz'
        >>> stab('  lm no p ')
        '--lm-no-p'
    """
    stripped = str(text).strip()
    name = "-".join(stripped.split())

    chars = len(name)

    if chars > 1:
        return f"--{name}"
    if chars == 1:
        return f"-{name}"

    raise ValueError("Cannot stab empty string")


def is_greedy(value):
    """Return a boolean representing whether a given value is "greedy"."""
    return value is ...


def identity(a):
    """Get the same output as the input."""
    return a


class Opt:
    """Define an option to take it from a list of arguments."""

    def __init__(self, *names: str):
        self._names = {stab(name) for name in names}
        self._argc = 0
        self._tfm = identity

    def __copy__(self):
        new = self.__class__()
        new._names = copy(self._names)
        new._argc = self._argc
        new._tfm = self._tfm
        return new

    def __str__(self):
        if not self._names:
            return ""

        names = "|".join(self._names)

        if not isinstance(self._tfm, type):
            metavar = "value"
        else:
            metavar = self._tfm.__name__.lower()

        if is_greedy(self._argc):
            vals = f"[{metavar}]..."
        elif self._argc > 0:
            vals = " ".join([f"<{metavar}>"] * self._argc)
        else:
            return names

        return f"{names} {vals}"

    def __repr__(self):
        repr_str = ""

        # Opt(<names>)
        qname = self.__class__.__qualname__
        mapped = [repr(name) for name in self._names]
        names = ", ".join(mapped)
        repr_str += f"{qname}({names})"

        # [.takes(<n>[, <converter>])]
        # This whole thing is optional, if there's nothing to show it won't
        # be in the repr string.
        # Should try to be smart about representing the converter.
        if self._argc != 0 or self._tfm is not identity:
            takes = [self._argc]
            if self._tfm is not identity:
                if isinstance(self._tfm, type):
                    takes.append(self._tfm.__name__)
                else:
                    takes.append(repr(self._tfm))
            repr_str += ".takes({})".format(", ".join(map(str, takes)))

        # at <ID>
        repr_str += f" at {hex(id(self))}"

        return f"<{repr_str}>"

    def __eq__(self, other):
        try:
            return (
                self._names == other._names
                and self._argc == other._argc
                and self._tfm == other._tfm
            )
        except AttributeError:
            return NotImplemented

    def _find_in(self, args):
        """Search args for this option and return an index if it's found."""
        for name in self._names:
            try:
                return args.index(name)
            except ValueError:
                continue
        return None

    def takes(self, n, tfm=None):
        """Set the number of arguments the instance takes."""
        if not is_greedy(n) and n < 0:
            msg = f"The number of arguments ({n}) must be positive or greedy ('...')"
            raise ArgsError(msg)

        self._argc = n
        if tfm is not None:
            self._tfm = tfm
        return self

    def take_flag(self, args=argv, *, mut=True):
        """Get a bool indicating whether the option was present in the arguments."""
        idx = self._find_in(args)
        if idx is None:
            return False
        if mut:
            del args[idx]
        return True

    def take_args(self, args=argv, *, d=None, raises=False, mut=True):
        """Get the values of this option."""
        amt = self._argc

        # Taking less than 1 argument will do nothing, better to use take_flag
        if isinstance(amt, int) and amt < 1:
            msg = "{} takes {} arguments (did you mean to use `take_flag`?)"
            raise ArgsError(msg.format(self, amt))

        # Is this option in the list?
        index = self._find_in(args)

        # Option not found in args, skip the remaining logic and return the
        # default value. No list mutation will occur
        if index is None:
            if raises:
                msg = f"{self} was not found in {args}"
                raise MissingOption(msg)

            # None is special (return the _actual_ default)

            if is_greedy(amt):
                return [] if d is None else d

            if d is None and amt != 1:
                return [None] * amt

            return d

        # The `take` call needs a start index, offset, and list
        if is_greedy(amt):
            # Number of indices after the starting index
            end_idx = len(args)
        else:
            # Start index is the option name, add 1 to compensate
            end_idx = index + amt + 1

            # Don't continue if there are too few arguments
            if end_idx > len(args):
                # Highest index (length - 1) minus this option's index
                n_found = len(args) - 1 - index
                plural = "" if amt == 1 else "s"
                found = ", ".join(map(repr, args[index + 1 : end_idx]))
                msg = "expected {n} argument{s} for '{self}', found {amt} ({what})"
                fmt = msg.format(n=amt, s=plural, self=self, amt=n_found, what=found)
                raise ArgsError(fmt)

        taken = args[index + 1 : end_idx]

        if mut:
            del args[index:end_idx]

        if amt == 1:
            # Single value if amt is 1
            return self._tfm(taken[0])

        # Short circuits if greedy to prevent ``... > 1``
        if is_greedy(amt) or amt > 1:
            # List of values (`taken` will always be iterable)
            return [self._tfm(x) for x in taken]

        # amt is (somehow) invalid -- manually set to a negative value?
        msg = "{!r} was found, but {!r} arguments could not be retreived."
        raise ArgsError(msg.format(self, amt))


# The following functions are such a frequent usage of this library that it's
# reasonable to provide them automatically, and remove even more boilerplate.

eprint = functools.partial(print, file=sys.stderr)

take_debug = Opt("debug").take_flag
take_verbose = Opt("v", "verbose").take_flag


def print_if(condition):
    """Return either ``print`` or a dummy function, depending on ``condition``."""
    return print if condition else lambda *_, **__: None
