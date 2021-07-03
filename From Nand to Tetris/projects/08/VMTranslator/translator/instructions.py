""" Containes all the code to parse and translate Operation """
from typing import List
from colorama import Fore


class Operation:
    """ represents a Jack OP code """

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        self.jack_op = JackOP
        self.s_op = JackOP.split()
        self.file_name = SourceFile
        self.jump_id = str(lineNumber).zfill(8)

    def translate(self) -> List[str]:
        """ Used for adding a Comment"""
        return [f"// {self.jack_op}", ]

    def parse(self) -> bool:
        """ Try to Parse from input"""
        return False


class Stack(Operation):
    """ A Jack stack operation
        eg: push static 0
            pop local 1
    """

    Modes = ["push", "pop"]
    Types = ["constant", "local", "argument",
             "this", "that", "temp", "pointer", "static"]
    Adresses = {"stack": "SP", "local": "LCL",
                "argument": "ARG", "this": "THIS", "that": "THAT"}
    TempRange = (5, 12)
    StaticRange = (16, 255)

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        super().__init__(JackOP, SourceFile, lineNumber)
        self.type = ""
        self.mode = ""
        self.value = 0

    def translate(self):
        return_value = super().translate()

        # constant
        if self._mt("push", "constant"):
            return_value.extend([f"@{self.value}",
                                 "D=A", "@SP", "A=M", "M=D"])
            return_value.extend(["@SP", "M=M+1"])
            return return_value

        # temp
        if self._mt("pop", "temp"):
            # SP --, D = *SP, tempAddr = D
            temp_addr = Stack.TempRange[0] + self.value
            if temp_addr > Stack.TempRange[1]:
                print(
                    Fore.RED + f"ERROR: Temp memory out of range ({Stack.TempRange})")
            # SP --, D = *SP
            return_value.extend(["@SP", "AM=M-1", "D=M"])
            # tempAddr = D
            return_value.extend([f"@{temp_addr}", "M=D"])
            return return_value

        if self._mt("push", "temp"):
            # SP++, *SP = tempadd
            temp_addr = Stack.TempRange[0] + self.value
            if temp_addr > Stack.TempRange[1]:
                print(
                    Fore.RED + f"ERROR: Temp memory out of range ({Stack.TempRange})")
            # D = tempAddr
            return_value.extend([f"@{temp_addr}", "D=M"])
            # *SP = D, SP ++
            return_value.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return return_value

        # pointer
        if self._mt("pop", "pointer"):
            # SP--, THIS/THAT = *SP
            if self.value == 0:
                thisthat = Stack.Adresses.get("this")
            elif self.value == 1:
                thisthat = Stack.Adresses.get("that")
            else:
                thisthat = Stack.Adresses.get("this")
                print(
                    Fore.RED + f"ERROR: pointer can only be 0 or 1. not {self.value}")
            # SP --, D = *SP
            return_value.extend(["@SP", "AM=M-1", "D=M"])
            # THIS/THAT = D
            return_value.extend([f"@{thisthat}", "M=D"])
            return return_value

        if self._mt("push", "pointer"):
            # *SP = THIS/THAT, SP++
            if self.value == 0:
                thisthat = Stack.Adresses.get("this")
            elif self.value == 1:
                thisthat = Stack.Adresses.get("that")
            else:
                thisthat = Stack.Adresses.get("this")
                print(
                    Fore.RED + f"ERROR: pointer can only be 0 or 1. not {self.value}")
            # D = THIS/THAT
            return_value.extend([f"@{thisthat}", "D=M"])
            # *SP = D, SP ++
            return_value.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return return_value

        # static
        if self._mt("pop", "static"):
            # SP --, @filename.value = *SP
            if Stack.StaticRange[0] + self.value > Stack.StaticRange[1]:
                print(Fore.RED + "ERROR: Static out of memory range")
            target_name = f"{self.file_name}.{self.value}"
            # SP --, D = @SP
            return_value.extend(["@SP", "AM=M-1", "D=M"])
            # @filename.value = D
            return_value.extend([f"@{target_name}", "M=D"])
            return return_value

        if self._mt("push", "static"):
            # *SP = @filename.value, SP ++
            if Stack.StaticRange[0] + self.value > Stack.StaticRange[1]:
                print(Fore.RED + "ERROR: Static out of memory range")
            target_name = f"{self.file_name}.{self.value}"
            #  D = @filename.value
            return_value.extend([f"@{target_name}", "D=M"])
            # SP ++, *SP = D
            return_value.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return return_value

        # local, argument, this, that
        if self.mode == "pop":
            # addr=LCL+i, SP--, *addr=*SP
            temp_register = "@13"
            type_base = Stack.Adresses.get(self.type)
            # D = addr
            return_value.extend([f"@{type_base}", "D=M"])
            if self.value != 0:
                return_value.extend([f"@{self.value}", "D=D+A"])
            # tempRegister = D
            return_value.extend([temp_register, "M=D"])
            # SP --, D=*SP
            return_value.extend(["@SP", "AM=M-1", "D=M"])
            # *addr = *SP
            return_value.extend([temp_register, "A=M", "M=D"])
            return return_value

        if self.mode == "push":
            # addr=LCL+i, *SP=*addr, SP++
            type_base = Stack.Adresses.get(self.type)
            # D = *addr + i
            if self.value == 0:
                return_value.extend([f"@{type_base}", "A=M", "D=M"])
            else:
                return_value.extend([f"@{type_base}", "D=M",
                                     f"@{self.value}", "A=D+A", "D=M"])
            # *SP = D, SP ++
            return_value.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return return_value

        # Default Case
        print(Fore.RED + f"ERROR: Unknown stack command ({self.jack_op})")
        return return_value

    def parse(self) -> bool:
        # Length
        if len(self.s_op) != 3:
            return False

        # Check for Push/Pop
        if self.s_op[0] in Stack.Modes:
            self.mode = self.s_op[0]
        else:
            return False

        # Check for type
        if self.s_op[1] in Stack.Types:
            self.type = self.s_op[1]
        else:
            return False

        # Value
        self.value = int(self.s_op[2])

        return True

    def _mt(self, mode: str, stype: str) -> bool:
        return self.mode == mode and self.type == stype


