# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

import pytest

import lethargy
from lethargy.option import Option


def all_args():
    return ["-a", "b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]


@pytest.fixture
def args():
    return all_args()


@pytest.mark.parametrize(
    "option, string",
    [
        # Flags
        (Option("x"), "-x"),
        (Option("mul"), "--mul"),
        (Option(["mul", "x"]), "-x|--mul"),
        # Options with arguments
        (Option("x", 1), "-x <value>"),
        (Option("mul", 1), "--mul <value>"),
        (Option(["mul", "x"], 1), "-x|--mul <value>"),
        (Option(["mul", "x"], 1, int), "-x|--mul <int>"),
        (Option(["mul", "x"], 1, lambda x: x), "-x|--mul <value>"),
        # Greedy options
        (Option("x", ...), "-x [value]..."),
        (Option("mul", ...), "--mul [value]..."),
        (Option(["mul", "x"], ...), "-x|--mul [value]..."),
        (Option(["mul", "x"], ..., int), "-x|--mul [int]..."),
        (Option(["mul", "x"], ..., lambda x: x), "-x|--mul [value]..."),
    ],
)
def test_string_form(option, string):
    assert str(option) == string


def test_take_flag(args):
    assert Option("a").take_flag(args) is True
    assert Option("w").take_flag(args) is False


def test_take_args_less_than_1_raises_err(args):
    with pytest.raises(RuntimeError):
        Option("a").take_args(args)


def test_argc_cannot_be_set_below_0():
    with pytest.raises(ValueError):
        Option("a", -1)


def test_take_args_1_returns_single_value(args):
    assert Option("a", 1).take_args(args) == "b"
    assert args == ["c", "-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_2_or_more_returns_list(args):
    assert Option("a", 2).take_args(args) == ["b", "c"]
    assert args == ["-d", "e", "--fgh", "i", "j", "-xyz"]


def test_take_args_valid_but_no_args_found_after_option():
    args = ["a", "b", "-c"]
    with pytest.raises(lethargy.ArgsError):
        Option("c", 1).take_args(args)
    assert args == ["a", "b", "-c"]


def test_take_args_greedy_returns_everything(args):
    expected = ["b", "c", "-d", "e", "--fgh", "i", "j", "-xyz"]
    assert Option("a", ...).take_args(args) == expected
    assert args == []


# opt not found, default none, raises false
def test_take_args_not_found_1_arg_returns_single_none(args):
    assert Option("w", 1).take_args(args) is None
    assert args == all_args()


def test_take_args_not_found_2_or_more_returns_none_list(args):
    assert Option("w", 2).take_args(args) == [None, None]
    assert args == all_args()


def test_take_args_not_found_greedy_returns_empty_list(args):
    assert Option("w", ...).take_args(args) == []
    assert args == all_args()


@pytest.mark.parametrize("amt", (2, ...))
def test_take_args_not_found_return_value_is_falsy(args, amt):
    assert not Option("w", amt).take_args(args)


# opt not found, default not none, raises true
@pytest.mark.parametrize("amt", (1, 2, ...))
def test_take_args_not_found_raises_true_raises_missingoption(args, amt):
    with pytest.raises(lethargy.MissingOption):
        assert Option("w", amt).take_args(args, required=True)


@pytest.mark.parametrize("amt", (1, 2, 3, ...))
def test_take_args_no_mut(amt):
    in_args = [0, "-x", 0, 0, 0, 0]
    out_args = in_args.copy()

    Option("x", amt).take_args(in_args, mut=False)
    assert in_args == out_args


def test_take_flag_no_mut():
    in_args = [0, "-x", 0]
    out_args = in_args.copy()

    Option("x").take_flag(in_args, mut=False)
    assert in_args == out_args


def test_find_in():
    # should find either -a or --aa
    o = Option(["a", "aa"])
    args_1 = [0, 1, "-a", 3, 4]
    args_2 = [0, 1, 2, "--aa", 4]
    assert o.find_in(args_1) == 2
    assert o.find_in(args_2) == 3


def test_converter_single_value():
    a = Option("test", 1, int).take_args(["--test", "0"])
    assert isinstance(a, int)


@pytest.mark.parametrize("opt", (Option("test", 2, int), Option("test", ..., int)))
def test_converter_multiple_values(opt):
    values = opt.take_args(["--test", "0", "1", "2", "3"])
    for val in values:
        assert isinstance(val, int)


def test_transform_calls_tfm_function_with_value():
    expected = []

    class TfmOpt:
        def tfm(self, value):
            return value

    assert Option.transform(TfmOpt(), expected) is expected


def test_transform_raises_exception_with_correct_exception():
    class CustomException(Exception):
        pass

    class TfmOpt:
        def tfm(self, _):
            raise CustomException

    with pytest.raises(CustomException):
        Option.transform(TfmOpt(), "")

    with pytest.raises(lethargy.TransformError):
        Option.transform(TfmOpt(), "")
