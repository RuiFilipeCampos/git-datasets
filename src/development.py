""" This file is for testing during development. 

TODO: getting "Method 'delete_corrupted_files' should have "self" as first argumentPylintE0213:no-self-argument"
"""

from git_datasets import dataset
from git_datasets.actions import Insert

@dataset
class TestDataset:
    """ Basic information about books. """

    title: str
    author: str
    pages: int
    label: str

    def ingest_data() -> Insert:
        return [
            ("To Kill a Mockingbird", "Harper Lee", 281, "medium"),
            ("1984", "George Orwell", 328, "medium"),
            ("War and Peace", "Leo Tolstoy", 1225, "long"),
            ("Animal Farm", "George Orwell", 112, "medium"),
            ("The Catcher in the Rye", "J.D. Salinger", 277, "medium"),
            ("The Great Gatsby", "F. Scott Fitzgerald", 180, "medium"),
            ("Moby Dick", "Herman Melville", 635, "long"),

        ]

    def print_staff(title: str, pages: int) -> None:
        print(f"This book is titled {title} and has {pages} pages-")

    def check_book_length(pages: int, label: str) -> None:

        if pages < 100:
            assert label == "short" 
      
        elif 100 <= pages <= 500:
            assert label == "medium" 
    
        else:
            assert label == "long"


