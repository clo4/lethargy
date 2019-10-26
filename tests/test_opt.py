from copy import copy
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


@pytest.mark.parametrize("amt", (1, 2, 3, ...))
def test_take_args_no_mut(amt):
    in_args = [0, "-x", 0, 0, 0, 0]
    out_args = copy(in_args)

    Opt("x").takes(amt).take_args(in_args, mut=False)
    assert in_args == out_args


def test_take_flag_no_mut():
    in_args = [0, "-x", 0]
    out_args = copy(in_args)

    Opt("x").takes(amt).take_flag(in_args, mut=False)
    assert in_args == out_args


def test_find_in():
    # should find either -a or --aa
    o = Opt('a', 'aa')
    args_1 = [0, 1, '-a', 3, 4]
    args_2 = [0, 1, 2, '--aa', 4]
    assert o.find_in(args_1) == 2
    assert o.find_in(args_2) == 3


def test_takes():
    o = Opt()
    assert o.arg_amt == 0
    assert o.takes(1) is o
    assert o.arg_amt == 1


def test_new_takes():
    o = Opt()
    assert o.arg_amt == 0
    new = o.new_takes(1)
    assert new is not o
    assert new != o


def test_copy():
    original = Opt('test').takes(1)
    copied = original.__copy__()
    assert original is not copied
    assert original == copied


def test_eq():
    a = Opt('test').takes(1)
    b = Opt('test').takes(1)
    assert a == b
    b.arg_amt = 3
    assert a != b


def test_iter():
    a = Opt('test 1', 'test 2')
    assert set(iter(a)) == set(['--test-1', '--test-2'])


def test_converter_single_value():
    a = Opt('test').takes(1, int).take_args(['--test', '0'])
    assert isinstance(a, int)


@pytest.mark.parametrize("opt", (
    Opt('test').takes(2, int),
    Opt('test').takes(..., int)
))
def test_converter_multiple_values(opt):
    values = opt.take_args(['--test', '0', '1', '2', '3'])
    for val in values:
        assert isinstance(val, int)
