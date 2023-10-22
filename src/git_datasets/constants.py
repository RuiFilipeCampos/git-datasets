""" constants.py - Central repository for constants used throughout the application """

import pyarrow as pa

PYTHON_TO_PARQUET = {
    str: pa.string(),
    int: pa.int32(),
}

