""" TODO """

import os.path
from git_datasets.logging import get_logger

logger = get_logger(__name__)


class ParquetFileHandler:
    """ TODO """

    def __init__(self, parquet_file: str):
        """ TODO """

        import pyarrow as pa
        self.python_to_arrow = {
            str: pa.string(),
            int: pa.int32(),
        }

        if not os.path.exists(parquet_file):
            logger.debug("Parquet file does not exist")

    def get_schema(self):
        """ TODO """
        return {}


