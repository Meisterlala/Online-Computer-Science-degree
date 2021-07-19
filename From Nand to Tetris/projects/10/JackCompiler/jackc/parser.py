""" Parses/Compiles the keywords"""


from os import name
from jackc.tokens import Token


class Parser():
    """ Parser of Keywords"""

    def __init__(self, tokens: list[Token]) -> None:
        # Reverse List
        self.tokens = tokens[::-1]

    def parse(self):
        """ Main Parse Function, returns JClass """
        main_class = JClass(self.tokens)
        return main_class


class XMLString():
    """ Parent Class to print to XML """

    xml_name = "default"
    content = []

    def __str__(self) -> str:

        # If no Content return early
        if len(self.content) == 0:
            return f"<{self.xml_name}> #### EMPTY #### </{self.xml_name}>"

        # If it has Content
        return_value = f"<{self.xml_name}>\n"
        for token in self.content:
            return_value += XMLString.indent_ever_line(str(token)) + "\n"
        return_value += f"</{self.xml_name}>"

        return return_value

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def indent_ever_line(to_indent: str) -> str:
        """ adds a tab bevor every line """
        split = to_indent.splitlines(keepends=True)
        out = ""
        for line in split:
            out += f"\t{line}"

        return out


class JClass(XMLString):
    """ 'class' ClassName '{ classVarDec* subroutineDec* '}' """
    xml_name = "class"

    def __init__(self, tokens: list[Token]) -> None:
        self.content = []

        # Class
        token = tokens.pop()
        assert token.value == "class"
        self.content.append(token)

        # Class Name Identifier
        token = tokens.pop()
        assert token.name == "identifier"
        self.content.append(token)

        # Symbol
        token = tokens.pop()
        assert token.value == "{"
        self.content.append(token)

        # ClassVarDec*
        next_token = tokens[-1]
        while next_token.name == "keyword" and next_token.value in JClassVarDec.var_types:
            self.content.append(JClassVarDec(tokens))
            next_token = tokens[-1]


class JClassVarDec(XMLString):
    """ ('static'|'field') type varName (',' varName)* ';' """
    xml_name = "classVarDec"
    var_types = {"static", "field"}

    def __init__(self, tokens: list[Token]) -> None:
        self.content = []

        # ('static'|'field')
        token = tokens.pop()
        assert token.value in self.var_types
        self.content.append(token)

        # type
        self.content.append(JType(tokens))

        # TODO continue here

        pass

    pass


class JType(XMLString):
    """ 'int' | 'char' | 'boolean' | className """
    types = {"int", "char", "boolean"}

    def __init__(self, tokens: list[Token]) -> None:
        token = tokens.pop()

        # 'int' | 'char' | 'boolean'
        if token.name == "keyword":
            assert token.value in self.types
        # className
        else:
            assert token.name == "identifier"

        self.singe_content = token

    def __str__(self) -> str:
        return str(self.singe_content)
