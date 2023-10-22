""" TODO: docstring """

from git_datasets.types import DecoratedClass
from git_datasets.config import DatasetRunConfig
from git_datasets.logging import get_logger

logger = get_logger(__name__)

def push(cls: DecoratedClass, config: DatasetRunConfig):
    """ Push data to remote. """

    logger.error("Push not implemented.")
    raise SystemExit
