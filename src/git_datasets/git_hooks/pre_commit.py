"""
This module provides functionality to shape the datasets prior to committing their index.py file.

This code is executed when:

```
python index.py --pre-commit
```

is executed. Which itself is called as a git hook by `git commit index.py`. 
"""

from git_datasets.types import DecoratedClass
from git_datasets.config import DatasetRunConfig
from git_datasets.logging import get_logger
from git_datasets.exceptions import RepeatedAttributeError


logger = get_logger(__name__)

def pre_commit(cls: DecoratedClass, config: DatasetRunConfig) -> None:
    """ Pre commit dataset. """

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

    logger.debug("Desired schema: %s", desired_schema)

    # pylint: disable=import-outside-toplevel
    # reason: delaying imports until needed
    from git_datasets.parquet import ParquetFileHandler

    with ParquetFileHandler.open(config) as parquet_file:
        parquet_file.set_schema(desired_schema)

    logger.error("Pre-commit not implemented.")
    raise SystemExit




