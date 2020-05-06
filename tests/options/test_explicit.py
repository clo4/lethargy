# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy.options import Explicit as Ex
from lethargy.util import identity
from lethargy.errors import MissingOption, ArgsError

parametrize = pytest.mark.parametrize


def test_init():
    a, b, c, d = object(), object(), object(), object()
    e = Ex(a, b, c, d)
    assert e.names is a
    assert e.number is b
    assert e._transform is c
    assert e.required is d


@parametrize("required", (True, False))
def test_str(required):
    e = Ex(["-e", "--example", "-x"], 2, float, required)
    assert str(e) == "-e|-x|--example <float> <float>"


@parametrize("required", (True, False))
def test_span_returns_correct_indices(required):
    number = 3
    thething = "b"
    find_in = "abcdefg"
    expected = "bcde"
    start, end = Ex(thething, number, None, required).span(find_in)
    assert find_in[start:end] == expected


def test_span_raises_missingoption_if_required_but_not_found():
    with pytest.raises(MissingOption):
        Ex("w", 1, identity, True).span("xyz")


def test_span_raises_indexerror_if_not_required_and_not_found():
    with pytest.raises(IndexError):
        Ex("w", 1, identity, False).span("xyz")


@parametrize("required", (True, False))
def test_span_with_fewer_arguments_than_expected_raises_argserror(required):
    with pytest.raises(ArgsError):
        Ex("x", 3, identity, required).span("xyz")


def test_missing_returns_none_if_number_is_1():
    class FakeExplicit:
        def __init__(self, number):
            self.number = number

    assert Ex.missing(FakeExplicit(1)) is None


def test_missing_returns_falsy_list_of_none_if_number_is_not_1():
    class FakeExplicit:
        def __init__(self, number):
            self.number = number

    length = 5
    missing = Ex.missing(FakeExplicit(length))
    assert isinstance(missing, list)
    assert len(missing) == length
    assert not missing


@parametrize("required", (True, False))
def test_found_returns_index_1_alone_if_it_only_takes_1_argument(required):
    # All it cares about should be args[1], in this case, "c"
    assert Ex("b", 1, identity, required).found("bcdef") == "c"


@parametrize("required", (True, False))
def test_found_returns_list_if_number_is_not_1(required):
    # It shouldn't actually care how many arguments it's supposed to
    # take, found just transforms the arguments it... found, whatever
    # those happen to be.
    assert Ex("b", -1, identity, required).found("bcdef") == list("cdef")


@parametrize("required", (True, False))
@parametrize("number, expected", [(1, [1]), (3, [1, 2, 3])])
def test_found_calls_transform_on_arguments(required, number, expected):
    accumulated = []

    def fn(value):
        nonlocal accumulated
        accumulated.append(value)
        return value

    Ex((), number, fn, required).found([0, 1, 2, 3])
    assert accumulated == expected
