""" This file is for testing during development. 

TODO: getting "Method 'delete_corrupted_files' should have "self" as first argumentPylintE0213:no-self-argument"
"""

from typing import Literal

from git_datasets import dataset, Action
from git_datasets.files import File, png, jpg

@dataset
class SegmentationDataset:
    """ TODO """

    image: File[jpg]
    segmentation: File[png]
    label: Literal["cat", "dog", "person"]


    def delete_corrupted_files(image: File[jpg]) -> Action.Delete:
        """ TODO """

        # perform some checks, get image_is_corrupted: bool

        return True

    def encoded_label(label: Literal["cat", "dog", "person"]) -> Literal[0, 1, 2]:
        """ TODO """

        if label == "cat":
            return 0
        elif label == "dog":
            return 1
        elif label == "person":
            return 2
        else:
            raise ValueError("Not a cat, dog or person !!")
