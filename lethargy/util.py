"""Functions and values, independent of other modules."""

import functools
import sys

# Lethargy provides its own argv so you don't have to import sys or worry
# about mutating the original.
argv = sys.argv.copy()


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

    Unless, of course, it has already been stabbed. That would just be cruel.

        >>> stab('-x')
        '-x'

    Or if it has a shield. These are only skewers after all.

        >>> stab('/FLAG')
        '/FLAG'
    """
    stripped = str(text).strip()

    # Assume it's been pre-formatted if it starts with a slash or a dash
    if stripped.startswith("-") or stripped.startswith("/"):
        return stripped

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


def print_if(condition):
    """Return either ``print`` or a dummy function, depending on ``condition``."""
    return print if condition else lambda *__, **_: None


eprint = functools.partial(print, file=sys.stderr)
