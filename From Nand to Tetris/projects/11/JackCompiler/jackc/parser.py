""" Parses/Compiles the keywords"""


from jackc.tokens import Token
from jackc.JClasses.structure import Structure


class Parser():
    """ Parser of Keywords"""

    def __init__(self, tokens: list[Token]) -> None:
        # Reverse List
        self.tokens = tokens[::-1]

    def parse(self):
        """ Main Parse Function, returns JClass """
        main_class = Structure.JClass(self.tokens)
        return main_class
