""" TODO"""

from git_datasets.logging import get_logger
from git_datasets.types import AnyFunction
from git_datasets.virtual_memory.abstract import FileInterface
from typing import final
from abc import ABC, abstractmethod


logger = get_logger(__name__)


class Action(ABC):
    """ TODO """

    function: AnyFunction
    args: list[str]

    def __init__(self, function: AnyFunction, args: list[str]) -> None:
        """ TODO """

        self.function = function
        self.args = args

    @final
    def _select_args(self, parquet_file: FileInterface):
        """ TODO """

        return parquet_file.select(*self.args)

    @abstractmethod
    def __call__(self, parquet_file: FileInterface) -> None:
        """ TODO """
        ...


class Insert(Action):
    """ TODO """

    def __call__(self, parquet_file: FileInterface) -> None:
        """ TODO """

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
    """ TODO """
    def __call__(self, parquet_file: FileInterface) -> None:
        """ TODO """
        rows = self._select_args(parquet_file)
        for id, *row in rows:
            if self.function(*row):
                parquet_file.delete(id)


class Alter(Action):
    """ TODO """
    ...

class NewField(Insert):
    """ TODO """
    ...

class DoNothing(Action):
    """ TODO """
    def __eq__(self, other):
        """ TODO """
        return other == type(None)

    def __call__(self, parquet_file: FileInterface) -> None:
        """ TODO """

        rows = self._select_args(parquet_file)

        for id, *row in rows:
            self.function(*row)


ACTIONS = {Insert, Delete, Alter, DoNothing}


