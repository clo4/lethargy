# Keep on separate lines for better diff and readability ~
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name

import pytest

from lethargy.errors import TransformError
from lethargy.mixins import Transforming


def test_metavar_gets_name_of_type_if_transformer_is_a_type():
    class Impl(Transforming):
        _transform = int

    assert Impl().metavar() == "int"


def test_metavar_gets_default_name_if_transformer_is_an_instance_of_something():
    class Impl(Transforming):
        default_metavar = "something"
        _transform = lambda x: x

    assert Impl().metavar() == Impl.default_metavar
    assert Impl().metavar() == "something"


def test_transform_calls_transformer_on_value():
    flag = False

    class Impl(Transforming):
        def _transform(self, value):
            nonlocal flag
            flag = True
            return value

    Impl().transform(None)
    assert flag is True


def test_transform_returns_result_of_transform_function():
    class Impl(Transforming):
        _transform = int

    assert Impl().transform("1") == 1


def test_transform_exception_raises_instance_of_causing_exception():
    class Impl(Transforming):
        _transform = int

    with pytest.raises(ValueError):
        Impl().transform("Not a number!")


def test_transform_exception_raises_transformerror():
    class Impl(Transforming):
        _transform = int

    with pytest.raises(TransformError):
        Impl().transform("Not a number!")


def test_original_exception_accessible_through_attribute():
    class Impl(Transforming):
        _transform = int

    try:
        Impl().transform("Not a string!")
    except TransformError as e:
        assert isinstance(e.__cause__, ValueError)
