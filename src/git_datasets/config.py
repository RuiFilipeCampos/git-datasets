from dataclasses import dataclass
from typing import Literal
import os
import sys

from git_datasets.git_operations import get_git_root_path


@dataclass
class DatasetRunConfig:
    main_script_path: str = os.path.abspath(sys.argv[0])
    repository_root: str = get_git_root_path()
    hidden_dir: str = os.path.join(repository_root, ".gitdatasets")


