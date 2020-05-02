# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

"""
## What needs to be tested?

- [x] init
- [x] string form shows metavars

- [ ] span returns correct start and end indices
- [ ] span raises missingoption if option is required and not found
- [ ] span raises indexerror if option is not required and not found
- [ ] span with fewer arguments than expected raises argserror

- [x] missing returns none if number is 1
- [x] missing returns falsy list of none if number is not 1

- [ ] found returns single value if number is 1
- [ ] found returns list if number is not 1
- [ ] found calls transform on arguments

"""

import pytest

from lethargy.options import Explicit as Ex


def test_init():
    a, b, c, d = object(), object(), object(), object()
    e = Ex(a, b, c, d)
    assert e.names is a
    assert e.number is b
    assert e._transform is c
    assert e.required is d


def test_str():
    e = Ex(["-e", "--example", "-x"], 2, float, None)
    assert str(e) == "-e|-x|--example <float> <float>"


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
