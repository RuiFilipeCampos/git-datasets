""" TODO"""

from git_datasets.logging import get_logger
from git_datasets.types import AnyFunction
from git_datasets.virtual_memory.abstract import FileInterface
from graphlib import TopologicalSorter
from typing import get_type_hints, Iterator, final
from abc import ABC, abstractmethod


__all__ = ["apply_transforms"]

logger = get_logger(__name__)


class Action(ABC):
    function: AnyFunction
    args: list[str]

    def __init__(self, function: AnyFunction, args: list[str]) -> None:
        self.function = function
        self.args = args

    @final
    def _select_args(self, parquet_file: FileInterface):
        return parquet_file.select(*self.args)

    @abstractmethod
    def __call__(self, parquet_file: FileInterface) -> None:
        ...


class Insert(Action):

    def __call__(self, parquet_file: FileInterface) -> None:

        fields = parquet_file.current_schema.keys()

        rows = self._select_args(parquet_file)

        if len(rows) == 1 and rows[0][0] is None:
            to_insert = self.function()
            parquet_file.insert(fields, to_insert)
            return

        for id, *row in rows:
            to_insert = self.function(*row)
            parquet_file.insert(fields, to_insert)

class Delete(Action):
    def __call__(self, parquet_file: FileInterface) -> None:
        rows = self._select_args(parquet_file)
        for id, *row in rows:
            if self.function(*row):
                parquet_file.delete(id)


class Alter(Action):
    ...

class NewField(Insert):
    ...

class DoNothing(Action):
    def __eq__(self, other):
        return other == type(None)

    def __call__(self, parquet_file: FileInterface) -> None:

        rows = self._select_args(parquet_file)

        for id, *row in rows:
            self.function(*row)


ACTIONS = {Insert, Delete, Alter, DoNothing}


class TransformsGraph(TopologicalSorter):

    _last_method_name: str
    _set_of_transforms: dict[str, Action]

    def __init__(self):
        super().__init__()
        self._last_method_name = ""
        self._set_of_transforms = {}

    def add(self, method: AnyFunction):

        type_hints = get_type_hints(method)
        return_type = type_hints.pop("return")
        args = type_hints.keys()

        dependency_transforms = [
            dependency_name for dependency_name in args
            if dependency_name in self._set_of_transforms
        ]

        if return_type == type(None):
            return_type = DoNothing

        self._set_of_transforms[method.__name__] = return_type(method, args)

        super().add(
            method.__name__,
            self._last_method_name,
            *dependency_transforms
        )

        self._last_method_name = method.__name__

        return return_type
    
    def static_order(self):
        sorted_nodes = super().static_order()
        sorted_nodes = iter(sorted_nodes)
        next(sorted_nodes, None)
        logger.debug("Dependency graph has been constructed.")
        return sorted_nodes
    
    def __iter__(self) -> Iterator[Action]:
        sorted_nodes: Iterator[str] = self.static_order()

        for transform_name in sorted_nodes:
            yield self._set_of_transforms[transform_name]
