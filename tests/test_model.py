from aviation._model import transform


@transform
def add(x: float, y: float) -> float:
    return x + y


def test_transform_decorator() -> None:
    assert add.name == "add"
    assert add.parameters == ("x", "y")
