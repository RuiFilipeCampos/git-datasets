""" TODO"""

from git_datasets.logging import get_logger
from git_datasets.types import AnyFunction
from git_datasets.actions import Action, DoNothing


from graphlib import TopologicalSorter
from typing import get_type_hints, Iterator

logger = get_logger(__name__)


class TransformsGraph(TopologicalSorter):
    """ TODO """

    _last_method_name: str
    _set_of_transforms: dict[str, Action]

    def __init__(self):
        """ TODO """
        super().__init__()
        self._last_method_name = ""
        self._set_of_transforms = {}

    def add(self, method: AnyFunction):
        """ TODO """

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
        """ TODO """
        sorted_nodes = super().static_order()
        sorted_nodes = iter(sorted_nodes)
        next(sorted_nodes, None)
        logger.debug("Dependency graph has been constructed.")
        return sorted_nodes
    
    def __iter__(self) -> Iterator[Action]:
        """ TODO """
        sorted_nodes: Iterator[str] = self.static_order()

        for transform_name in sorted_nodes:
            yield self._set_of_transforms[transform_name]
