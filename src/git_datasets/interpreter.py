""" Collection of utilities that extract information from the decorated class. """

from git_datasets.exceptions import InvalidInputType
from git_datasets.virtual_memory.abstract import VirtualMemory
from git_datasets.logging import get_logger
from git_datasets.types import (
    DecoratedClass, RelativePath,
    AnyFunction, DatasetPySchema,
      TypeCheckedArgs
)
from git_datasets.actions import Insert, Delete
from graphlib import TopologicalSorter
from functools import wraps
from typing import Any, get_type_hints, Any, Unpack
from collections import  Counter, OrderedDict

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

        attribute = getattr(cls, attribute_name, None)

        if attribute is not None:
            raise RuntimeError

        desired_schema[attribute_name] = cls.__annotations__[attribute_name]

    graph = TopologicalSorter()
    previous_method_name = ""

    for method_name in cls.__dict__:

        if method_name.startswith("_"):
            continue

        method = getattr(cls, method_name)
        type_hints = get_type_hints(method)
        return_type = type_hints.pop("return")

        if return_type not in [type(None), Insert]:
            desired_schema[method_name] = return_type


        dependency_transforms = [
            dependency_name
            for dependency_name in type_hints.keys()
            if dependency_name not in desired_schema
        ]

        graph.add(
            method_name,
            previous_method_name,
            *dependency_transforms
        )

        previous_method_name = method_name

    sorted_nodes = graph.static_order()
    sorted_nodes = iter(sorted_nodes)
    next(sorted_nodes, None)
    logger.debug("Dependency graph has been constructed.")

    with virtual_memory.open(parquet_file_path) as parquet_file:

        parquet_file.set_schema(desired_schema)

        logger.debug("Schema has been set")

        for transformation_name in sorted_nodes:
            transformation = getattr(cls, transformation_name)
            type_hints = get_type_hints(transformation)
            return_type = type_hints.pop("return")
            data = parquet_file.select(*type_hints.keys())

            if return_type == Delete:
                for id, *row in data:
                    if transformation(*row):
                        parquet_file.delete(id)

            elif return_type == type(None):
                
                for id, *row in data:
                    transformation(*row)

            elif return_type == Insert:
                fields = desired_schema.keys()

                if len(data) == 1 and data[0][0] is None:
                    to_insert = transformation()
                    parquet_file.insert(fields, to_insert)
                    continue

                for id, *row in data:
                    to_insert = transformation(*row)
                    parquet_file.insert(fields, to_insert)
            else:
                raise NotImplementedError





  