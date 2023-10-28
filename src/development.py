""" This file is for testing during development. 

TODO: getting "Method 'delete_corrupted_files' should have "self" as first argumentPylintE0213:no-self-argument"
"""


from git_datasets import dataset


@dataset
class TestDataset:
    """ TODO """

    label: int
    age: int
