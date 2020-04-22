# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

import sys

import lethargy


def test_argv_is_not_sys_argv():
    assert lethargy.argv is not sys.argv


def test_argv_equals_sys_argv():
    assert lethargy.argv == sys.argv


def test_falsylist_is_list():
    assert isinstance(lethargy.util.falsylist(), list)


def test_falsylist_is_falsy():
    assert not lethargy.util.falsylist()
    assert not lethargy.util.falsylist([])
    assert not lethargy.util.falsylist([None])
    assert not lethargy.util.falsylist([1, 2, 3])
