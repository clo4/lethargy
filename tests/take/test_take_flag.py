# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy import take_flag

x = str.split


def test_true_if_in_args():
    args = x("# -x #")
    assert take_flag("x", args=args) is True
    assert args == x("# #")


def test_no_mut_true_if_in_args():
    args = x("# -x #")
    assert take_flag("x", args=args, mut=False) is True
    assert args == x("# -x #")


@pytest.mark.parametrize("mut", (True, False))
def test_false_if_not_in_args(mut):
    args = x("# #")
    assert take_flag("x", args=args, mut=mut) is False
    assert args == x("# #")
