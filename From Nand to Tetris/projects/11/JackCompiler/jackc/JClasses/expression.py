""" Containts all Jack Expressions """
from enum import Enum
from jackc.parents import Compile, XMLString
from jackc.symbol_table import SymbolTable
from jackc.tokens import Token


class Expressions:
    """ Namespace class containg every class dealing with Statements"""

    KEYWORD_CONSTANTS = {"true", "false", "null", "this"}
    OPS = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
    UNARY_OPS = {"-", "~"}

    class JExpression(XMLString, Compile):
        """ term (op term)* """
        xml_name = "expression"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []
            self.terms_and_ops: list[tuple[Expressions.JTerm, Token]] = []

            # term
            term_1 = Expressions.JTerm(tokens)
            self.content.append(term_1)
            self.first_term = term_1

            # (op term)*
            next_token = tokens[-1]
            while (next_token.name == "symbol" and
                   next_token.value in Expressions.OPS):
                # op
                operator = tokens.pop()
                self.content.append(operator)

                # term
                term_next = Expressions.JTerm(tokens)
                self.content.append(term_next)

                self.terms_and_ops.append((term_next, operator))

                next_token = tokens[-1]

        def compile(self, table) -> list[str]:
            compiled = []

            # Compile first term
            compiled.extend(self.first_term.compile(table))

            # Compile next Term
            for term, operator in self.terms_and_ops:
                compiled.extend(term.compile(table))

                # Do Operation
                compiled.extend(Expressions.JOperation.compile(operator))

            return compiled

    class JOperation():
        """ Simple Compile or Covert from OP to Jack VM call"""
        OPS = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
        lookup_table = {"+": ["add"],
                        "-": ["sub"],
                        "*": ["call Math.multiply 2"],
                        "/": ["call Math.divide 2"],
                        "&": [" & not imp"],
                        "|": [" | not imp"],
                        "<": [" < not imp"],
                        ">": [" > not imp"],
                        "=": [" = not imp"]}

        @staticmethod
        def compile(token: Token) -> list[str]:
            """ Convert from op Token to JackVM call"""
            return Expressions.JOperation.lookup_table.get(token.value, [])

    class JTerm(XMLString, Compile):
        """ integerConstant | stringConstant | keywordConstant | varName |
            varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOP term """
        xml_name = "term"

        class TermType(Enum):
            """ Type of the Term for compilation"""
            INTCONST = 0
            STRINGCONST = 1
            KEYWORDCONST = 2
            VARNAME = 3
            VARNAME_EXP = 4
            SUBCALL = 5
            EXP = 6
            UNARY = 7
            INVALID = 8

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            token = tokens.pop()
            self.term_type = Expressions.JTerm.TermType.INVALID

            # IntergerConstant
            if token == ("integerConstant", None):
                self.content.append(token)
                self.term_type = Expressions.JTerm.TermType.INTCONST
                self.value = token.value
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
                self.term_type = Expressions.JTerm.TermType.EXP

                # '('
                self.content.append(token)

                # expression
                expression = Expressions.JExpression(tokens)
                self.content.append(expression)
                self.expression = expression

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

        def compile(self, table) -> list[str]:
            if self.term_type == Expressions.JTerm.TermType.INTCONST:
                return [f"push constant {self.value}"]
            if self.term_type == Expressions.JTerm.TermType.EXP:
                return self.expression.compile(table)

            return ["TermType not implemented"]

    class JExpressionList(XMLString, Compile):
        """ (expression (',' expression)*)?
            Expects every empty expression list to be followed by a ')'
        """

        xml_name = "expressionList"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []
            self.length = 0
            self.expressions = []

            # Expects every empty expression list to be followed by a ')'
            possible_bracket = tokens[-1]
            if possible_bracket == ("symbol", ")"):
                return

            # expression
            expr = Expressions.JExpression(tokens)
            self.content.append(expr)
            self.expressions.append(expr)
            self.length += 1

            # (',' expression)*
            next_token = tokens[-1]
            while next_token == ("symbol", ","):
                # ','
                self.content.append(tokens.pop())

                # expression
                expr = Expressions.JExpression(tokens)
                self.content.append(expr)
                self.expressions.append(expr)
                self.length += 1
                next_token = tokens[-1]

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []
            for expression in self.expressions:
                compiled.extend(expression.compile(table))
            return compiled

    class JSubroutineCall(XMLString, Compile):
        """ subroutineName '(' expressionList ')' |
            (className | varName) '.' subroutineName '(' expressionList ')' """
        xml_name = "subroutineCall"

        def __init__(self, tokens: list[Token]) -> None:
            self.content = []

            possible_dot = tokens[-2]
            if possible_dot != ("symbol", "."):
                self.class_name = None

                # subroutineName
                token = tokens.pop()
                assert token == ("identifier", None)
                self.subroutine_name = token
                self.content.append(token)

                # '('
                token = tokens.pop()
                assert token == ("symbol", "(")
                self.content.append(token)

                # expressionList
                e_list = Expressions.JExpressionList(tokens)
                self.content.append(e_list)
                self.expression_list = e_list

                # ')'
                token = tokens.pop()
                assert token == ("symbol", ")")
                self.content.append(token)
            else:
                # (className | varName)
                token = tokens.pop()
                assert token == ("identifier", None)
                self.content.append(token)
                self.class_name = token

                # '.'
                token = tokens.pop()
                assert token == ("symbol", ".")
                self.content.append(token)

                # subroutineName
                token = tokens.pop()
                assert token == ("identifier", None)
                self.content.append(token)
                self.subroutine_name = token

                # '('
                token = tokens.pop()
                assert token == ("symbol", "(")
                self.content.append(token)

                # expressionList
                e_list = Expressions.JExpressionList(tokens)
                self.content.append(e_list)
                self.expression_list = e_list

                # ')'
                token = tokens.pop()
                assert token == ("symbol", ")")
                self.content.append(token)

        def __str__(self) -> str:
            """ Dont Display self Name"""
            return "\n".join(str(x) for x in self.content)

        def compile(self, table: SymbolTable) -> list[str]:
            compiled = []

            # push expressions onto stack
            compiled.extend(self.expression_list.compile(table))

            # call function
            # If the subroutine call has no Class name, assume the current class as name
            name = ""
            if self.class_name is None:
                name = table.class_name
            else:
                name = self.class_name.value

            length = self.expression_list.length
            sub_name = self.subroutine_name.value

            compiled.append(f"call {name}.{sub_name} {length}")

            return compiled
