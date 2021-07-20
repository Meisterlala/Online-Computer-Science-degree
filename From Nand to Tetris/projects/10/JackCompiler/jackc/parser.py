""" Parses/Compiles the keywords"""


from jackc.tokens import Token


class Parser():
    """ Parser of Keywords"""

    def __init__(self, tokens: list[Token]) -> None:
        # Reverse List
        self.tokens = tokens[::-1]

    def parse(self):
        """ Main Parse Function, returns JClass """
        main_class = Structure.JClass(self.tokens)
        return main_class


class XMLString():
    """ Parent Class to print to XML """

    xml_name = "default"
    content = []

    def __str__(self) -> str:

        # If no Content return early
        if len(self.content) == 0:
            return f"<{self.xml_name}>\n</{self.xml_name}>"

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


class Structure():
    """ Namespace Class containing all Program Structure related classes"""

    class JClass(XMLString):
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

            # Symbol
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # ClassVarDec*
            next_token = tokens[-1]
            while (next_token == ("keyword", None) and
                   next_token.value in Structure.JClassVarDec.var_types):
                self.content.append(Structure.JClassVarDec(tokens))
                next_token = tokens[-1]

            # subroutineDec*
            next_token = tokens[-1]
            while (next_token == ("keyword", None) and
                   next_token.value in Structure.JSubroutineDec.sub_types):
                self.content.append(Structure.JSubroutineDec(tokens))
                next_token = tokens[-1]

            # Symbol
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

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

    class JSubroutineDec(XMLString):
        """ ('constructor'|'function'|'method') ('void' | type)
            subroutineName '(' parameterList ')' subroutineBody """
        xml_name = "subroutineDec"
        sub_types = {"constructor", "function", "method"}

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # ('constructor'|'function'|'method')
            token = tokens.pop()
            assert token.value in self.sub_types
            self.content.append(token)

            # ('void' | type)
            token = tokens.pop()
            if token != ("keyword", "void"):
                assert token == ("identifier", None)
            self.content.append(token)

            # subroutineName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)

            # (
            token = tokens.pop()
            assert token == ("symbol", "(")
            self.content.append(token)

            # paremeterList
            self.content.append(Structure.JParameterList(tokens))

            # )
            token = tokens.pop()
            assert token == ("symbol", ")")
            self.content.append(token)

            # Subroutine Body
            self.content.append(Structure.JSubroutineBody(tokens))

    class JParameterList(XMLString):
        """ ((type varName) (',' type varName)*)? """
        xml_name = "parameterList"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # parameterList  ((type varName) (',' type varName)*)?
            if tokens[-1] != ("symbol", ")"):  # to match the last question mark
                self.content.append(Structure.JType(tokens))  # type
                token = tokens.pop()  # varName
                assert token == ("identifier", None)
                self.content.append(token)

                while tokens[-1] == ("symbol", ","):  # (',' type varName)*
                    token = tokens.pop()
                    self.content.append(token)  # ','
                    self.content.append(Structure.JType(tokens))  # type
                    token = tokens.pop()  # varName
                    assert token == ("identifier", None)
                    self.content.append(token)

    class JSubroutineBody(XMLString):
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
            while next_token == ("keyword", "var"):
                self.content.append(Structure.JVarDec(tokens))
                next_token = tokens[-1]

            # statements
            self.content.append(Statements.JStatements(tokens))

            # }
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

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


