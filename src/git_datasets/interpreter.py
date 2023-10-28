""" TODO """

from git_datasets.exceptions import RepeatedAttributeError
from git_datasets.types import DecoratedClass

def cls_to_schema(cls: DecoratedClass):
    """ TODO """
    # pylint: disable=import-outside-toplevel
    # reason: delaying imports until needed
    from typing import get_type_hints
    from git_datasets.types import Action

    desired_schema = cls.__annotations__

    # finish constructing `desired_schema` by collecting
    # transformations of the form `def field(some_field: Foo) -> Bar`
    # where `Bar` is not an action.


    for attribute_name in dir(cls):

        # prohibit repeated naming
        if attribute_name in desired_schema:
            raise RepeatedAttributeError

        # exclude dunder methods and attributes
        if attribute_name.startswith("__"):
            continue

        # exclude private methods and attributes
        if attribute_name.startswith("_"):
            continue

        # exclude attributes
        attribute = getattr(cls, attribute_name)
        if not callable(attribute):
            continue

        # exclude actions (insert, alter, delete, etc)
        return_type = get_type_hints(attribute).get('return')
        if return_type in [Action.Insert, Action.Alter, Action.Delete, None]:
            continue

        # collect new field
        desired_schema[attribute_name] = return_type
    return desired_schema


def get_dataset_name(cls: DecoratedClass) -> str:
    """ TODO """

    return cls.__name__.lower()