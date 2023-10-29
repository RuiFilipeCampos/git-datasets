""" Collection of utilities that extract information from the decorated class. """

from git_datasets.exceptions import RepeatedAttributeError
from git_datasets.types import DecoratedClass, RelativePath, AnyFunction
from git_datasets.virtual_memory.abstract import VirtualMemory

from typing import TypedDict, Any, Callable
from collections import OrderedDict


class Action(TypedDict):
    function: Callable
    type_hints: dict[str, Any]

def apply_transforms(
    cls: DecoratedClass,
    virtual_memory: VirtualMemory,
    path: RelativePath
) -> None:
    """ Constructs schema and dependency graph, and applies the transformations. """

    # pylint: disable=import-outside-toplevel
    # reason: delaying imports until needed
    from typing import get_type_hints
    from git_datasets.types import Action


    desired_schema = {}
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
        attribute = getattr(cls, attribute_name)
        if not callable(attribute):
            continue
        
        attribute: AnyFunction
        type_hints = get_type_hints(attribute)
        return_type = type_hints.pop("return")
        if return_type not in [Action.Insert, Action.Alter, Action.Delete, None]:
            desired_schema[attribute_name] = return_type

        for dependency_name in type_hints:
            if dependency_name not in transforms_graph:
                raise ValueError("Transform depends on something that has not yet been defined.")

        transforms_graph[attribute_name] = (attribute_name, attribute, type_hints)

    with virtual_memory.open(path) as parquet_file:
        parquet_file.set_schema(desired_schema)
        results = {}
        for attribute_name, transform, type_hints in transforms_graph:
            args = [results[dependency_name] for dependency_name in type_hints]
            results[attribute_name] = transform(*args)


def get_dataset_name(cls: DecoratedClass) -> str:
    """ TODO """

    return cls.__name__.lower()
