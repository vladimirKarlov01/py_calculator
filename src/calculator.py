from typing import Callable, Dict, List, Optional, Tuple

from .token import Token


class CalculationError(Exception):
    def __init__(self, error: str):
        self.error = error

    def __str__(self):
        return f"Failed to calculate expression due to error: {self.error}"


class Calculator:
    """
    Main calculator class for performing arithmetic operations
    """

    def __init__(self) -> None:
        self.operators: Dict[str, Tuple[int, Callable]] = {
            "+": (1, lambda x, y: x + y),
            "-": (1, lambda x, y: x - y),
            "*": (2, lambda x, y: x * y),
            "/": (2, lambda x, y: x / y if y != 0 else self.div_zero_err()),
            "~": (3, lambda x: -x),
        }

    def div_zero_err(self) -> None:
        """
        Raises a division by zero error.
        """
        raise CalculationError("Zero division is not allowed!")

    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenization function (splitting input sequence into tokens)
        """
        tokens: List[Token] = []
        number: str = ""
        prev_char: Optional[str] = None
        for char in expression:
            if char.isdigit() or char == ".":
                number += char
            else:
                if number:
                    tokens.append(Token(number))
                    number = ""
                if char == "-" and (
                    prev_char is None or prev_char in self.operators or prev_char == "("
                ):
                    tokens.append(Token("~", is_operator=True))
                elif char in self.operators or char in "()":
                    tokens.append(Token(char, is_operator=True))
                prev_char = char
        if number:
            tokens.append(Token(number))
        return tokens

    def to_reverse_polish_notation(self, tokens: List[Token]) -> List[Token]:
        """
        Convert tokens into reverse polish notation
        """
        output: List[Token] = []
        stack: List[Token] = []
        for token in tokens:
            if token.is_operator:
                if token.value == "(":
                    stack.append(token)
                elif token.value == ")":
                    while stack and stack[-1].value != "(":
                        output.append(stack.pop())
                    stack.pop()
                else:
                    while (
                        stack
                        and stack[-1].is_operator
                        and stack[-1].value not in "()"
                        and self.operators[stack[-1].value][0]
                        >= self.operators[token.value][0]
                    ):
                        output.append(stack.pop())
                    stack.append(token)
            else:
                output.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def evaluate(self, expression: str) -> float:
        tokens = self.tokenize(expression)
        rpn = self.to_reverse_polish_notation(tokens)
        stack: List[Token] = []
        for token in rpn:
            if token.is_operator:
                if token.value == "~":
                    x = stack.pop()
                    result = self.operators[token.value][1](float(x.value))
                else:
                    y, x = stack.pop(), stack.pop()
                    result = self.operators[token.value][1](
                        float(x.value), float(y.value)
                    )
                stack.append(Token(str(result)))
            else:
                stack.append(token)
        return float(stack[0].value) if stack else 0
