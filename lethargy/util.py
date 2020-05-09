"""Functions and values, independent of other modules."""
import sys
from contextlib import contextmanager
from lethargy.errors import OptionError, TransformError

# Lethargy provides its own argv so you don't have to import sys or worry
# about mutating the original.
argv = sys.argv.copy()

falsylist = type("falsylist", (list,), {"__bool__": lambda _: False})

identity = lambda a: a  # noqa


def names_from(name):
    """Create a frozenset of potentially POSIX-like names from a string or sequence."""
    if not name:
        raise ValueError("Options must have at least one name.")

    names = name if not isinstance(name, str) else [name]

    return {try_name(nm) for nm in names}


def try_name(text):
    """Try to make a loosely POSIX-style name."""
    stripped = str(text).strip()

    if not stripped:
        raise ValueError("Cannot make an option name from an empty string.")

    # Assume it's been pre-formatted if it starts with something that's not
    # a letter or number.
    if not stripped[0].isalnum():
        return stripped

    name = "-".join(stripped.split())

    return f"-{name}" if len(name) == 1 else f"--{name}"


def fail(message=None):
    """Print a message to stderr and exit with code 1."""
    if message:
        print(message, file=sys.stderr)
    sys.exit(1)


@contextmanager
def expecting(*errors, reason=None):
    """Call `fail()` if any given errors are raised."""
    try:
        yield
    except errors as e:
        fail(reason or e)


def show_errors():
    """Expect errors from options and values, fail with a useful message."""
    return expect(OptionError, TransformError)
