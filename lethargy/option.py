"""Defines the Opt class (main interface)."""

from copy import copy

from lethargy.errors import ArgsError, MissingOption, TransformError
from lethargy.util import argv, falsylist, identity, is_greedy, stab


class Opt:
    """Define an option to take it from a list of arguments."""

    def __init__(self, name, number=0, tfm=None):
        names = [name] if isinstance(name, str) else name
        self.names = {stab(name) for name in names}
        self.argc = number  # Usually int, but can also be Ellipsis (greedy)
        self.tfm = tfm if callable(tfm) else identity

    def __copy__(self):
        return self.__class__(copy(self.names), self.argc, self.tfm)

    def __str__(self):
        if not self.names:
            return ""

        names = "|".join(sorted(sorted(self.names), key=len))

        if not isinstance(self.tfm, type):
            metavar = "value"
        else:
            metavar = self.tfm.__name__.lower()

        if is_greedy(self.argc):
            hint = f"[{metavar}]..."
        elif self.argc > 0:
            hint = " ".join([f"<{metavar}>"] * self.argc)
        else:
            return names

        return f"{names} {hint}"

    def __repr__(self):
        repr_str = ""

        # Opt(<names>)
        qname = self.__class__.__qualname__
        mapped = [repr(name) for name in self.names]
        names = ", ".join(mapped)
        repr_str += f"{qname}({names})"

        # [.takes(<n>[, <tfm>])]
        # This whole thing is optional, if there's nothing to show it won't
        # be in the repr string.
        if self.argc:
            takes = [self.argc]
            if self.tfm is not identity:
                if isinstance(self.tfm, type):
                    takes.append(self.tfm.__name__)
                else:
                    takes.append(repr(self.tfm))
            repr_str += ".takes({})".format(", ".join(map(str, takes)))

        # at <ID>
        repr_str += f" at {hex(id(self))}"

        return f"<{repr_str}>"

    def __eq__(self, other):
        try:
            return (
                self.names == other.names
                and self.argc == other.argc
                and self.tfm is other.tfm
            )
        except AttributeError:
            return NotImplemented

    @property
    def argc(self):
        """Get the number of arguments this option takes."""
        return self._argc

    @argc.setter
    def argc(self, value):
        if not is_greedy(value) and value < 0:
            msg = f"The number of arguments ({value}) must be >1 or greedy (``...``)"
            raise ValueError(msg)
        self._argc = value

    def find_in(self, args):
        """Search args for this option and return an index if it's found."""
        for name in self.names:
            try:
                return args.index(name)
            except ValueError:
                continue
        return None

    def take_flag(self, args=argv, *, mut=True):
        """Get a bool indicating whether the option was present in the arguments."""
        idx = self.find_in(args)

        if idx is None:
            return False

        if mut:
            del args[idx]

        return True

    def take_args(self, args=argv, *, required=False, mut=True):
        """Get the values of this option."""
        argc = self.argc

        if not argc:
            msg = f"'{self}' takes no arguments (did you mean to use `take_flag`?)"
            raise RuntimeError(msg)

        # Is this option in the list?
        index = self.find_in(args)

        # Return early if the option isn't present.
        if index is None:
            if required:
                msg = f"Missing required option '{self}'"
                raise MissingOption(msg)

            if is_greedy(argc):
                return falsylist()

            if argc != 1:
                return falsylist([None] * argc)

            return None

        # Start index is now set, find the index of the *final* value.
        if is_greedy(argc):
            end_idx = len(args)
        else:
            # Start index is the option name, add 1 to compensate.
            end_idx = index + argc + 1

            # Fail fast if the option expects more arguments than it has.
            if end_idx > len(args):
                # Highest index (length - 1) minus this option's index.
                actual = len(args) - 1 - index
                n = actual or "none"
                s = "s" if argc != 1 else ""
                msg = f"Expected {argc} argument{s} for option '{self}', but found {n}"
                if actual:
                    present_args = ", ".join(map(repr, args[index + 1 : end_idx]))
                    msg += f" ({present_args})"
                raise ArgsError(msg)

        # Get the list of values starting from the first value to the option.
        taken = args[index + 1 : end_idx]

        # Remove the option and its associated values from the list.
        if mut:
            del args[index:end_idx]

        # Single return value keeps the unpacking usage pattern consistent.
        if argc == 1:
            return self.transform(taken[0])

        # Return a list of transformed values.
        return [self.transform(x) for x in taken]

    def transform(self, value):
        """Call _tfm on a string and return the result, or raise an exception union."""
        try:
            return self.tfm(value)

        except Exception as exc:
            message = f"Option '{self}' received an invalid value: {value!r}"

            # The exception needs to be a subclass of both the raised exception
            # and TransformError. This allows manually handling specific
            # exception types, _and_ automatically handling all exceptions that
            # get raised during transformation.
            name = f"TransformError[{exc.__class__.__name__}]"
            bases = (TransformError, exc.__class__)
            new_exc = type(name, bases, {})

            raise new_exc(message) from exc


def take_opt(name, number=None, call=None, *, args=argv, required=False, mut=True):
    """Quickly take an option as flag, or with some arguments."""
    opt = Opt(name, number, call)
    if not number:
        return opt.take_flag(args, mut=mut)
    return opt.take_args(args, required=required, mut=mut)
