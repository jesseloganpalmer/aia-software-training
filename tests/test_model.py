import typing

import camia_model as model
import pytest

# from aviation._model import transform
from aviation import transforms


@model.transform
def add(x: float, y: float) -> float:
    return x + y


# Legacy code for _model.py
# def test_transform_decorator() -> None:
#     assert add.name == "add"
#     assert add.parameters == ("x", "y")


@pytest.mark.parametrize("transform", transforms)
def test_transform_decorator(transform: model.StandardTransform[typing.Any, ...]) -> None:
    assert model.is_transform(transform)
