# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy.mixins import Named


def test_prettynames_sorts_by_length_alphabetically():
    class Impl(Named):
        names = ("cc", "a", "zz", "aa", "fff", "b")

    assert Impl().prettynames() == "a|b|aa|cc|zz|fff"


def test_index_finds_correct_index():
    class Impl(Named):
        names = (99, 100)

    assert Impl().index([77, 88, 99, 100]) == 2
    assert Impl().index([77, 88, -1, 100]) == 3


def test_index_raises_indexerror_if_not_found():
    class Impl(Named):
        names = ()

    with pytest.raises(IndexError):
        Impl().index([])


def test_index_raises_exc_instead_of_indexerror_if_set():
    class Impl(Named):
        names = ()

    # Doesn't attempt to raise None.
    with pytest.raises(IndexError):
        Impl().index([], exc=None)

    # Works with the exception type.
    with pytest.raises(ValueError):
        Impl().index([], exc=ValueError)

    # Works with exception instances.
    with pytest.raises(ValueError):
        Impl().index([], exc=ValueError("Instance"))
