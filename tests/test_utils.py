# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

import contextlib
import sys

import pytest

import lethargy
from lethargy import util

parametrize = pytest.mark.parametrize


def test_argv_is_not_sys_argv():
    assert util.argv is not sys.argv


def test_argv_equals_sys_argv():
    assert util.argv == sys.argv


def test_falsylist_is_list():
    assert isinstance(util.falsylist(), list)
    assert isinstance(util.falsylist, type)


def test_falsylist_is_always_falsy():
    # falsylist should not require itself to return false -- it's always falsy.
    assert util.falsylist.__bool__(None) is False


@parametrize("message", (None, "Message"))
def test_fail_exits(message):
    with pytest.raises(SystemExit):
        util.fail(message)


@parametrize("message", (None, "Message"))
def test_fail_exits_with_code_1(message):
    try:
        util.fail(message)
    except SystemExit as error:
        assert error.code == 1


def test_fail_prints_message_to_stderr(capsys):
    with contextlib.suppress(SystemExit):
        util.fail("Message!")
    out, err = capsys.readouterr()
    assert err == "Message!\n"
    assert out == ""


def test_fail_without_message_prints_nothing(capsys):
    with contextlib.suppress(SystemExit):
        util.fail()
    out, err = capsys.readouterr()
    assert out == err == ""


@parametrize("current_err", (ValueError, IndexError))
def test_expect(capsys, current_err):
    with contextlib.suppress(SystemExit):
        with util.expect(ValueError, IndexError):
            raise current_err("Uh oh!")
    _, err = capsys.readouterr()
    assert err == "Uh oh!\n"


def test_expect_custom_message_overrides_exception_message(capsys):
    with contextlib.suppress(SystemExit):
        with util.expect(RuntimeError, reason="yikes"):
            raise RuntimeError("Uh oh!")
    _, err = capsys.readouterr()
    assert err == "yikes\n"


def test_show_errors(capsys):
    with contextlib.suppress(SystemExit):
        with util.show_errors():
            raise util.OptionError("damn")
    _, err = capsys.readouterr()
    assert err == "damn\n"


def test_identity():
    o = object()
    assert util.identity(o) is o


def test_try_name():
    assert util.try_name("test") == "--test"
    assert util.try_name("t") == "-t"
    assert util.try_name("1") == "-1"
    assert util.try_name("-1") == "-1"
    assert util.try_name("-t") == "-t"
    assert util.try_name("-test") == "-test"
    assert util.try_name("+1") == "+1"


def test_try_name_fails_on_empty_name():
    with pytest.raises(ValueError):
        util.try_name("")


def test_names_from():
    assert util.names_from("x") == {"-x"}
    assert util.names_from(["x"]) == {"-x"}
    assert util.names_from(["x", "y"]) == {"-x", "-y"}

    with pytest.raises(ValueError):
        util.names_from("")

    with pytest.raises(ValueError):
        util.names_from([])

    with pytest.raises(ValueError):
        util.names_from([""])
