

class Token:
    """
    Token class, representing single token from expression
    """

    def __init__(self, value: str, is_operator: bool = False) -> None:
        self.value = value
        self.is_operator = is_operator

    def __repr__(self):
        return self.value
