"""Functions and values, independent of other modules."""

import sys
from contextlib import contextmanager
from collections.abc import Collection

from lethargy.errors import OptionError, TransformError

# Lethargy provides its own argv so you don't have to import sys or worry
# about mutating the original.
argv = sys.argv.copy()

falsylist = type("falsylist", (list,), {"__bool__": lambda _: False})


def into_list(o):
    """Put `o` in a list, if it's not a collection."""
    return [o] if isinstance(o, str) or not isinstance(o, Collection) else o


def tryname(text):
    """Try to make a loosely POSIX-style name."""
    stripped = str(text).strip()

    if not stripped:
        raise ValueError("Cannot make an option name from an empty string.")

    # Assume it's been pre-formatted if it starts with something that's not
    # a letter or number.
    if not stripped[:1].isalnum():
        return stripped

    name = "-".join(stripped.split())

    return f"-{name}" if len(name) == 1 else f"--{name}"


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
