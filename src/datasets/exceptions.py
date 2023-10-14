



class InvalidInputType(TypeError):
    """ Raised when invalid input type. """

    def __init__(self, name: str, expected_type, value) -> None:
        self.name = name
        self.expected_type = expected_type
        self.value = value
        super().__init__(self)

    def __str__(self) -> str:
        return (
            f"Argument {self.name} should be of type {self.expected_type}, "
            f"but got {type(self.value)} instead."
        )
