import sys
from lethargy import Argv


def test_opts():
    arg_lst = ["-a", "-aa", "--b", "--bb"]
    args = Argv(arg_lst)
    assert list(args.opts()) == [(0, "-a"), (3, "--bb")]


def test_from_argv():
    sys.argv = ["a", "b"]
    args = Argv.from_argv()
    assert args == sys.argv
    sys.argv = ["a", "b", "c"]
    assert args != sys.argv


def test_slicing():
    a = Argv([0, 1, 2, 3, 4])
    assert a[0] == 0
    assert a[0:2] == Argv([0, 1])
    assert a[::2] == Argv([0, 2, 4])


def test_addition():
    assert Argv([0]) + Argv([1]) == Argv([0, 1])


def test_multiplication():
    assert Argv([0]) * 3 == Argv([0, 0, 0])
