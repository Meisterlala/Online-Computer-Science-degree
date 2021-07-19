""" Contains every Token except Keyword """


class Token():
    """ Type of Tokens """
    name = "empty_token"

    def __init__(self) -> None:
        self.value = ""

    def __str__(self) -> str:
        return f"<{self.name}> {self.value} </{self.name}>"

    def __repr__(self) -> str:
        return f"({self.name}: {self.value} )"


class Invalid(Token):
    """ base case Invalid """


class Tokens():
    """ Namespace only class """

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
        name = "integerConstant"

        def __init__(self, int_value: int) -> None:
            super().__init__()
            self.value = int(int_value)

    class StringConst(Token):
        """ a literal string """
        name = "stringConstant"

        def __init__(self, string) -> None:
            super().__init__()
            self.value = string
