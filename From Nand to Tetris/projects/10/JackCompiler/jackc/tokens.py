""" Contains all enums """

from enum import Enum


class TokenType(Enum):
    """ Type of Tokens """
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


class KeywordE(Enum):
    """ Type of Keyword """

    CLASS = 0
    METHOD = 1
    FUNCTION = 2
    CONSTRUCTOR = 3
    INT = 4
    BOOLEAN = 5
    CHAR = 6
    VOID = 7
    VAR = 8
    STATIC = 9
    FIELD = 10
    LET = 11
    DO = 12
    IF = 13
    ELSE = 14
    WHILE = 15
    RETURN = 16
    TRUE = 17
    FALSE = 18
    NULL = 19
    THIS = 20


class Token():
    """ Type of Tokens """
    name = "empty_token"

    def __init__(self) -> None:
        self.value = ""

    def __str__(self) -> str:
        return f"<{self.name}> {self.value} </{self.name}>"


class Tokens():
    """ All Tokens"""

    class Symbol(Token):
        """ a single symbol (){}[]... """
        name = "symbol"

        def __init__(self, symbol_name) -> None:
            super().__init__()
            self.value = symbol_name

    class Keyword(Token):
        """ a more complex word"""
        name = "keyword"

        def __init__(self, key) -> None:
            super().__init__()
            self.value = key

    class Identifier(Token):
        """ A sequence of letters, digits and underscore not starting with a digit"""
        name = "identifier"

        def __init__(self, name) -> None:
            super().__init__()
            self.value = name

    class IntConst(Token):
        """ a literal int """
        name = "intConst"

        def __init__(self, int_value: int) -> None:
            super().__init__()
            self.value = int(int_value)

    class StringConst(Token):
        """ a literal string """
        name = "stringConst"

        def __init__(self, string) -> None:
            super().__init__()
            self.value = string

    class Invalid(Token):
        """ base case Invalid """
