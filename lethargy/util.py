"""Functions and values, independent of other modules."""

import sys
from contextlib import contextmanager
from collections.abc import Collection

from lethargy.errors import OptionError, TransformError

# Lethargy provides its own argv so you don't have to import sys or worry
# about mutating the original.
argv = sys.argv.copy()


def into_list(o):
    return [o] if isinstance(o, str) or not isinstance(o, Collection) else o


def index_of_first_found(needles, haystack):
    for index, item in enumerate(haystack):
        if item in needles:
            return index
    raise IndexError


def tryposixname(text):
    """Get a POSIX-style name, or strip if the first character isn't alphanumeric."""
    stripped = str(text).strip()

    # Assume it's been pre-formatted if it starts with something that's not
    # a letter or number.
    if not stripped[:1].isalnum():
        return stripped

    name = "-".join(stripped.split())

    chars = len(name)

    if chars > 1:
        return f"--{name}"
    if chars == 1:
        return f"-{name}"

    raise ValueError("Cannot make an option name from an empty string.")


def is_greedy(value):
    """Return a boolean representing whether a given value is "greedy"."""
    return value is ...


def identity(a):
    """Get the same output as the input."""
    return a


def fail(message=None):
    """Print a message to stderr and exit with code 1."""
    if message:
        print(message, file=sys.stderr)
    sys.exit(1)


@contextmanager
def expect(*errors, reason=None):
    """Call `fail()` if any given errors are raised."""
    try:
        yield
    except errors as e:
        fail(reason or e)


def show_errors():
    """Expect errors from options and values, fail with a useful message."""
    return expect(OptionError, TransformError)


falsylist = type("falsylist", (list,), {"__bool__": lambda _: False})
