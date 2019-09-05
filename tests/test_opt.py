import lethargy
from lethargy import Opt
import pytest


def all_args():
    return ["-a", "b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]


@pytest.fixture
def args():
    return all_args()


def test_take_flag(args):
    assert Opt("a").take_flag(args) is True
    assert Opt("w").take_flag(args) is False


# opt found
def test_take_args_0_args_raises_err(args):
    with pytest.raises(lethargy.ArgsError):
        Opt("a").take_args(args)  # raises ArgsError
    assert args == all_args()


def test_take_args_1_returns_single_value(args):
    assert Opt("a").takes(1).take_args(args) == "b"
    assert args == ["c", "-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_2_or_more_returns_list(args):
    assert Opt("a").takes(2).take_args(args) == ["b", "c"]
    assert args == ["-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_valid_but_no_args_found_after_option():
    args = ['a', 'b', '-c']
    with pytest.raises(lethargy.ArgsError):
        Opt("c").takes(1).take_args(args)
    assert args == ['a', 'b', '-c']


@pytest.mark.parametrize("greedy_op", (..., any, lethargy.greedy, "*"))
def test_take_args_greedy_returns_everything(args, greedy_op):
    expected = ["b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]
    assert Opt("a").takes(greedy_op).take_args(args) == expected
    assert args == []


# opt not found, default none, raises false
def test_take_args_not_found_default_none_1_arg_returns_single_none(args):
    assert Opt("w").takes(1).take_args(args) is None
    assert args == all_args()


def test_take_args_not_found_default_none_2_or_more_returns_none_list(args):
    assert Opt("w").takes(2).take_args(args) == [None, None]
    assert args == all_args()


def test_take_args_not_found_default_none_greedy_returns_empty_list(args):
    assert Opt("w").takes(...).take_args(args) == []
    assert args == all_args()


# opt not found, default not none, raises false
@pytest.mark.parametrize("amt", (1, 2, *lethargy.GREEDY_VALUES))
def test_take_args_not_found_default_not_none_returns_default(args, amt):
    assert Opt("w").takes(amt).take_args(args, default=1) == 1


# opt not found, default not none, raises true
@pytest.mark.parametrize("amt", (1, 2, *lethargy.GREEDY_VALUES))
def test_take_args_not_found_raises_true_raises_missingoption(args, amt):
    with pytest.raises(lethargy.MissingOption):
        assert Opt("w").takes(amt).take_args(args, raises=True)