class Arithmetic(Operation):
    """ A Jack arithmetic operation
        eg: add
            sub
    """

    Types = ["add", "sub", "neg", "and", "or", "not", "eq", "lt", "gt"]

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        super().__init__(JackOP, SourceFile, lineNumber)
        self.type = ""

    def translate(self):
        return_value = super().translate()

        _sp_read2 = ["@SP", "AM=M-1", "D=M", "A=A-1"]

        if self.type == "add":
            return_value.extend(_sp_read2)
            return_value.extend(["M=M+D"])
            return return_value

        if self.type == "sub":
            return_value.extend(_sp_read2)
            return_value.extend(["M=M-D"])
            return return_value

        if self.type == "neg":
            return_value.extend(["@SP", "A=M-1"])
            return_value.extend(["D=0", "M=D-M"])
            return return_value

        if self.type == "and":
            return_value.extend(_sp_read2)
            return_value.extend(["M=D&M"])
            return return_value

        if self.type == "or":
            return_value.extend(_sp_read2)
            return_value.extend(["M=D|M"])
            return return_value

        if self.type == "not":
            return_value.extend(["@SP", "A=M-1"])
            return_value.extend(["M=!M"])
            return return_value

        if self.type == "eq":
            return_value.extend(self.comparison("JEQ"))
            return return_value

        if self.type == "lt":
            return_value.extend(self.comparison("JGT"))
            return return_value

        if self.type == "gt":
            return_value.extend(self.comparison("JLT"))
            return return_value

        # Default Case
        print(
            Fore.RED + f"ERROR: unknown arithmetic operation ({self.jack_op})")
        return return_value

    def comparison(self, stype: str):
        """ Template for Comparisons, needing a Jump """
        return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=D-M", f"@TRUE_{self.jump_id}", f"D;{stype}",
                "@SP", "A=M-1", "M=0", f"@END_{self.jump_id}", "0;JMP",
                f"(TRUE_{self.jump_id})", "@SP", "A=M-1", "M=-1", f"(END_{self.jump_id})"]

    def parse(self) -> bool:
        # Length
        if len(self.s_op) != 1:
            return False

        # Check for Type (add, sub, gt, ...)
        if self.s_op[0] in Arithmetic.Types:
            self.type = self.s_op[0]
        else:
            return False

        return True


class Label(Operation):
    """ A Jack label operation
        eg: label Cool_Stuff
    """

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        super().__init__(JackOP, SourceFile, lineNumber)
        self.label = ""

    def parse(self) -> bool:
        # Length
        if len(self.s_op) != 2:
            return False

        # Has to start with "label"
        if self.s_op[0] != "label":
            return False

        self.label = self.s_op[1]

        return True

    def translate(self):
        return_value = super().translate()
        label_name = f"{self.file_name}.funcName${self.label}"
        return_value.append(f"({label_name})")
        return return_value


class GoTo(Operation):
    """ A Jack GoTo operation
        eg: goto Cool_Stuff
            if-goto Bad_Stuff
    """

    types = ["if-goto", "goto"]

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        super().__init__(JackOP, SourceFile, lineNumber)
        self.type = ""
        self.label = ""

    def parse(self) -> bool:
        # Length
        if len(self.s_op) != 2:
            return False

        # Goto or if-Goto
        if self.s_op[0] in GoTo.types:
            self.type = self.s_op[0]
        else:
            return False

        self.label = self.s_op[1]

        return True

    def translate(self):
        return_value = super().translate()

        label_name = f"{self.file_name}.funcName${self.label}"

        if self.type == "if-goto":
            # SP --, D = *SP
            return_value.extend(["@SP", "AM=M-1", "D=M"])
            # JGT -> labelname
            return_value.extend([f"@{label_name}", "D;JGT"])
        elif self.type == "goto":
            # JMP -> labelname
            return_value.extend([f"@{label_name}", "0;JMP"])
        return return_value


class Invalid(Operation):
    """ Empty Operation to represent a invalid Operation """
    # pylint: disable=super-init-not-called

    def __init__(self, line):
        self.jack_op = line


class Comment(Operation):
    """ Empty Operation to represent a Comment """
    # pylint: disable=super-init-not-called

    def __init__(self):
        pass
