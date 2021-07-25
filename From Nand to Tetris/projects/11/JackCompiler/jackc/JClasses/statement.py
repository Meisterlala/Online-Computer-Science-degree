""" Containts all Jack Statements """

from os import chdir
from jackc.parents import XMLString, Compile
from jackc.tokens import Token
from jackc.JClasses.expression import Expressions
from jackc.symbol_table import SymbolTable


class Statements:
    """ Namespace class containg every class dealing with Statements"""

    class JStatements(XMLString, Compile):
        """ (letStatement | ifStatement| whileStatement | doStatement | returnStatement)* """
        xml_name = "statements"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []
            self.statements = []

            # get Next Token without pop
            next_token = tokens[-1]
            # get type of statement from dic (or NONE)
            statement_type = Statements.STATEMENT_TYPES.get(
                next_token.value, None)

            while (next_token.name == "keyword" and
                   statement_type is not None):

                # Construct Statement
                new_statenent = statement_type(tokens)
                self.content.append(new_statenent)
                self.statements.append(new_statenent)

                # do the same as before the while loop
                next_token = tokens[-1]
                statement_type = Statements.STATEMENT_TYPES.get(
                    next_token.value, None)

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []
            # compile statements
            for statement in self.statements:
                compiled.extend(statement.compile(table))

            return compiled

    class JLetStatement(XMLString, Compile):
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

    class JIfStatement(XMLString, Compile):
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

    class JWhileStatement(XMLString, Compile):
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

    class JDoStatement(XMLString, Compile):
        """ 'do' subroutineCall ';' """
        xml_name = "doStatement"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            # 'do'
            token = tokens.pop()
            assert token == ("keyword", "do")
            self.content.append(token)

            # subroutineCall
            call = Expressions.JSubroutineCall(tokens)
            self.content.append(call)
            self.sub_call = call

            # ';'
            token = tokens.pop()
            assert token == ("symbol", ";")
            self.content.append(token)

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []
            # Compile Subrine
            compiled.extend(self.sub_call.compile(table))
            # remove 0 from stack, because this is a void method
            compiled.append("pop temp 0")
            return compiled

    class JReturnStatement(XMLString, Compile):
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
            self.expression = None
            if next_token != ("symbol", ";"):
                expression = Expressions.JExpression(tokens)
                self.expression = expression
                self.content.append(expression)

            # ';'
            token = tokens.pop()
            assert token == ("symbol", ";")
            self.content.append(token)

        def compile(self, table) -> list[str]:
            compiled = []

            # If it has an expression
            if self.expression is not None:
                compiled.extend(self.expression.compile(table))
            else:  # else it has type void
                # push dummy value on stack
                compiled.append("push constant 0")

            # return statement
            compiled.append("return")

            return compiled

    STATEMENT_TYPES = {"let": JLetStatement, "if": JIfStatement,
                       "while": JWhileStatement, "do": JDoStatement, "return": JReturnStatement}
