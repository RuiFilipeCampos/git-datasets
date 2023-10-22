""" constants.py - Central repository for constants used throughout the application """

from git_datasets.types import SQLTypeStrLit

PYTHON_TO_SQLITE3: dict[type, SQLTypeStrLit] = {
    str: "TEXT",
    int: "INTEGER",
    float: "REAL",
    bytes: "BLOB",
    bool: "INTEGER",
    None: "NULL"
}