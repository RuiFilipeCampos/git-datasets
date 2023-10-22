""" TODO """

import os.path
from git_datasets.logging import get_logger

logger = get_logger(__name__)

class ParquetFileHandler:
    """ TODO """

    def __init__(self, parquet_file: str):
        """ TODO """
        if not os.path.exists(parquet_file):
            logger.debug("Parquet file does not exist")

    def get_schema(self):
        """ TODO """
        return {}
