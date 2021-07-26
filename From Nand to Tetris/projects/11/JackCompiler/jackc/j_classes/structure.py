""" Containts all Jack Structures """


from .statement import Statements
from ..parents import XMLString, Compile
from ..tokens import Token  # pylint: disable=unused-import
from ..symbol_table import SymbolTable


class Structure():
    """ Namespace Class containing all Program Structure related classes"""

    class JClass(XMLString, Compile):
        """ 'class' ClassName '{ classVarDec* subroutineDec* '}' """
        xml_name = "class"

        def __init__(self, tokens: "list[Token]") -> None:
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

        def compile(self, table) -> "list[str]":
            compiled = []

            # ClassVarDec*
            for class_var_dec in self.class_var_decs:
                compiled.extend(class_var_dec.compile(table))

            # subroutineDec*
            for subroutine in self.subroutine_decs:
                compiled.extend(subroutine.compile(table))

            return compiled

    class JClassVarDec(XMLString, Compile):
        """ ('static'|'field') type varName (',' varName)* ';' """
        xml_name = "classVarDec"
        var_types = {"static", "field"}

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []
            self.var_names = []

            # ('static'|'field')
            token = tokens.pop()
            assert token.value in self.var_types
            self.content.append(token)
            self.kind = token.value

            # type
            j_type = Structure.JType(tokens)
            self.content.append(j_type)
            self.j_type = j_type.singe_content.value

            # varName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)
            self.var_names.append(token.value)

            # (, Varname)*
            token = tokens.pop()  # , or ;
            self.content.append(token)

            while token != ("symbol", ";"):
                token_name = tokens.pop()  # varName
                assert token_name == ("identifier", None)
                self.content.append(token)
                token = tokens.pop()  # , or ;
                self.content.append(token)
                self.var_names.append(token_name.value)

            # ;
            assert token.value == ";"

        def compile(self, table: "SymbolTable") -> "list[str]":
            compiled = []

            if self.kind == "static":
                kind = SymbolTable.Entry.Kind.STATIC
            else:  # Else it has to be "field"
                kind = SymbolTable.Entry.Kind.FIELD

            for name in self.var_names:
                table.add(name, self.j_type, kind)

            return compiled

    class JSubroutineDec(XMLString, Compile):
        """ ('constructor'|'function'|'method') ('void' | type)
            subroutineName '(' parameterList ')' subroutineBody """
        xml_name = "subroutineDec"
        sub_types = {"constructor", "function", "method"}

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []

            # ('constructor'|'function'|'method')
            token = tokens.pop()
            assert token.value in self.sub_types
            self.sub_type = token.value
            self.content.append(token)

            # ('void' | type)
            token = tokens.pop()
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

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []

            # reset Table
            table.reset_table_sub()

            # function Main.main 0
            # parameter_count = self.parameter_list.length
            argument_count = self.sub_body.locals()
            # inc argument length to account for first this
            if self.sub_type == "method":
                argument_count += 1

            # function header
            compiled.append(
                f"function {table.class_name}.{self.subroutine_name.value} {argument_count}")

            # add imaginary "this" and push it to pointer 0
            if self.sub_type == "method":
                table.add("this", table.class_name, SymbolTable.Entry.Kind.ARG)
                index_of_this = table.index_of("this")  # should be 0
                compiled.extend([f"push argument {index_of_this} // push this",
                                 "pop pointer 0 // assign this from arg"])

            # Handle arguments
            compiled.extend(self.parameter_list.compile(table))

            # Handle Object Memory Alloc
            if self.sub_type == "constructor":
                field_count = table.var_count(SymbolTable.Entry.Kind.FIELD)
                compiled.extend([f"push constant {field_count} // size of object",
                                 "call Memory.alloc 1 // allocate memory",
                                 "pop pointer 0 // store base adress in this"])

            # compile Body
            compiled.extend(self.sub_body.compile(table))

            return compiled

    class JParameterList(XMLString, Compile):
        """ ((type varName) (',' type varName)*)? """
        xml_name = "parameterList"

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []
            self.length = 0
            self.arguments: "list[tuple[str, str]]" = []

            # parameterList  ((type varName) (',' type varName)*)?
            if tokens[-1] != ("symbol", ")"):  # to match the last question mark
                # type
                j_type = Structure.JType(tokens)
                self.content.append(j_type)
                # varName
                token = tokens.pop()
                assert token == ("identifier", None)
                self.content.append(token)
                self.length += 1
                self.arguments.append(
                    (j_type.singe_content.value, token.value))

                while tokens[-1] == ("symbol", ","):  # (',' type varName)*
                    # ','
                    token_1 = tokens.pop()
                    self.content.append(token_1)

                    # type
                    j_type = Structure.JType(tokens)
                    self.content.append(j_type)

                    # varName
                    token = tokens.pop()
                    assert token == ("identifier", None)
                    self.content.append(token)

                    self.length += 1
                    self.arguments.append(
                        (j_type.singe_content.value, token.value))

        def compile(self, table: SymbolTable) -> "list[str]":

            for j_type, name in self.arguments:
                table.add(name, j_type, SymbolTable.Entry.Kind.ARG)

            # no code generated, only symbol table addition
            return []

    class JSubroutineBody(XMLString, Compile):
        """ '{' varDec* statements '}' """
        xml_name = "subroutineBody"

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []

            # {
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # varDec*
            next_token = tokens[-1]
            self.var_decs: "list[Structure.JVarDec]" = []
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

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []

            # varDec*
            for var_dec in self.var_decs:
                compiled.extend(var_dec.compile(table))

            # statements
            compiled.extend(self.statements.compile(table))

            return compiled

        def locals(self) -> int:
            """ Returns the amount of local variables in this Subroutine """
            count = 0
            for var_dec in self.var_decs:
                count += len(var_dec.var_names)

            return count

    class JVarDec(XMLString, Compile):
        """ 'var' type varName (',' varName)* ';' """
        xml_name = "varDec"

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []
            self.var_names = []

            # 'var'
            token = tokens.pop()
            assert token == ("keyword", "var")
            self.content.append(token)

            # type
            token = Structure.JType(tokens)
            self.content.append(token)
            self.j_type = token.singe_content.value

            # varName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)
            self.var_names.append(token.value)

            # (, Varname)*
            token = tokens.pop()  # , or ;
            self.content.append(token)

            while token != ("symbol", ";"):
                token = tokens.pop()  # varName
                assert token == ("identifier", None)
                self.content.append(token)
                self.var_names.append(token.value)

                token = tokens.pop()  # , or ;
                self.content.append(token)

            # ;
            assert token.value == ";"

        def compile(self, table: SymbolTable) -> "list[str]":
            # Adds to the Symbol Table
            for name in self.var_names:
                table.add(name, self.j_type, SymbolTable.Entry.Kind.LOCAL)

            # no output
            return []

    class JType(XMLString, Compile):
        """ 'int' | 'char' | 'boolean' | className """
        types = {"int", "char", "boolean"}

        def __init__(self, tokens: "list[Token]") -> None:
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
