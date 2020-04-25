# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

from copy import copy

import pytest

import lethargy
from lethargy.option import Opt


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
        (Opt(["mul", "x"]), "-x|--mul"),
        # Options with arguments
        (Opt("x", 1), "-x <value>"),
        (Opt("mul", 1), "--mul <value>"),
        (Opt(["mul", "x"], 1), "-x|--mul <value>"),
        (Opt(["mul", "x"], 1, int), "-x|--mul <int>"),
        (Opt(["mul", "x"], 1, lambda x: x), "-x|--mul <value>"),
        # Greedy options
        (Opt("x", ...), "-x [value]..."),
        (Opt("mul", ...), "--mul [value]..."),
        (Opt(["mul", "x"], ...), "-x|--mul [value]..."),
        (Opt(["mul", "x"], ..., int), "-x|--mul [int]..."),
        (Opt(["mul", "x"], ..., lambda x: x), "-x|--mul [value]..."),
    ],
)
def test_string_form(option, string):
    assert str(option) == string


def test_take_flag(args):
    assert Opt("a").take_flag(args) is True
    assert Opt("w").take_flag(args) is False


def test_take_args_less_than_1_raises_err(args):
    with pytest.raises(RuntimeError):
        Opt("a").take_args(args)


def test_argc_cannot_be_set_below_0():
    with pytest.raises(ValueError):
        Opt("a", -1)


def test_take_args_1_returns_single_value(args):
    assert Opt("a", 1).take_args(args) == "b"
    assert args == ["c", "-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_2_or_more_returns_list(args):
    assert Opt("a", 2).take_args(args) == ["b", "c"]
    assert args == ["-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_valid_but_no_args_found_after_option():
    args = ["a", "b", "-c"]
    with pytest.raises(lethargy.ArgsError):
        Opt("c", 1).take_args(args)
    assert args == ["a", "b", "-c"]


def test_take_args_greedy_returns_everything(args):
    expected = ["b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]
    assert Opt("a", ...).take_args(args) == expected
    assert args == []


# opt not found, default none, raises false
def test_take_args_not_found_1_arg_returns_single_none(args):
    assert Opt("w", 1).take_args(args) is None
    assert args == all_args()


def test_take_args_not_found_2_or_more_returns_none_list(args):
    assert Opt("w", 2).take_args(args) == [None, None]
    assert args == all_args()


def test_take_args_not_found_greedy_returns_empty_list(args):
    assert Opt("w", ...).take_args(args) == []
    assert args == all_args()


@pytest.mark.parametrize("amt", (2, ...))
def test_take_args_not_found_return_value_is_falsy(args, amt):
    assert not Opt("w", amt).take_args(args)


# opt not found, default not none, raises true
@pytest.mark.parametrize("amt", (1, 2, ...))
def test_take_args_not_found_raises_true_raises_missingoption(args, amt):
    with pytest.raises(lethargy.MissingOption):
        assert Opt("w", amt).take_args(args, required=True)


@pytest.mark.parametrize("amt", (1, 2, 3, ...))
def test_take_args_no_mut(amt):
    in_args = [0, "-x", 0, 0, 0, 0]
    out_args = copy(in_args)

    Opt("x", amt).take_args(in_args, mut=False)
    assert in_args == out_args


def test_take_flag_no_mut():
    in_args = [0, "-x", 0]
    out_args = copy(in_args)

    Opt("x").take_flag(in_args, mut=False)
    assert in_args == out_args


def test_find_in():
    # should find either -a or --aa
    o = Opt(["a", "aa"])
    args_1 = [0, 1, "-a", 3, 4]
    args_2 = [0, 1, 2, "--aa", 4]
    assert o.find_in(args_1) == 2
    assert o.find_in(args_2) == 3


def test_copy():
    original = Opt("test", 1)
    copied = original.__copy__()
    assert original is not copied
    assert original == copied


def test_eq():
    assert Opt([], 1) == Opt([], 1)
    assert Opt("test", 1) != Opt([], 1)

    assert Opt([], 1) == Opt([], 1)
    assert Opt([], 2) != Opt([], 1)

    assert Opt([], 1, int) == Opt([], 1, int)
    assert Opt([], 1, int) != Opt([], 1)


def test_converter_single_value():
    a = Opt("test", 1, int).take_args(["--test", "0"])
    assert isinstance(a, int)


@pytest.mark.parametrize("opt", (Opt("test", 2, int), Opt("test", ..., int)))
def test_converter_multiple_values(opt):
    values = opt.take_args(["--test", "0", "1", "2", "3"])
    for val in values:
        assert isinstance(val, int)


def test_transform_calls_tfm_function_with_value():
    expected = []

    class TfmOpt:
        def tfm(self, value):
            return value

    assert Opt.transform(TfmOpt(), expected) is expected


def test_transform_raises_exception_with_correct_exception():
    class CustomException(Exception):
        pass

    class TfmOpt:
        def tfm(self, _):
            raise CustomException

    with pytest.raises(CustomException):
        Opt.transform(TfmOpt(), "")

    with pytest.raises(lethargy.TransformError):
        Opt.transform(TfmOpt(), "")