class Statements:
    """ Namespace class containg every class dealing with Statements"""

    class JStatements(XMLString):
        """ (letStatement | ifStatement| whileStatement | doStatement | returnStatement)* """
        xml_name = "statements"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # get Next Token without pop
            next_token = tokens[-1]
            # get type of statement from dic (or NONE)
            statement_type = Statements.STATEMENT_TYPES.get(
                next_token.value, None)

            while (next_token.name == "keyword" and
                   statement_type is not None):
                # Construct Statement
                self.content.append(statement_type(tokens))

                # do the same as before the while loop
                next_token = tokens[-1]
                statement_type = Statements.STATEMENT_TYPES.get(
                    next_token.value, None)

    class JLetStatement(XMLString):
        """ 'let' varName ('[' expression ']')? '=' expression ';' """
        xml_name = "letStatement"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'let'
            token = tokens.pop()
            assert token == ("keyword", "let")
            self.content.append(token)

            # varName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)

            # ('[' expression ']')?
            next_token = tokens[-1]
            while next_token == ("symbol", "["):
                # [
                self.content.append(tokens.pop())  # [

                # expression
                self.content.append(Expressions.JExpression(tokens))

                # ]
                token = tokens.pop()
                assert token == ("symbol", "]")
                self.content.append(token)
                next_token = tokens[-1]

            # '='
            token = tokens.pop()
            assert token == ("symbol", "=")
            self.content.append(token)

            # expression
            self.content.append(Expressions.JExpression(tokens))

            # ';'
            token = tokens.pop()
            assert token == ("symbol", ";")
            self.content.append(token)

    class JIfStatement(XMLString):
        """ 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')? """
        xml_name = "ifStatement"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'if'
            token = tokens.pop()
            assert token == ("keyword", "if")
            self.content.append(token)

            # '('
            token = tokens.pop()
            assert token == ("symbol", "(")
            self.content.append(token)

            # expression
            self.content.append(Expressions.JExpression(tokens))

            # ')'
            token = tokens.pop()
            assert token == ("symbol", ")")
            self.content.append(token)

            # '{'
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # statements
            self.content.append(Statements.JStatements(tokens))

            # '}'
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

            # ('else' '{' statements '}')?
            next_token = tokens[-1]
            if next_token == ("keyword", "else"):
                self.content.append(tokens.pop())

                # '{'
                token = tokens.pop()
                assert token == ("symbol", "{")
                self.content.append(token)

                # statements
                self.content.append(Statements.JStatements(tokens))

                # '}'
                token = tokens.pop()
                assert token == ("symbol", "}")
                self.content.append(token)

    class JWhileStatement(XMLString):
        """ 'while' '(' expression ')' '{' statements '}' """
        xml_name = "whileStatement"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'while'
            token = tokens.pop()
            assert token == ("keyword", "while")
            self.content.append(token)

            # '('
            token = tokens.pop()
            assert token == ("symbol", "(")
            self.content.append(token)

            # expression
            self.content.append(Expressions.JExpression(tokens))

            # ')'
            token = tokens.pop()
            assert token == ("symbol", ")")
            self.content.append(token)

            # '{'
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # statements
            self.content.append(Statements.JStatements(tokens))

            # '}'
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

    class JDoStatement(XMLString):
        """ 'do' subroutineCall ';' """
        xml_name = "doStatement"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'do'
            token = tokens.pop()
            assert token == ("keyword", "do")
            self.content.append(token)

            # subroutineCall
            self.content.append(Expressions.JSubroutineCall(tokens))

            # ';'
            token = tokens.pop()
            assert token == ("symbol", ";")
            self.content.append(token)

    class JReturnStatement(XMLString):
        """ 'return' expression? ';' """
        xml_name = "returnStatement"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'return'
            token = tokens.pop()
            assert token == ("keyword", "return")
            self.content.append(token)

            # expression?
            next_token = tokens[-1]
            if next_token != ("symbol", ";"):
                self.content.append(Expressions.JExpression(tokens))

            # ';'
            token = tokens.pop()
            assert token == ("symbol", ";")
            self.content.append(token)

    STATEMENT_TYPES = {"let": JLetStatement, "if": JIfStatement,
                       "while": JWhileStatement, "do": JDoStatement, "return": JReturnStatement}


