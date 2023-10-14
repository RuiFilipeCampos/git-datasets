"""
Prototype for the datasets project.
"""

import sqlite3
from contextlib import closing
import logging

from .types import DecoratedClass, Decorator
from .pre_commit import pre_commit
from .pull import pull
from .push import push
from .checkout import checkout


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("datasets")

def dataset(*, remote: str) -> Decorator:
    """
    A decorator to manage the lifecycle of the SQLite connection 
    and initialize a dataset with the provided schema.
    """

    sql_file = "./dataset.sql"
    data_dir = "./dataset"

    def decorator(cls: DecoratedClass) -> DecoratedClass:
        with closing(sqlite3.connect(sql_file)) as conn:
            cursor = conn.cursor()

            if __name__ == "__main__":
                arg = "commit"

                if arg == "commit":
                    pre_commit(cls, cursor, data_dir, remote)
                elif arg == "pull":
                    pull(cls, cursor, data_dir, remote)
                elif arg == "push":
                    push(cls, cursor, data_dir, remote)
                elif arg == "checkout":
                    checkout(cls, cursor, data_dir, remote)
            return cls
    return decorator
