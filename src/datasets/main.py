"""
Prototype for the datasets project.
"""

import sqlite3
from sqlite3 import Cursor
from contextlib import closing
import logging
from functools import wraps
from typing import Callable, get_type_hints

from .types import SQLTypeStrLit, DecoratedClass, PathStr, Decorator
from .pre_commit import pre_commit
from .pull import pull
from .push import push
from .checkout import checkout
from .exceptions import InvalidInputType

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("datasets")


def validate_arguments(func: Callable) -> Callable:
    """ Runtime validation of function arguments. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        for name, value in kwargs.items():
            expected_type = hints.get(name)

            if expected_type is None:
                continue

            if not isinstance(value, expected_type):
                raise InvalidInputType(name, expected_type, value)

        return func(*args, **kwargs)
    return wrapper


PYTHON_TO_SQLITE3: dict[type, SQLTypeStrLit] = {
    str: "TEXT",
    int: "INTEGER",
    float: "REAL",
    bytes: "BLOB",
    bool: "INTEGER",
    None: "NULL"
}




def dataset(
    sql_file: PathStr = "./dataset.sqlite",
    data_dir: PathStr = "./dataset",
) -> Decorator:
    """
    A decorator to manage the lifecycle of the SQLite connection 
    and initialize a dataset with the provided schema.
    """

    def decorator(cls: DecoratedClass) -> DecoratedClass:
        with closing(sqlite3.connect(sql_file)) as conn:
            cursor = conn.cursor()

            if __name__ == "__main__":
                arg = "commit"

                if arg == "commit":
                    pre_commit(cls, cursor, data_dir)
                elif arg == "pull":
                    pull(cls, cursor, data_dir)
                elif arg == "push":
                    push(cls, cursor, data_dir)
                elif arg == "checkout":
                    checkout(cls, cursor, data_dir)

            return cls

    return decorator
