""" Serialises JackFiles acording to the grammar"""


from io import StringIO

from .jack_file import JackFile
from .tokens import Token, Tokens, Invalid


class Tokenizer():
    """ Cerates a list of Tokens, ignoring whitespace and following the grammar of Jack"""

    WHITESPACE = {"\n", " ", "\t", "\r"}
    SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";",
               "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
    KEYWORDS = {"class", "constructor", "function", "method", "field",
                "static", "char", "boolean",  "void", "true", "false",
                "null", "this", "let", "do", "if", "else", "while",
                "return", "var", "int"}

    def __init__(self, file: JackFile) -> None:
        self.jack_file = file
        self.raw_content = file.read()
        self.stream = StringIO(self.raw_content)
        self.raw_content_position = 0
        self.tokens = []

    def to_xml(self) -> list[str]:
        """ Uses the str() on all Tokens and outputs a list"""
        return_list = ["<tokens>"]
        for token in self.tokens:
            return_list.append(str(token))
        return_list.append("</tokens>")
        return return_list

    def tokenize(self):
        """ Main part of Tokenizer, it takes the input file and tokenizes everything"""

        self.ignore_white()

        while self.has_more_tokens():
            next_token = self.advance()
            self.ignore_white()

            self.tokens.append(next_token)

        return self.tokens

    def advance(self) -> Token:
        """ Read the next Token"""

        current_char = self.stream.read(1)

        # If symbol
        if current_char in Tokenizer.SYMBOLS:
            return Tokens.Symbol(current_char)

        # if IntConst
        if current_char.isdigit():
            number = current_char
            last_known_digit = self.stream.tell()
            next_char = self.stream.read(1)
            # While next char is a digit
            while next_char.isdigit():
                number += next_char
                next_char = self.stream.read(1)
            self.stream.seek(last_known_digit + len(number) - 1)
            return Tokens.IntConst(int(number))

        # if StringConst
        if current_char == '"':
            temp_string = ""
            next_char = self.stream.read(1)
            # while not the next "
            while next_char != '"':
                temp_string += next_char
                next_char = self.stream.read(1)
            return Tokens.StringConst(temp_string)

        # if Keyword
        is_keyword = False
        fallback_index = self.stream.tell()
        temp_keyword = current_char
        for _ in range(12):
            temp_keyword += self.stream.read(1)
            if temp_keyword in Tokenizer.KEYWORDS:
                is_keyword = True
                break

        if is_keyword:
            return Tokens.Keyword(temp_keyword)
        else:
            self.stream.seek(fallback_index)

        # if identifier
        if not current_char.isdigit():
            temp_name = current_char
            next_char = self.stream.read(1)
            # while letter, digit or _
            while next_char.isalnum() or next_char == "_":
                temp_name += next_char
                next_char = self.stream.read(1)
            self.stream.seek(self.stream.tell() - 1)
            return Tokens.Identifier(temp_name)

        return Invalid()

    def has_more_tokens(self) -> bool:
        """ True if there are more tokens"""
        index = self.stream.tell()

        # read one more to know if there is more
        current_char = self.stream.read(1)
        if current_char == "":
            return False

        # reset index
        self.stream.seek(index)
        return True

    def ignore_white(self):
        """ Seek past whitespace and comments"""

        chars = self.stream.read(2)

        # End of File
        if len(chars) != 2:
            return

        # Skip line if it begins with /
        if chars == "//":
            self.stream.readline()
            self.ignore_white()
            return

        # Ignore whitespace
        first_char = chars[0]
        if chars[0] in Tokenizer.WHITESPACE:
            if chars[1] not in Tokenizer.WHITESPACE:
                # Decrease index by 1, because only 1 of the 2 read chars is whitespace
                self.stream.seek(self.stream.tell() - 1)
                self.ignore_white()
                return

            while first_char in Tokenizer.WHITESPACE:
                first_char = self.stream.read(1)
            self.stream.seek(self.stream.tell() - 1)
            self.ignore_white()
            return

        # Ignore Multiline Comments
        if chars == "/*":
            buffer = ["", ""]
            while buffer != ["*", "/"]:
                buffer[0] = buffer[1]
                buffer[1] = self.stream.read(1)
            self.ignore_white()
            return

        # Decrease index by 2, for 2 read chars
        self.stream.seek(self.stream.tell() - 2)
        return
