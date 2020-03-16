# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

import sys

import lethargy


def test_argv_is_not_sys_argv():
    assert lethargy.argv is not sys.argv
