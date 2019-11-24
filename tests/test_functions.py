import pytest
from lethargy.lethargy import (
    Opt,
    dashed,
    kebabcase,
    print_if,
    skewer,
    take_debug,
    take_verbose,
)


def args():
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


@pytest.mark.parametrize(
    "text, expected",
    (
        ("word", "--word"),
        ("  word  ", "--  word  "),
        ("wor d", "--wor d"),
        ("  ", ""),
        ("c", "-c"),
    ),
)
def test_dashed(text, expected):
    assert dashed(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    (
        ("help", "help"),
        ("help me", "help-me"),
        ("help  me", "help-me"),
        ("  help me  ", "help-me"),
    ),
)
def test_kebabcase(text, expected):
    assert kebabcase(text) == expected


@pytest.mark.parametrize(
    "text, expected", (("test", "--test"), ("te st", "--te-st"), ("t", "-t"),)
)
def test_skewer(text, expected):
    assert skewer(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    (
        ("-a", True),
        ("-aa", False),
        ("-", False),
        ("a", False),
        ("--aa", False),
        ("--a", False),
    ),
)
def test_opt_is_short(text, expected):
    assert Opt.is_short(text) is expected


@pytest.mark.parametrize(
    "text, expected",
    (
        ("-a", False),
        ("-aa", False),
        ("-", False),
        ("a", False),
        ("--aa", True),
        ("--a", False),
    ),
)
def test_opt_is_long(text, expected):
    assert Opt.is_long(text) is expected


def test_print_if():
    assert print_if(True) is print
    assert print_if(False) is not print


def test_take_debug():
    lst = [0, "--debug", 1]
    assert take_debug(lst) is True
    assert lst == [0, 1]


@pytest.mark.parametrize("option", ("--verbose", "-v"))
def test_take_verbose(option):
    lst = [0, option, 1]
    assert take_verbose(lst) is True
    assert lst == [0, 1]
