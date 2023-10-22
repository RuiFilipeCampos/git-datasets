""" TODO """
from typing import TypeVar, Generic


class MimeType:
    """ TODO """
    def __init__(self, mime_type: str):
        """ TODO """
        self.mime_type = mime_type
    
    def __repr__(self):
        """ TODO """
        return f"<mimetype '{self.mime_type}'>"

png = MimeType("image/png")
jpg = MimeType("image/png")

T = TypeVar('T')

class File(Generic[T]):
    """ TODO """
    mime_type: T
