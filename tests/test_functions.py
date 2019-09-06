import pytest
from lethargy import take, dashed, kebabcase, skewer, Opt


def args():
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_take_0():
    a = args()
    assert take(0, 0, a) == []
    assert a == args()


def test_take_1():
    a = args()
    assert take(0, 1, a) == [0]
    assert a == args()[1:]


def test_take_1_middle():
    a = args()
    assert take(4, 1, a) == [4]
    assert a == args()[0:4] + args()[5:]


def test_take_end_overflow():
    a = args()
    assert take(8, 4, a) == [8, 9]
    assert a == args()[:8]


@pytest.mark.parametrize('text, expected', (
    ('word', '--word'),
    ('  word  ', '--  word  '),
    ('wor d', '--wor d'),
    ('  ', ''),
    ('c', '-c'),

))
def test_dashed(text, expected):
    assert dashed(text) == expected


@pytest.mark.parametrize('text, expected', (
    ('help', 'help'),
    ('help me', 'help-me'),
    ('help  me', 'help-me'),
    ('  help me  ', 'help-me'),
))
def test_kebabcase(text, expected):
    assert kebabcase(text) == expected


@pytest.mark.parametrize('text, expected', (
    ('test', '--test'),
    ('te st', '--te-st'),
    ('t', '-t'),
))
def test_skewer(text, expected):
    assert skewer(text) == expected


@pytest.mark.parametrize('text, expected', (
    ('-a', True),
    ('-aa', False),
    ('-', False),
    ('a', False),
    ('--aa', False),
    ('--a', False),
))
def test_opt_is_short(text, expected):
    assert Opt.is_short(text) is expected


@pytest.mark.parametrize('text, expected', (
    ('-a', False),
    ('-aa', False),
    ('-', False),
    ('a', False),
    ('--aa', True),
    ('--a', False),
))
def test_opt_is_long(text, expected):
    assert Opt.is_long(text) is expected
