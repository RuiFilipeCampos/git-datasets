""" Collection of utilities that extract information from the decorated class. """

from git_datasets.exceptions import RepeatedAttributeError, InvalidInputType
from git_datasets.virtual_memory.abstract import VirtualMemory
from git_datasets.types import (
    DecoratedClass, RelativePath,
    AnyFunction, DatasetPySchema,
    PyType, Action, TypeCheckedArgs
)
from functools import wraps
from typing import Any, get_type_hints, Any, Unpack
from collections import OrderedDict, Counter

__all__ = ["apply_transforms"]

def apply_transforms(
    cls: DecoratedClass,
    virtual_memory: VirtualMemory,
    parquet_file_path: RelativePath,
) -> None:
    """ Constructs schema and dependency graph, and applies the transformations. """

    # pylint: disable=import-outside-toplevel
    # reason: delaying imports until needed


    desired_schema: DatasetPySchema = {}
    field_selectors = {}
    # reference counting mechanism 
    columns_to_select: Counter[str] = Counter()
    selected_columns = {}
    transforms_graph: OrderedDict[str, AnyFunction] = OrderedDict()

    for attribute_name in cls.__annotations__:

        # prohibit repeated naming
        if attribute_name in desired_schema:
            raise RepeatedAttributeError(attribute_name)

        # exclude dunder methods and attributes
        # exclude private methods and attributes
        if attribute_name.startswith("_"):
            continue

        # exclude attributes
        attribute_or_method = getattr(cls, attribute_name)
        if not callable(attribute_or_method):
            continue
        
        method: AnyFunction = attribute_or_method
        type_hints = get_type_hints(method)
        return_type = type_hints.pop("return")

        # TODO turn this into typegard
        if return_type not in Action:
            if return_type not in PyType:
                # TODO raise custom error
                raise RuntimeError

            desired_schema[attribute_name] = return_type

        for dependency_name in type_hints:

            if dependency_name in desired_schema:
                columns_to_select.update([dependency_name])
                continue

            if dependency_name not in transforms_graph:
                # TODO turn this into custom error
                msg = "Transform depends on something that has not yet been defined."
                raise ValueError(msg)

        transforms_graph[attribute_name] = (attribute_name, method, type_hints)

    with virtual_memory.open(parquet_file_path) as parquet_file:
        parquet_file.set_schema(desired_schema)
        results = {}
        for attribute_name, transform, type_hints in transforms_graph:
            args = [results[dependency_name] for dependency_name in type_hints]
            results[attribute_name] = transform(*args)



def validate_arguments(function: AnyFunction) -> TypeCheckedArgs[AnyFunction]:
    """ Runtime validation of function arguments. """

    @wraps(function)
    def wrapper(*args: Unpack[Any], **kwargs: Unpack[Any]) -> Any:
        hints = get_type_hints(function)
        for name, value in kwargs.items():
            expected_type = hints.get(name)

            if expected_type is None:
                continue

            if not isinstance(value, expected_type):
                raise InvalidInputType(name, expected_type, value)

        return function(*args, **kwargs)
    return wrapper

