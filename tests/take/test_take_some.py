# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy import take_some, ArgsError, MissingOption

x = str.split


@pytest.mark.parametrize("name", ("x", ["not found", "x"]))
def test_take_one_is_single_value(name):
    args = x("# -x a #")
    assert take_some(name, 1, args=args) == "a"
    assert args == x("# #")


def test_no_mut_take_one_is_single_value():
    args = x("# -x a #")
    assert take_some("x", 1, args=args, mut=False) == "a"
    assert args == x("# -x a #")


# ---


def test_take_one_with_callable_is_single_value():
    args = x("# -x 1 #")
    assert take_some("x", 1, int, args=args) == 1
    assert args == x("# #")


def test_no_mut_take_one_with_callable_is_single_value():
    args = x("# -x 1 #")
    assert take_some("x", 1, int, args=args, mut=False) == 1
    assert args == x("# -x 1 #")


# ---


def test_take_one_with_callable_is_single_value():
    args = x("# -x 1 #")
    assert take_some("x", 1, int, args=args) == 1
    assert args == x("# #")


def test_no_mut_take_one_with_callable_is_single_value():
    args = x("# -x 1 #")
    assert take_some("x", 1, int, args=args, mut=False) == 1
    assert args == x("# -x 1 #")


# ---


def test_take_two_is_list():
    args = x("# -x a b #")
    assert take_some("x", 2, args=args) == ["a", "b"]
    assert args == x("# #")


def test_no_mut_take_two_is_list():
    args = x("# -x a b #")
    assert take_some("x", 2, args=args, mut=False) == ["a", "b"]
    assert args == x("# -x a b #")


# ---


def test_take_two_with_callable_is_list():
    args = x("# -x 1 2 #")
    assert take_some("x", 2, int, args=args) == [1, 2]
    assert args == x("# #")


def test_no_mut_take_two_with_callable_is_list():
    args = x("# -x 1 2 #")
    assert take_some("x", 2, int, args=args) == [1, 2]
    assert args == x("# #")


# ---


def test_using_number_under_one_raises_error():
    args = x("# -x a b #")
    with pytest.raises(ValueError):
        take_some("x", 0, args=args)
    assert args == x("# -x a b #")


def test_no_mut_using_number_under_one_raises_error():
    args = x("# -x a b #")
    with pytest.raises(ValueError):
        take_some("x", 0, args=args, mut=False)
    assert args == x("# -x a b #")


# ---


def test_must_have_at_least_n_arguments():
    args = x("# -x")
    with pytest.raises(ArgsError):
        take_some("x", 1, args=args)
    assert args == x("# -x")


def test_no_mut_must_have_at_least_n_arguments():
    args = x("# -x")
    with pytest.raises(ArgsError):
        take_some("x", 1, args=args, mut=False)
    assert args == x("# -x")


# ---


def test_must_have_at_least_n_arguments_with_callable():
    args = x("# -x")
    with pytest.raises(ArgsError):
        take_some("x", 1, int, args=args)
    assert args == x("# -x")


def test_no_mut_must_have_at_least_n_arguments_with_callable():
    args = x("# -x")
    with pytest.raises(ArgsError):
        take_some("x", 1, int, args=args, mut=False)
    assert args == x("# -x")


# ---


def test_required_argument_must_be_present():
    args = x("# # #")
    with pytest.raises(MissingOption):
        take_some("x", 1, required=True, args=args)
    assert args == x("# # #")


def test_required_argument_must_be_present():
    args = x("# # #")
    with pytest.raises(MissingOption):
        take_some("x", 1, required=True, args=args, mut=False)
    assert args == x("# # #")
