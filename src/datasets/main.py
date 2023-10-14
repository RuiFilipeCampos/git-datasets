"""
Prototype for the datasets project.
"""

import sqlite3
from contextlib import closing
import logging

from .types import DecoratedClass, PathStr, Decorator
from .pre_commit import pre_commit
from .pull import pull
from .push import push
from .checkout import checkout


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("datasets")



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