class Expressions:
    """ Namespace class containg every class dealing with Statements"""

    KEYWORD_CONSTANTS = {"true", "false", "null", "this"}
    OPS = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
    UNARY_OPS = {"-", "~"}

    class JExpression(XMLString):
        """ term (op term)* """
        xml_name = "expression"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # term
            self.content.append(Expressions.JTerm(tokens))

            # (op term)*
            next_token = tokens[-1]
            while (next_token.name == "symbol" and
                   next_token.value in Expressions.OPS):
                # op
                self.content.append(tokens.pop())

                # term
                self.content.append(Expressions.JTerm(tokens))
                next_token = tokens[-1]

    class JTerm(XMLString):
        """ integerConstant | stringConstant | keywordConstant | varName |
            varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOP term """
        xml_name = "term"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            token = tokens.pop()

            # IntergerConstant
            if token == ("integerConstant", None):
                self.content.append(token)
                return

            # StringConstant
            if token == ("stringConstant", None):
                self.content.append(token)
                return

            # KeywordConstant
            if (token.name == "keyword" and
                    token.value in Expressions.KEYWORD_CONSTANTS):
                self.content.append(token)
                return

            #  '(' expression ')'
            if token == ("symbol", "("):
                # '('
                self.content.append(token)

                # expression
                self.content.append(Expressions.JExpression(tokens))

                # ')'
                token = tokens.pop()
                assert token == ("symbol", ")")
                self.content.append(token)
                return

            # unaryOP term
            if (token.name == "symbol" and
                    token.value in Expressions.UNARY_OPS):
                self.content.append(token)

                # term
                self.content.append(Expressions.JTerm(tokens))
                return

            # subroutineCall
            next_token = tokens[-1]
            if (next_token == ("symbol", "(") or
                    next_token == ("symbol", ".")):
                assert token == ("identifier", None)
                tokens.append(token)
                self.content.append(Expressions.JSubroutineCall(tokens))
                return

            # varName  ('[' expression ']')
            if token == ("identifier", None):
                self.content.append(token)
                if next_token == ("symbol", "["):
                    # '['
                    self.content.append(tokens.pop())

                    # expression
                    self.content.append(Expressions.JExpression(tokens))

                    # ']'
                    token = tokens.pop()
                    assert token == ("symbol", "]")
                    self.content.append(token)
                return

    class JExpressionList(XMLString):
        """ (expression (',' expression)*)?
            Expects every empty expression list to be followed by a ')'
        """

        xml_name = "expressionList"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # Expects every empty expression list to be followed by a ')'
            possible_bracket = tokens[-1]
            if possible_bracket == ("symbol", ")"):
                return

            # expression
            self.content.append(Expressions.JExpression(tokens))

            # (',' expression)*
            next_token = tokens[-1]
            while next_token == ("symbol", ","):
                # ','
                self.content.append(tokens.pop())

                # expression
                self.content.append(Expressions.JExpression(tokens))
                next_token = tokens[-1]

    class JSubroutineCall(XMLString):
        """ subroutineName '(' expressionList ')' |
            (className | varName) '.' subroutineName '(' expressionList ')' """
        xml_name = "subroutineCall"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            possible_dot = tokens[-2]
            if possible_dot != ("symbol", "."):
                # subroutineName
                token = tokens.pop()
                assert token == ("identifier", None)
                self.content.append(token)

                # '('
                token = tokens.pop()
                assert token == ("symbol", "(")
                self.content.append(token)

                # expressionList
                self.content.append(Expressions.JExpressionList(tokens))

                # ')'
                token = tokens.pop()
                assert token == ("symbol", ")")
                self.content.append(token)
            else:
                # (className | varName)
                token = tokens.pop()
                assert token == ("identifier", None)
                self.content.append(token)

                # '.'
                token = tokens.pop()
                assert token == ("symbol", ".")
                self.content.append(token)

                # subroutineName
                token = tokens.pop()
                assert token == ("identifier", None)
                self.content.append(token)

                # '('
                token = tokens.pop()
                assert token == ("symbol", "(")
                self.content.append(token)

                # expressionList
                self.content.append(Expressions.JExpressionList(tokens))

                # ')'
                token = tokens.pop()
                assert token == ("symbol", ")")
                self.content.append(token)

        def __str__(self) -> str:
            """ Dont Display self Name"""
            return "\n".join(str(x) for x in self.content)
