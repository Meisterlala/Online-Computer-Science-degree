""" Containts all Jack Statements """


from .expression import Expressions
from ..parents import Compile, XMLString
from ..symbol_table import SymbolTable
from ..tokens import Token  # pylint: disable=unused-import


class Statements:
    """ Namespace class containg every class dealing with Statements"""

    class JStatements(XMLString, Compile):
        """ (letStatement | ifStatement| whileStatement | doStatement | returnStatement)* """
        xml_name = "statements"

        def __init__(self, tokens) -> None:
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

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []
            # compile statements
            for statement in self.statements:
                compiled.extend(statement.compile(table))

            return compiled

    class JLetStatement(XMLString, Compile):
        """ 'let' varName ('[' expression ']')? '=' expression ';' """
        xml_name = "letStatement"

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []
            self.is_array = False

            # 'let'
            token = tokens.pop()
            assert token == ("keyword", "let")
            self.content.append(token)

            # varName
            token = tokens.pop()
            assert token == ("identifier", None)
            self.content.append(token)
            self.target = token.value

            # ('[' expression ']')?
            next_token = tokens[-1]
            while next_token == ("symbol", "["):
                self.is_array = True

                # [
                self.content.append(tokens.pop())  # [

                # expression
                expression_array = Expressions.JExpression(tokens)
                self.content.append(expression_array)
                self.expression_array = expression_array

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
            expr = Expressions.JExpression(tokens)
            self.expression = expr
            self.content.append(expr)

            # ';'
            token = tokens.pop()
            assert token == ("symbol", ";")
            self.content.append(token)

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []

            if self.is_array:
                # push arr
                kind = table.kind_of(self.target)
                index = table.index_of(self.target)
                segment = "not_defined"
                if kind == SymbolTable.Entry.Kind.LOCAL:
                    segment = "local"
                elif kind == SymbolTable.Entry.Kind.STATIC:
                    segment = "static"
                elif kind == SymbolTable.Entry.Kind.FIELD:
                    segment = "this"
                elif kind == SymbolTable.Entry.Kind.ARG:
                    segment = "argument"

                compiled.extend(
                    [f"push {segment} {index} // array {self.target}"])

                # Compile expression
                compiled.extend(self.expression_array.compile(table))
                # add base value to offset
                compiled.append("add // Calculate offset")
                # Compile right expression
                compiled.extend(self.expression.compile(table))

                compiled.extend(["pop temp 2 // value of right site expression",
                                 f"pop pointer 1 // that = {self.target}[offset]",
                                 "push temp 2 // restore value",
                                 f"pop that 0 // {self.target}[offset]=value"])

            else:
                # Compile Expression
                compiled.extend(self.expression.compile(table))

                # pop into value
                index = table.index_of(self.target)
                kind = table.kind_of(self.target)
                if kind == SymbolTable.Entry.Kind.LOCAL:
                    compiled.append(f"pop local {index} // {self.target}")
                elif kind == SymbolTable.Entry.Kind.ARG:
                    compiled.append(f"pop argument {index} // {self.target}")
                elif kind == SymbolTable.Entry.Kind.STATIC:
                    compiled.append(f"pop static {index} // {self.target}")
                elif kind == SymbolTable.Entry.Kind.FIELD:
                    # Assume pointer 0 is this
                    compiled.append(f"pop this {index} // {self.target}")

            return compiled

    class JIfStatement(XMLString, Compile):
        """ 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')? """
        xml_name = "ifStatement"

        def __init__(self, tokens: "list[Token]") -> None:
            self.content = []
            self.has_else = False

            # 'if'
            token = tokens.pop()
            assert token == ("keyword", "if")
            self.content.append(token)

            # '('
            token = tokens.pop()
            assert token == ("symbol", "(")
            self.content.append(token)

            # expression
            expression = Expressions.JExpression(tokens)
            self.content.append(expression)
            self.expression = expression

            # ')'
            token = tokens.pop()
            assert token == ("symbol", ")")
            self.content.append(token)

            # '{'
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # statements
            statement1 = Statements.JStatements(tokens)
            self.content.append(statement1)
            self.statements_true = statement1

            # '}'
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

            # ('else' '{' statements '}')?
            next_token = tokens[-1]
            if next_token == ("keyword", "else"):
                self.content.append(tokens.pop())
                self.has_else = True

                # '{'
                token = tokens.pop()
                assert token == ("symbol", "{")
                self.content.append(token)

                # statements
                statement2 = Statements.JStatements(tokens)
                self.content.append(statement2)
                self.statements_false = statement2

                # '}'
                token = tokens.pop()
                assert token == ("symbol", "}")
                self.content.append(token)

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []

            u_index = table.get_unique_index()
            label1 = u_index + "_IF_FALSE"
            label2 = u_index + "_IF_END"

            if self.has_else:
                # Expression
                compiled.extend(self.expression.compile(table))
                # not
                compiled.append("not")
                # if-goto L1 (Start Label)
                compiled.append(f"if-goto {label1}")
                # statements True
                compiled.extend(self.statements_true.compile(table))
                # goto L2 (End Label)
                compiled.append(f"goto {label2}")

                # Label L1 (Start Label)
                compiled.append(f"label {label1}")
                # statements False
                compiled.extend(self.statements_false.compile(table))
                # Label L2 (End Label)
                compiled.append(f"label {label2}")
            else:
                # Expression
                compiled.extend(self.expression.compile(table))
                # not
                compiled.append("not")
                # goto L2 (End Label)
                compiled.append(f"if-goto {label2}")
                # statements True
                compiled.extend(self.statements_true.compile(table))
                # Label L2 (End Label)
                compiled.append(f"label {label2}")

            return compiled

    class JWhileStatement(XMLString, Compile):
        """ 'while' '(' expression ')' '{' statements '}' """
        xml_name = "whileStatement"

        def __init__(self, tokens: "list[Token]") -> None:
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
            expression = Expressions.JExpression(tokens)
            self.content.append(expression)
            self.expression = expression

            # ')'
            token = tokens.pop()
            assert token == ("symbol", ")")
            self.content.append(token)

            # '{'
            token = tokens.pop()
            assert token == ("symbol", "{")
            self.content.append(token)

            # statements
            statements = Statements.JStatements(tokens)
            self.content.append(statements)
            self.statements = statements

            # '}'
            token = tokens.pop()
            assert token == ("symbol", "}")
            self.content.append(token)

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []

            u_index = table.get_unique_index()
            label1 = u_index + "_WHILE_START"
            label2 = u_index + "_WHILE_END"

            # Label L1 (Start Label)
            compiled.append(f"label {label1}")
            # Expression
            compiled.extend(self.expression.compile(table))
            # not
            compiled.append("not")
            # if-goto L2 (End Label)
            compiled.append(f"if-goto {label2}")
            # statements
            compiled.extend(self.statements.compile(table))
            # goto L1 (Start Label)
            compiled.append(f"goto {label1}")
            # Label L2 (End Label)
            compiled.append(f"label {label2}")

            return compiled

    class JDoStatement(XMLString, Compile):
        """ 'do' subroutineCall ';' """
        xml_name = "doStatement"

        def __init__(self, tokens: "list[Token]") -> None:
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

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []
            # Compile subroutine
            compiled.extend(self.sub_call.compile(table))
            # remove 0 from stack, because this is a void method
            compiled.append("pop temp 0 // dump return type void")
            return compiled

    class JReturnStatement(XMLString, Compile):
        """ 'return' expression? ';' """
        xml_name = "returnStatement"

        def __init__(self, tokens: "list[Token]") -> None:
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

        def compile(self, table) -> "list[str]":
            compiled = []

            # If it has an expression
            if self.expression is not None:
                compiled.extend(self.expression.compile(table))
            else:  # else it has type void
                # push dummy value on stack
                compiled.append("push constant 0 // dummy void value")

            # return statement
            compiled.append("return")

            return compiled

    STATEMENT_TYPES = {"let": JLetStatement, "if": JIfStatement,
                       "while": JWhileStatement, "do": JDoStatement, "return": JReturnStatement}
