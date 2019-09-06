import sys
import lethargy


def test_opts():
    arg_lst = ['-a', '-aa', '--b', '--bb']
    args = lethargy.Argv(arg_lst)
    assert list(args.opts()) == [(0, '-a'), (3, '--bb')]


def test_from_argv():
    sys.argv = ['a', 'b']
    args = lethargy.Argv.from_argv()
    assert args == sys.argv
    sys.argv = ['a', 'b', 'c']
    assert args != sys.argv
