# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

from copy import copy

import pytest

import lethargy
from lethargy import Opt


def all_args():
    return ["-a", "b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]


@pytest.fixture
def args():
    return all_args()


@pytest.mark.parametrize(
    "option, string",
    [
        # Flags
        (Opt("x"), "-x"),
        (Opt("mul"), "--mul"),
        (Opt("mul", "x"), "-x|--mul"),
        # Options with arguments
        (Opt("x").takes(1), "-x <value>"),
        (Opt("mul").takes(1), "--mul <value>"),
        (Opt("mul", "x").takes(1), "-x|--mul <value>"),
        (Opt("mul", "x").takes(1, int), "-x|--mul <int>"),
        (Opt("mul", "x").takes(1, lambda x: x), "-x|--mul <value>"),
        # Greedy options
        (Opt("x").takes(...), "-x [value]..."),
        (Opt("mul").takes(...), "--mul [value]..."),
        (Opt("mul", "x").takes(...), "-x|--mul [value]..."),
        (Opt("mul", "x").takes(..., int), "-x|--mul [int]..."),
        (Opt("mul", "x").takes(..., lambda x: x), "-x|--mul [value]..."),
    ],
)
def test_string_form(option, string):
    assert str(option) == string


def test_take_flag(args):
    assert Opt("a").take_flag(args) is True
    assert Opt("w").take_flag(args) is False


def test_take_args_less_than_1_raises_err(args):
    with pytest.raises(lethargy.ArgsError):
        Opt("a").take_args(args)
    with pytest.raises(lethargy.ArgsError):
        x = Opt("a")
        x._argc = -1
        x.take_args(args)
    assert args == all_args()


def test_take_args_1_returns_single_value(args):
    assert Opt("a").takes(1).take_args(args) == "b"
    assert args == ["c", "-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_2_or_more_returns_list(args):
    assert Opt("a").takes(2).take_args(args) == ["b", "c"]
    assert args == ["-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_valid_but_no_args_found_after_option():
    args = ["a", "b", "-c"]
    with pytest.raises(lethargy.ArgsError):
        Opt("c").takes(1).take_args(args)
    assert args == ["a", "b", "-c"]


def test_take_args_greedy_returns_everything(args):
    expected = ["b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]
    assert Opt("a").takes(...).take_args(args) == expected
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


@pytest.mark.parametrize("amt", (2, ...))
def test_take_args_not_found_default_none_return_value_is_falsy(args, amt):
    assert not Opt("w").takes(amt).take_args(args)


# opt not found, default not none, raises false
@pytest.mark.parametrize("amt", (1, 2, ...))
def test_take_args_not_found_default_not_none_returns_default(args, amt):
    assert Opt("w").takes(amt).take_args(args, d=1) == 1


# opt not found, default not none, raises true
@pytest.mark.parametrize("amt", (1, 2, ...))
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

    Opt("x").take_flag(in_args, mut=False)
    assert in_args == out_args


def test_find_in():
    # should find either -a or --aa
    o = Opt("a", "aa")
    args_1 = [0, 1, "-a", 3, 4]
    args_2 = [0, 1, 2, "--aa", 4]
    assert o._find_in(args_1) == 2
    assert o._find_in(args_2) == 3


def test_takes():
    o = Opt()
    assert o._argc == 0
    assert o.takes(1) is o
    assert o._argc == 1


def test_copy():
    original = Opt("test").takes(1)
    copied = original.__copy__()
    assert original is not copied
    assert original == copied


def test_eq():
    assert Opt().takes(1) == Opt().takes(1)
    assert Opt("test").takes(1) != Opt().takes(1)

    assert Opt().takes(1) == Opt().takes(1)
    assert Opt().takes(2) != Opt().takes(1)

    assert Opt().takes(1, int) == Opt().takes(1, int)
    assert Opt().takes(1, int) != Opt().takes(1)


def test_converter_single_value():
    a = Opt("test").takes(1, int).take_args(["--test", "0"])
    assert isinstance(a, int)


@pytest.mark.parametrize(
    "opt", (Opt("test").takes(2, int), Opt("test").takes(..., int))
)
def test_converter_multiple_values(opt):
    values = opt.take_args(["--test", "0", "1", "2", "3"])
    for val in values:
        assert isinstance(val, int)


def test_transform_calls_tfm_function_with_value():
    expected = []

    class MockOpt:
        def _tfm(self, value):
            return value

    assert Opt._transform(MockOpt(), expected) is expected


def test_transform_raises_exception_with_correct_exception():
    class CustomException(Exception):
        pass

    class MockOpt:
        def _tfm(self, _):
            raise CustomException

    with pytest.raises(CustomException):
        Opt._transform(MockOpt(), "")

    with pytest.raises(lethargy.TransformError):
        Opt._transform(MockOpt(), "")
