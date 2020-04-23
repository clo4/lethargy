# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

import contextlib
import sys

import pytest

import lethargy


def test_argv_is_not_sys_argv():
    assert lethargy.argv is not sys.argv


def test_argv_equals_sys_argv():
    assert lethargy.argv == sys.argv


def test_falsylist_is_list():
    assert isinstance(lethargy.util.falsylist(), list)


def test_falsylist_is_always_falsy():
    # falsylist should not require itself to return false -- it's always falsy.
    assert lethargy.util.falsylist.__bool__(None) is False


@pytest.mark.parametrize("message", (None, "Message"))
def test_fail_exits(message):
    with pytest.raises(SystemExit):
        lethargy.fail(message)


@pytest.mark.parametrize("message", (None, "Message"))
def test_fail_exits_with_code_1(message):
    try:
        lethargy.fail(message)
    except SystemExit as e:
        assert e.code == 1


def test_fail_prints_message_to_stderr(capsys):
    with contextlib.suppress(SystemExit):
        lethargy.fail("Message!")
    out, err = capsys.readouterr()
    assert err == "Message!\n"
    assert out == ""


def test_fail_without_message_prints_nothing(capsys):
    with contextlib.suppress(SystemExit):
        lethargy.fail()
    out, err = capsys.readouterr()
    assert out == err == ""


@pytest.mark.parametrize("current_err", (ValueError, IndexError))
def test_expect(capsys, current_err):
    with contextlib.suppress(SystemExit):
        with lethargy.expect(ValueError, IndexError):
            raise current_err("Uh oh!")
    _, err = capsys.readouterr()
    assert err == "Uh oh!\n"


def test_expect_custom_message_overrides_exception_message(capsys):
    with contextlib.suppress(SystemExit):
        with lethargy.expect(RuntimeError, reason="yikes"):
            raise RuntimeError("Uh oh!")
    _, err = capsys.readouterr()
    assert err == "yikes\n"


def test_show_errors(capsys):
    with contextlib.suppress(SystemExit):
        with lethargy.show_errors():
            raise lethargy.OptionError("damn")
    _, err = capsys.readouterr()
    assert err == "damn\n"
