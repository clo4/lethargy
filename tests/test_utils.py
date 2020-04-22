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


def test_falsylist_is_falsy():
    assert not lethargy.util.falsylist()
    assert not lethargy.util.falsylist([])
    assert not lethargy.util.falsylist([None])
    assert not lethargy.util.falsylist([1, 2, 3])


def test_fail_exits():
    with pytest.raises(SystemExit):
        lethargy.fail()


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
def test_fail_on(capsys, current_err):
    with contextlib.suppress(SystemExit):
        with lethargy.fail_on(ValueError, IndexError):
            raise current_err("Uh oh!")
    _, err = capsys.readouterr()
    assert err == "Uh oh!\n"


def test_show_errors(capsys):
    with contextlib.suppress(SystemExit):
        with lethargy.show_errors():
            raise lethargy.OptionError("damn")
    _, err = capsys.readouterr()
    assert err == "damn\n"
