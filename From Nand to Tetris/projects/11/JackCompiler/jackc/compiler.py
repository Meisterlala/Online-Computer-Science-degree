""" Compiles a JClass to Jack VM code """


from jackc.parser import Structure
from jackc.symbol_table import SymbolTable


class Compiler():
    """ Compiles a JClass to Jack VM code """

    def __init__(self, j_class: Structure.JClass) -> None:
        self.j_class = j_class

        # Identifyer Token of Class
        self.class_name = j_class.content[1].value

        self.content = []

    def compile(self) -> str:
        """ Compile everything """
        symbol_table = SymbolTable(self.class_name)
        compiled = self.j_class.compile(symbol_table)
        return "\n".join(compiled)
        