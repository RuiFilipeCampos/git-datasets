""" Collection of utilities that extract information from the decorated class. """

from git_datasets.virtual_memory.abstract import VirtualMemory
from git_datasets.logging import get_logger
from git_datasets.actions import TransformsGraph, ACTIONS
from git_datasets.types import DecoratedClass, RelativePath, DatasetPySchema
from git_datasets.exceptions import RepeatedAttributeError
from collections import  OrderedDict

__all__ = ["apply_transforms"]

logger = get_logger(__name__)

def apply_transforms(
    cls: DecoratedClass,
    virtual_memory: VirtualMemory,
    parquet_file_path: RelativePath,
) -> None:
    """ Constructs schema and dependency graph, and applies the transformations. """

    desired_schema: DatasetPySchema = OrderedDict()

    for attribute_name in cls.__annotations__:

        if attribute_name.startswith("_"):
            continue

        if attribute_name in desired_schema:
            raise RepeatedAttributeError(attribute_name)

        attribute = getattr(cls, attribute_name, None)

        if attribute is not None:
            # TODO make custom error here
            raise RuntimeError

        desired_schema[attribute_name] = cls.__annotations__[attribute_name]

    transforms_graph = TransformsGraph()

    for method_name in cls.__dict__:

        if method_name.startswith("_"):
            continue

        transform = getattr(cls, method_name)
        if not callable(transform):
            continue

        

        if method_name in desired_schema:
            raise RepeatedAttributeError(attribute_name)

        

        type_of_transform = transforms_graph.add(transform)

        if type_of_transform not in ACTIONS:
            desired_schema[method_name] = type_of_transform

    with virtual_memory.open(parquet_file_path) as parquet_file:

        parquet_file.set_schema(desired_schema)

        for transform in transforms_graph:
            rows = parquet_file.select(*transform.args)
            transform(parquet_file, rows)



  