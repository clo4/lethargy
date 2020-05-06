import pytest

from lethargy import take_all

parametrize = pytest.mark.parametrize
x = str.split


def test_takes_all_following_arguments():
    args = x("a b -x c d e")
    assert take_all("x", args=args) == x("c d e")
    assert args == x("a b")


def test_no_mut_takes_all_following_arguments():
    args = x("a b -x c d e")
    assert take_all("x", args=args, mut=False) == x("c d e")
    assert args == x("a b -x c d e")


# ---


def test_takes_all_following_arguments_and_calls_callable():
    args = x("2 1 -x 1 2 3")
    assert take_all("x", int, args=args) == [1, 2, 3]
    assert args == x("2 1")


def test_no_mut_takes_all_following_arguments_and_calls_callable():
    args = x("2 1 -x 1 2 3")
    assert take_all("x", int, args=args, mut=False) == [1, 2, 3]
    assert args == x("2 1 -x 1 2 3")


# ---


@pytest.mark.parametrize("mut", (True, False))
def test_no_args_found_is_empty_list(mut):
    args = x("# # a #")
    assert take_all("This shouldn't be found!", args=args, mut=mut) == []
    assert args == x("# # a #")
