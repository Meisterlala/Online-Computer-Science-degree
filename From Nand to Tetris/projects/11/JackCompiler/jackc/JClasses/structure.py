""" Containts all Jack Structures """

from jackc.parents import XMLString, Compile
from jackc.tokens import Token
from jackc.JClasses.statement import Statements
from jackc.symbol_table import SymbolTable


class Structure():
    """ Namespace Class containing all Program Structure related classes"""

    class JClass(XMLString, Compile):
        """ 'class' ClassName '{ classVarDec* subroutineDec* '}' """
        xml_name = "class"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # Class
            token = tokens.pop()
            assert token == ("keyword", "class")
            self.content.append(token)

            # Class Name Identifier
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)
            self.identifier = token

            # Symbol
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # ClassVarDec*
            self.class_var_decs = []
            next_token = tokens[-1]
            while (next_token == ("keyword", None) and
                   next_token.value in Structure.JClassVarDec.var_types):
                j_class = Structure.JClassVarDec(tokens)
                self.content.append(j_class)
                self.class_var_decs.append(j_class)
                next_token = tokens[-1]

            # subroutineDec*
            self.subroutine_decs = []
            next_token = tokens[-1]
            while (next_token == ("keyword", None) and
                   next_token.value in Structure.JSubroutineDec.sub_types):
                j_sub = Structure.JSubroutineDec(tokens)
                self.content.append(j_sub)
                self.subroutine_decs.append(j_sub)
                next_token = tokens[-1]

            # Symbol
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []

            # subroutineDec*
            for subroutine in self.subroutine_decs:
                compiled.extend(subroutine.compile(table))

            return compiled

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
            self.content.append(Structure.JType(tokens))

            # varName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)

            # (, Varname)*
            token = tokens.pop()  # , or ;
            self.content.append(token)

            while token != ("symbol", ";"):
                token = tokens.pop()  # varName
                assert token == ("identifier", None)
                self.content.append(token)
                token = tokens.pop()  # , or ;
                self.content.append(token)

            # ;
            assert token.value == ";"

    class JSubroutineDec(XMLString, Compile):
        """ ('constructor'|'function'|'method') ('void' | type)
            subroutineName '(' parameterList ')' subroutineBody """
        xml_name = "subroutineDec"
        sub_types = {"constructor", "function", "method"}

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # ('constructor'|'function'|'method')
            token = tokens.pop()
            assert token.value in self.sub_types
            self.sub_type = token
            self.content.append(token)

            # ('void' | type)
            token = tokens.pop()
            if token != ("keyword", "void"):
                assert token == ("identifier", None)
            self.content.append(token)
            self.return_type = token

            # subroutineName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.subroutine_name = token
            self.content.append(token)

            # (
            token = tokens.pop()
            assert token == ("symbol", "(")
            self.content.append(token)

            # paremeterList
            params = Structure.JParameterList(tokens)
            self.content.append(params)
            self.parameter_list = params

            # )
            token = tokens.pop()
            assert token == ("symbol", ")")
            self.content.append(token)

            # Subroutine Body
            body = Structure.JSubroutineBody(tokens)
            self.content.append(body)
            self.sub_body = body

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []

            # function Main.main 0
            parameter_count = self.parameter_list.length
            compiled.append(
                f"function {table.class_name}.{self.subroutine_name.value} {parameter_count}")

            # compile
            compiled.extend(self.sub_body.compile(table))

            return compiled

    class JParameterList(XMLString):
        """ ((type varName) (',' type varName)*)? """
        xml_name = "parameterList"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []
            self.length = 0

            # parameterList  ((type varName) (',' type varName)*)?
            if tokens[-1] != ("symbol", ")"):  # to match the last question mark
                self.content.append(Structure.JType(tokens))  # type
                token = tokens.pop()  # varName
                assert token == ("identifier", None)
                self.content.append(token)
                self.length += 1

                while tokens[-1] == ("symbol", ","):  # (',' type varName)*
                    token = tokens.pop()
                    self.content.append(token)  # ','
                    self.content.append(Structure.JType(tokens))  # type
                    token = tokens.pop()  # varName
                    assert token == ("identifier", None)
                    self.content.append(token)
                    self.length += 1

    class JSubroutineBody(XMLString, Compile):
        """ '{' varDec* statements '}' """
        xml_name = "subroutineBody"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # {
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # varDec*
            next_token = tokens[-1]
            self.var_decs = []
            while next_token == ("keyword", "var"):
                var_dec = Structure.JVarDec(tokens)
                self.var_decs.append(var_dec)
                self.content.append(var_dec)
                next_token = tokens[-1]

            # statements
            statements = Statements.JStatements(tokens)
            self.content.append(statements)
            self.statements = statements

            # }
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []

            # varDec*

            # statements
            compiled.extend(self.statements.compile(table))

            return compiled

    class JVarDec(XMLString):
        """ 'var' type varName (',' varName)* ';' """
        xml_name = "varDec"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'var'
            token = tokens.pop()
            assert token == ("keyword", "var")
            self.content.append(token)

            # type
            self.content.append(Structure.JType(tokens))

            # varName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)

            # (, Varname)*
            token = tokens.pop()  # , or ;
            self.content.append(token)

            while token != ("symbol", ";"):
                token = tokens.pop()  # varName
                assert token == ("identifier", None)
                self.content.append(token)
                token = tokens.pop()  # , or ;
                self.content.append(token)

            # ;
            assert token.value == ";"

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
