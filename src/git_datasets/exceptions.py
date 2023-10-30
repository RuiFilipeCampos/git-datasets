"""
Defines custom exceptions.
"""

from typing import Any


class InvalidInputType(TypeError):
    """ Raised when invalid input type. """

    name: str
    expected_type: type
    actual_type: type

    def __init__(self, name: str, expected_type: type, value: Any) -> None:
        self.name = name
        self.expected_type = expected_type
        self.actual_type = type(value)
        super().__init__(self)

    def __str__(self) -> str:
        return (
            f"Argument {self.name} should be of type {self.expected_type}, "
            f"but got {self.actual_type} instead."
        )

class RepeatedAttributeError(TypeError):
    """ TODO """

    attribute_name: str

    def __init__(self, attribute_name: str) -> None:
        """ TODO """
        self.attribute_name = attribute_name
        super().__init__(self)

    def __str__(self) -> str:
        """ TODO """
        return f"Repeated name '{self.attribute_name}' in decorated class."
