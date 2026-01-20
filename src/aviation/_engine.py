"""Evaluate systems model of transforms."""

__all__ = ("SystemsModel",)

import collections.abc
import typing

from aviation._model import Transform


class SystemsModel:
    """A systems model defined by a collection of transform."""

    def __init__(self, transforms: collections.abc.Sequence[Transform[typing.Any, ...]]) -> None:
        """Initialize the systems model from a collection of transforms."""
        self.transforms = set(transforms)

    def evaluate(self, inputs: dict[str, typing.Any], output: str) -> typing.Any:  # noqa: ANN401
        """Calculate the value returned by a transform.

        This implementation uses recursion to recursively evaluate the arguments required by a
        transform if they aren't already known. The algorithm has four steps:
        1. Check to see if the requested `output` is already a known member of `inputs`. If it is
        then the value can be returned without the need for any computation.
        2. Find the function who's name matches `output` as this is what needs to be evaluated in
        this call. If no transform can be found with a matching name then it won't be possible to
        continue evaluation and an error must be raised.
        3. Build a mapping of the transform's parameters to the arguments that will be used to
        evaluate the transform. If the value of the parameter isn't currently known then make a
        recursive call to `self.evaluate` and insert the parameter name-value pair back into
        `inputs` for its reuse later.
        4. Evaluate the transform using the keyword arguments and return the value.
        """
        # If the requested `output` has already been supplied as an input then this can just be
        # returned directly without any need for computation.
        if output in inputs:
            return inputs[output]

        # The requested `output` isn't in `inputs` so it must be the name of a transform in
        # `self.transforms`. If it's not found in `self.transforms` then there must be an error.
        for transform in self.transforms:
            if transform.name == output:
                break
        else:
            message = f"Unknown transform: {output}"
            raise ValueError(message)

        # To evaluate the `transform`, arguments for all of its parameters are required. If a
        # parameter's name can't be found in `inputs` make a recursive call to `self.evaluate` to
        # evaluate it and then insert it into `inputs`.
        for parameter in transform.parameters:
            if parameter not in inputs:
                inputs[parameter] = self.evaluate(inputs, parameter)

        # Evaluate and return the `transform` associated with the passed `output`.
        arguments = {parameter: inputs[parameter] for parameter in transform.parameters}
        return transform(**arguments)
