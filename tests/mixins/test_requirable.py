# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

from lethargy.mixins import Requirable
from lethargy.errors import MissingOption


def test_check_required_returns_missingoption_if_required():
    class Impl(Requirable):
        required = True

    assert isinstance(Impl().check_required(), MissingOption)


def test_check_required_returns_none_if_not_required():
    class Impl(Requirable):
        required = False

    assert Impl().check_required() is None
