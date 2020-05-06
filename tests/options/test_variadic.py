# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy.options import Variadic as Var
from lethargy.util import identity


def test_init():
    v = Var("Name", float)
    assert v.names == "Name"
    assert v._transform is float


def test_str():
    assert str(Var(["-v", "--variadic"], int)) == "-v|--variadic [int]..."
    assert str(Var(["-v", "--variadic"], identity)) == "-v|--variadic [value]..."


def test_missing_is_always_empty_list():
    assert Var.missing() == []


def test_found_transforms_each_argument_after_first():
    rv = Var((), int).found(["x", "1", "2", "3", "4"])
    assert rv == [1, 2, 3, 4]


def test_span():
    thing_to_find = "e"
    args = list("abcdefghijklmnopqrstuvwxyz")
    expected = list("efghijklmnopqrstuvwxyz")
    start, end = Var(thing_to_find, identity).span(args)
    assert args[start:end] == expected


def test_span_raises_indexerror_if_target_is_not_in_list():
    with pytest.raises(IndexError):
        Var((), identity).span(())
