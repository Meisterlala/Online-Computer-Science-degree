""" Containts all Jack Expressions """


from enum import Enum
from ..parents import Compile, XMLString
from ..symbol_table import SymbolTable
from ..tokens import Token  # pylint: disable=unused-import


class Expressions:
    """ Namespace class containg every class dealing with Statements"""

    KEYWORD_CONSTANTS = {"true", "false", "null", "this"}
    OPS = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
    UNARY_OPS = {"-", "~"}

    class JExpression(XMLString, Compile):
        """ term (op term)* """
        xml_name = "expression"

        def __init__(self, tokens) -> None:
            self.content = []
            self.terms_and_ops: "list[tuple[Expressions.JTerm, Token]]" = []

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

        def compile(self, table) -> "list[str]":
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

        lookup_table = {"+": ["add"],
                        "-": ["sub"],
                        "*": ["call Math.multiply 2"],
                        "/": ["call Math.divide 2"],
                        "&": ["and"],
                        "|": ["or"],
                        "<": ["lt"],
                        ">": ["gt"],
                        "=": ["eq"]}

        @staticmethod
        def compile(token: "Token") -> "list[str]":
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

        def __init__(self, tokens: "list[Token]") -> None:
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
                self.term_type = Expressions.JTerm.TermType.STRINGCONST

                self.content.append(token)
                return

            # KeywordConstant
            if (token.name == "keyword" and
                    token.value in Expressions.KEYWORD_CONSTANTS):
                self.term_type = Expressions.JTerm.TermType.KEYWORDCONST
                self.key_word = token.value
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
                self.term_type = Expressions.JTerm.TermType.UNARY
                self.content.append(token)
                self.unary_type = token.value

                # term
                term = Expressions.JTerm(tokens)
                self.term = term
                self.content.append(term)
                return

            # subroutineCall
            next_token = tokens[-1]
            if (next_token == ("symbol", "(") or
                    next_token == ("symbol", ".")):

                self.term_type = Expressions.JTerm.TermType.SUBCALL
                assert token == ("identifier", None)
                tokens.append(token)
                sub_call = Expressions.JSubroutineCall(tokens)
                self.content.append(sub_call)
                self.sub_call = sub_call

                return

            # varName  ('[' expression ']')
            if token == ("identifier", None):
                self.term_type = Expressions.JTerm.TermType.VARNAME
                self.content.append(token)
                self.var_name = token.value

                if next_token == ("symbol", "["):
                    self.term_type = Expressions.JTerm.TermType.VARNAME_EXP

                    # '['
                    self.content.append(tokens.pop())

                    # expression
                    self.content.append(Expressions.JExpression(tokens))

                    # ']'
                    token = tokens.pop()
                    assert token == ("symbol", "]")
                    self.content.append(token)
                return

        def compile(self, table: SymbolTable) -> "list[str]":
            if self.term_type == Expressions.JTerm.TermType.INTCONST:
                return [f"push constant {self.value}"]

            if self.term_type == Expressions.JTerm.TermType.EXP:
                return self.expression.compile(table)

            if self.term_type == Expressions.JTerm.TermType.UNARY:
                compiled = self.term.compile(table)
                if self.unary_type == "-":
                    compiled.append("neg")
                else:  # ~
                    compiled.append("not")
                return compiled

            if self.term_type == Expressions.JTerm.TermType.SUBCALL:
                return self.sub_call.compile(table)

            if self.term_type == Expressions.JTerm.TermType.VARNAME:

                kind = table.kind_of(self.var_name)
                index = table.index_of(self.var_name)
                segment = "not_defined"
                if kind == SymbolTable.Entry.Kind.LOCAL:
                    segment = "local"
                elif kind == SymbolTable.Entry.Kind.STATIC:
                    segment = "static"
                elif kind == SymbolTable.Entry.Kind.FIELD:
                    segment = "this"
                elif kind == SymbolTable.Entry.Kind.ARG:
                    segment = "argument"

                return [f"push {segment} {index} // {self.var_name}"]

            if self.term_type == Expressions.JTerm.TermType.KEYWORDCONST:
                if self.key_word in ("null", "false"):
                    return ["push constant 0 // false or null"]
                elif self.key_word == "true":
                    return["push constant 1", "neg // True"]
                elif self.key_word == "this":
                    # this
                    return["push pointer 0 // return base adress"]

            return ["TermType not implemented " + str(self.term_type)]

    class JExpressionList(XMLString, Compile):
        """ (expression (',' expression)*)?
            Expects every empty expression list to be followed by a ')'
        """

        xml_name = "expressionList"

        def __init__(self, tokens: "list[Token]") -> None:
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

        def compile(self, table: SymbolTable) -> "list[str]":
            compiled = []
            for expression in self.expressions:
                compiled.extend(expression.compile(table))
            return compiled

    class JSubroutineCall(XMLString, Compile):
        """ subroutineName '(' expressionList ')' |
            (className | varName) '.' subroutineName '(' expressionList ')' """
        xml_name = "subroutineCall"

        def __init__(self, tokens) -> None:
            self.content = []

            possible_dot = tokens[-2]
            if possible_dot != ("symbol", "."):
                self.class_var_name = None

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
                self.class_var_name = token

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

        def compile(self, table: "SymbolTable") -> "list[str]":
            compiled = []
            calling_method = False
            calling_on_object = False
            obj_name = ""

            # Figure out what type it is trying to call
            # If the subroutine call has no Class name, assume the current class as name
            name = ""
            if self.class_var_name is None:
                name = table.class_name
                calling_method = True
            else:
                name = self.class_var_name.value

                # if class_name is a variable, use the class
                potential_type = table.j_type_of(name)
                if potential_type is not None:
                    obj_name = name
                    name = potential_type
                    calling_method = True
                    calling_on_object = True
            length = self.expression_list.length
            sub_name = self.subroutine_name.value

            # Inc argument lenght if calling a method
            if calling_method:
                length += 1

            if calling_on_object:
                # Push object base adress as argument
                vm_type = table.kind_of(obj_name)
                assert vm_type is not None  # already found previusly
                segment = ""
                if vm_type == SymbolTable.Entry.Kind.STATIC:
                    segment = "static"
                elif vm_type == SymbolTable.Entry.Kind.ARG:
                    segment = "argument"
                elif vm_type == SymbolTable.Entry.Kind.FIELD:
                    segment = "this"
                elif vm_type == SymbolTable.Entry.Kind.LOCAL:
                    segment = "local"
                index = table.index_of(obj_name)

                # Push base adress of obj
                compiled.append(
                    f"push {segment} {index} // base adress of {obj_name}")

            elif calling_method:
                # Push this as Argument
                compiled.append(
                    "push pointer 0 // push this as reference for method")

            # push expressions onto stack
            compiled.extend(self.expression_list.compile(table))

            # call function
            compiled.append(f"call {name}.{sub_name} {length}")

            return compiled
