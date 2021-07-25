""" Parent Classes for JClasses """


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


class Compile():
    """ Parent Class to compile to JackVM """

    def compile(self, table) -> list[str]:
        """ Compile self to JackVM """
        # pylint: disable=unused-argument
        return [str(self)]
