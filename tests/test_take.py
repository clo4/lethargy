# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy.options import take


@pytest.mark.parametrize("mut", (True, False))
def test_missing_called_if_span_raises_indexerror(mut):
    class FunctionCalled(Exception):
        pass

    class Fake:
        def span(self, args):
            raise IndexError

        def missing(self):
            raise FunctionCalled

    with pytest.raises(FunctionCalled):
        take(Fake(), None, mut=mut)


@pytest.mark.parametrize("mut", (True, False))
def test_missing_can_raise_other_exceptions(mut):
    class CustomException(Exception):
        pass

    class Fake:
        def span(self, args):
            raise CustomException

    with pytest.raises(CustomException):
        take(Fake(), None, mut=mut)


@pytest.mark.parametrize("mut", (True, False))
def test_found_is_called_with_items_from_span_if_span_does_not_raise_indexerror(mut):
    class FunctionCalled(Exception):
        pass

    expecting = None

    class Fake:
        def span(self, args):
            nonlocal expecting
            expecting = args[3:5]
            return 3, 5

        def found(self, args):
            raise FunctionCalled(args)

    try:
        take(Fake(), "abcdefgh", mut=mut)
    except FunctionCalled as f:
        assert str(f) == expecting


@pytest.mark.parametrize(
    "mut, expected", [(True, [0, 1, 4, 5]), (False, [0, 1, 2, 3, 4, 5])]
)
def test_only_removes_items_from_span_if_mut_is_true(mut, expected):
    class Fake:
        def span(self, _):
            return 2, 4

        def found(self, _):
            return None

    args = [0, 1, 2, 3, 4, 5]
    take(Fake(), args=args, mut=mut)
    assert args == expected


def test_span_can_return_none_tuple():
    class FunctionCalled(Exception):
        pass

    class Fake:
        def span(self, _):
            return None, None

        def found(self, args):
            raise FunctionCalled(args)

    try:
        take(Fake(), "help me")
    except FunctionCalled as f:
        assert str(f) == "help me"


@pytest.mark.parametrize("mut", (True, False))
def test_take_returns_result_of_found(mut):
    class Fake:
        def span(self, _):
            return 0, 0

        def found(self, _):
            return "something completely different"

    assert take(Fake(), [], mut=mut) == "something completely different"
