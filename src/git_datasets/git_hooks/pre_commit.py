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


logger = get_logger(__name__)

def pre_commit(cls: DecoratedClass, config: DatasetRunConfig) -> None:
    """ Pre commit dataset. """

    # avoiding unnecessary imports until needed (this is a cli command)
    from typing import get_type_hints
    from git_datasets.parquet import ParquetFileHandler
    from git_datasets.types import Action

    parquet_handler = ParquetFileHandler(config.parquet_file)
    current_schema = parquet_handler.get_schema()
    desired_schema = cls.__annotations__

    for attribute_name in dir(cls):

        if attribute_name.startswith("__"):
            continue

        attribute = getattr(cls, attribute_name)

        if not callable(attribute):
            continue
        
        return_type = get_type_hints(attribute).get('return')

        if return_type in [Action.Insert, Action.Alter, Action.Delete]:
            continue

        if attribute_name in desired_schema:
            raise ValueError

        desired_schema[attribute_name] = return_type

    logger.debug("Current schema: %s", current_schema)
    logger.debug("Desired schema: %s", desired_schema)


    logger.error("Pre-commit not implemented.")
    raise SystemExit
