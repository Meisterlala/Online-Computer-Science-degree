""" Parses/Compiles the keywords"""

# pylint: disable=unused-import
from .tokens import Token
from .JClasses.structure import Structure


class Parser():
    """ Parser of Keywords"""

    def __init__(self, tokens: "list[Token]") -> None:
        # Reverse List
        self.tokens = tokens[::-1]

    def parse(self):
        """ Main Parse Function, returns JClass """
        main_class = Structure.JClass(self.tokens)
        return main_class
