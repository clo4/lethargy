from copy import copy

from .errors import ArgsError, MissingOption
from .util import stab, identity, is_greedy, argv


class Opt:
    """Define an option to take it from a list of arguments."""

    def __init__(self, *names: str):
        self._names = {stab(name) for name in names}
        self._argc = 0  # Usually int, but can also be Ellipsis (greedy)
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

        # Shortest always goes first
        names = "|".join(sorted(self._names, reverse=True))

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
            raise ValueError(msg)

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
        argc = self._argc

        # Taking less than 1 argument will do nothing, use take_flag instead.
        if isinstance(argc, int) and argc < 1:
            msg = "{} takes {} arguments (did you mean to use `take_flag`?)"
            raise ArgsError(msg.format(self, argc))

        # Is this option in the list?
        index = self._find_in(args)

        # Return early if the option isn't present.
        if index is None:
            if raises:
                msg = f"{self} was not found in {args}"
                raise MissingOption(msg)

            if is_greedy(argc):
                return [] if d is None else d

            if d is None and argc != 1:
                return [None] * argc

            return d

        # Now we have the start index, find the index of the last value.
        if is_greedy(argc):
            end_idx = len(args)
        else:
            # Start index is the option name, add 1 to compensate
            end_idx = index + argc + 1

            # Don't continue if there are too few arguments
            if end_idx > len(args):
                # Highest index (length - 1) minus this option's index
                msg = "expected {n} argument{s} for '{self}', found {amount} ({args})"
                fmt = msg.format(
                    n=argc,
                    s="" if argc < 2 else "s",
                    self=str(self),
                    amount=len(args) - 1 - index,
                    args=", ".join(map(repr, args[index + 1 : end_idx])),
                )
                raise ArgsError(fmt)

        # The Opt itself is first, so offset by 1 for a list of the values.
        taken = args[index + 1 : end_idx]

        # Remove the option and its associated values from the list.
        if mut:
            del args[index:end_idx]

        # Returns a single value if there's only 1 value
        if argc == 1:
            return self._tfm(taken[0])

        # Return a list of transformed values.
        return [self._tfm(x) for x in taken]


# The following options are such a frequent usage of this library that it's
# reasonable to provide them automatically, and remove even more boilerplate.


take_debug = Opt("debug").take_flag
take_verbose = Opt("v", "verbose").take_flag
