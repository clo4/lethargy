from lethargy.util import (
    tryposixname,
    argv,
    falsylist,
    identity,
    into_list,
    index_of_first_found,
)
from lethargy.errors import ArgsError, MissingOption, TransformError


def take_opt(name, number=None, into=None, *, args=argv, required=False, mut=True):
    names = frozenset(map(tryposixname, into_list(name)))
    tfm = into or identity

    if not number:
        option = FlagOption(names)

    elif number is ...:
        option = VariadicOption(names, tfm, required)

    elif number > 0:
        option = FiniteOption(names, number, tfm, required)

    else:
        msg = f"The number of params ({number}) must be greedy (...) or greater than 0."
        raise ValueError(msg)

    return take(option, args, mut=mut)


def take(option, args, *, mut=True):
    try:
        start, end = option.indices()
    except IndexError:
        return option.not_found()

    taken = args[start:end]

    if mut:
        del args[start:end]

    return option.found(taken)


class NamedMixin:
    names: frozenset

    def pretty_names(self):
        return "|".join(sorted(sorted(self.names), key=len))


class TransformMixin:
    tfm: callable

    def metavar(self):
        if isinstance(self.tfm, type):
            return self.tfm.__name__.lower()
        return "value"

    def transform(self, value):
        try:
            return self.tfm(value)
        except Exception as exc:
            message = f"Option '{self}' received an invalid value: {value!r}"
            new = TransformError.of(exc)
            raise new(message) from exc


class FlagOption(NamedMixin):
    def __init__(self, names):
        self.names = names

    def __str__(self):
        return self.pretty_names()

    def found(self, _):
        return True

    def not_found(self):
        return False

    def indices(self, args):
        for index, arg in enumerate(args):
            if arg in self.names:
                return index, index + 1
        raise IndexError


class VariadicOption(TransformMixin, NamedMixin):
    def __init__(self, names, tfm, required):
        self.names = names
        self.tfm = tfm
        self.required = required

    def __str__(self):
        names = self.pretty_names()
        meta = self.metavar()
        return f"{names} [{meta}]..."

    def indices(self, args):
        try:
            return index_of_first_found(self.names, args), len(args)
        except IndexError:
            if not self.required:
                raise
            raise MissingOption(f"Missing required option '{self}'")

    def not_found(self):
        return []

    def found(self, args):
        return [self.transform(arg) for arg in args[1:]]


class FiniteOption(TransformMixin, NamedMixin):
    def __init__(self, names, number, tfm, required):
        self.names = names
        self.number = number
        self.tfm = tfm
        self.required = required

    def __str__(self):
        meta = self.metavar()
        parts = [self.pretty_names()]
        parts += [f"<{meta}>"] * self.number
        return " ".join(parts)

    def indices(self, args):
        try:
            start = index_of_first_found(self.names, args)
        except IndexError:
            if not self.required:
                raise
            raise MissingOption(f"Missing required option '{self}'")

        end = start + self.number + 1

        # There can't be fewer items than the number of expected values!
        if end > len(args):
            some = self.number
            number_found = len(args) - 1 - start
            n = number_found or "none"
            s = "s" if some != 1 else ""
            msg = f"Expected {some} argument{s} for option '{self}', but found {n}"
            if number_found:
                given = ", ".join(map(repr, args[start + 1 : end]))
                msg += f" ({given})"
            raise ArgsError(msg)

        return start, end

    def found(self, args):
        if self.number == 1:
            return self.transform(args[1])
        return [self.transform(arg) for arg in args[1:]]

    def not_found(self):
        if self.number == 1:
            return None
        return falsylist([None] * self.number)
