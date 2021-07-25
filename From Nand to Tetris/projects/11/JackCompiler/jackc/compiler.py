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
        # Create Symbol Tabels
        symbol_table = SymbolTable(self.class_name)
        # Compile Code
        code = self.j_class.compile(symbol_table)
        # Optize Code
        code = Compiler.remove_duplicates(code)
        # Indent to make easy to read
        code = Compiler.indent(code)
        # Add Sys.init 0 Bootstrap
        #code = self.sys_init(code)
        return "\n".join(code)

    def sys_init(self, source: list[str]) -> list[str]:
        """ Bootstrap Code """

        bootstrap = ["// Bootstrap Code",
                     "function Sys.init 0",
                     "call Main.main 0",
                     "label SYSINIT_LOOP",
                     "goto SYSINIT_LOOP",
                     ""]
        bootstrap.extend(source)

        return bootstrap

    @staticmethod
    def indent(source: list[str]) -> list[str]:
        """ Indents Jack Commands for easier reading """
        indented = []
        for line in source:
            # dont indent functions
            if line.startswith("function"):
                indented.append("\n" + line)
                continue

            # Dont indent return
            if line.startswith("return"):
                indented.append(line)
                continue

            # Dont indent labels
            if line.startswith("label"):
                indented.append(line)
                continue
            # indent
            indented.append("\t" + line)
        return indented

    @staticmethod
    def remove_duplicates(source: list[str]) -> list[str]:
        """ Removes duplicates commands for performance"""
        clean = []
        last_line = ""
        for line in source:
            # remove whitespace
            trimmed = line.strip()
            if trimmed == last_line:
                if trimmed in ("not", "neg"):
                    clean.pop()
                    continue
            clean.append(line)
            last_line = trimmed

        return clean
