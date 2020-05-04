# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy.options import Flag


def test_init():
    assert Flag("Names").names == "Names"


def test_str_is_prettynames():
    assert str(Flag("Very good")) == Flag("Very good").prettynames()


def test_found_is_always_true():
    assert Flag.found(None) is True


def test_missing_is_always_false():
    assert Flag.missing() is False


def test_span_raises_indexerror_if_not_in_args():
    with pytest.raises(IndexError):
        Flag(()).span([])


def test_span_returns_correct_indices():
    needle = "i"
    haystack = "abcdefghijklmopqrstuvwxyz"
    start, end = Flag(needle).span(haystack)
    assert haystack[start:end] == needle
