"""Decorate functions as transforms."""

__all__ = ("Transform", "transform")

import collections.abc
import inspect
import typing


class Transform[T, **P](typing.Protocol):
    name: str
    parameters: tuple[str, ...]

    def __call__(*args: P.args, **kwargs: P.kwargs) -> T: ...


def transform[T, **P](function: collections.abc.Callable[P, T]) -> Transform[T, P]:
    """Decorator to identify a function as a transform."""
    transform = typing.cast("Transform[T, P]", function)
    transform.name = function.__name__
    transform.parameters = tuple(inspect.signature(function).parameters.keys())
    return transform
