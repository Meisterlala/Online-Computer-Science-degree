from colorama import Fore


class Operation:

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        self.JackOP = JackOP
        self.sOP = JackOP.split()
        self.fileName = SourceFile
        self.jumpID = str(lineNumber).zfill(8)
        pass

    def translate(self):
        return [f"// {self.JackOP}", ]

    def parse(self) -> bool:
        """ Try to Parse from input"""
        return False


SModes = ["push", "pop"]
STypes = ["constant", "local", "argument",
          "this", "that", "temp", "pointer", "static"]
SAdresses = {"stack": 0, "local": 1, "argument": 2, "this": 3, "that": 4}
STempRange = (5, 12)
SStaticRange = (16, 255)


class Stack(Operation):
    mode = ""
    type = ""
    value = 0

    def translate(self):
        r = super().translate()

        # constant
        if self._mt("push", "constant"):
            r.extend([f"@{self.value}",
                      "D=A", "@SP", "A=M", "M=D"])
            r.extend(_SPinc)
            return r

        # temp
        if self._mt("pop", "temp"):
            # SP --, D = *SP, tempAddr = D
            tempAddr = STempRange[0] + self.value
            if tempAddr > STempRange[1]:
                print(
                    Fore.RED + f"ERROR: Temp memory out of range ({STempRange})")
            # SP --, D = *SP
            r.extend(["@SP", "AM=M-1", "D=M"])
            # tempAddr = D
            r.extend([f"@{tempAddr}", "M=D"])
            return r

        if self._mt("push", "temp"):
            # SP++, *SP = tempadd
            tempAddr = STempRange[0] + self.value
            if tempAddr > STempRange[1]:
                print(
                    Fore.RED + f"ERROR: Temp memory out of range ({STempRange})")
            # D = tempAddr
            r.extend([f"@{tempAddr}", "D=M"])
            # *SP = D, SP ++
            r.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return r

        # pointer
        if self._mt("pop", "pointer"):
            # SP--, THIS/THAT = *SP
            if self.value == 0:
                thisthat = SAdresses.get("this")
            elif self.value == 1:
                thisthat = SAdresses.get("that")
            else:
                thisthat = SAdresses.get("this")
                print(
                    Fore.RED + f"ERROR: pointer can only be 0 or 1. not {self.value}")
            # SP --, D = *SP
            r.extend(["@SP", "AM=M-1", "D=M"])
            # THIS/THAT = D
            r.extend([f"@{thisthat}", "M=D"])
            return r

        if self._mt("push", "pointer"):
            # *SP = THIS/THAT, SP++
            if self.value == 0:
                thisthat = SAdresses.get("this")
            elif self.value == 1:
                thisthat = SAdresses.get("that")
            else:
                thisthat = SAdresses.get("this")
                print(
                    Fore.RED + f"ERROR: pointer can only be 0 or 1. not {self.value}")
            # D = THIS/THAT
            r.extend([f"@{thisthat}", "D=M"])
            # *SP = D, SP ++
            r.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return r

        # static
        if self._mt("pop", "static"):
            # SP --, @filename.value = *SP
            if SStaticRange[0] + self.value > SStaticRange[1]:
                print(Fore.RED + "ERROR: Static out of memory range")
            targetName = f"{self.fileName}.{self.value}"
            # SP --, D = @SP
            r.extend(["@SP", "AM=M-1", "D=M"])
            # @filename.value = D
            r.extend([f"@{targetName}", "M=D"])
            return r

        if self._mt("push", "static"):
            # *SP = @filename.value, SP ++
            if SStaticRange[0] + self.value > SStaticRange[1]:
                print(Fore.RED + "ERROR: Static out of memory range")
            targetName = f"{self.fileName}.{self.value}"
            #  D = @filename.value
            r.extend([f"@{targetName}", "D=M"])
            # SP ++, *SP = D
            r.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return r

        # local, argument, this, that
        if self.mode == "pop":
            # addr=LCL+i, SP--, *addr=*SP
            tempRegister = "@13"
            typeBase = SAdresses.get(self.type)
            # D = addr
            r.extend([f"@{typeBase}", "D=M", f"@{self.value}", "D=D+A"])
            # tempRegister = D
            r.extend([tempRegister, "M=D"])
            # SP --, D=*SP
            r.extend(["@SP", "AM=M-1", "D=M"])
            # *addr = *SP
            r.extend([tempRegister, "A=M", "M=D"])
            return r

        if self.mode == "push":
            # addr=LCL+i, *SP=*addr, SP++
            typeBase = SAdresses.get(self.type)
            # D = *addr + i
            r.extend([f"@{typeBase}", "D=M", f"@{self.value}", "A=D+A", "D=M"])
            # *SP = D, SP ++
            r.extend(["@SP", "AM=M+1", "A=A-1", "M=D"])
            return r

        # Default Case
        print(Fore.RED + f"ERROR: Unknown stack command ({self.JackOP})")
        return r

    def parse(self) -> bool:
        # Length
        if len(self.sOP) != 3:
            return False

        # Check for Push/Pop
        if self.sOP[0] in SModes:
            self.mode = self.sOP[0]
        else:
            return False

        # Check for type
        if self.sOP[1] in STypes:
            self.type = self.sOP[1]
        else:
            return False

        # Value
        self.value = int(self.sOP[2])

        return True

    def _mt(self, mode: str, type: str) -> bool:
        return self.mode == mode and self.type == type


ATypes = ["add", "sub", "neg", "and", "or", "not", "eq", "lt", "gt"]


class Arithmetic(Operation):
    type = ""

    def translate(self):
        r = super().translate()

        if self.type == "add":
            r.extend(_SPread2)
            r.extend(["M=M+D"])
            return r

        if self.type == "sub":
            r.extend(_SPread2)
            r.extend(["M=M-D"])
            return r

        if self.type == "neg":
            r.extend(_SPfollow)
            r.extend(["D=0", "M=D-M"])
            return r

        if self.type == "and":
            r.extend(_SPread2)
            r.extend(["M=D&M"])
            return r

        if self.type == "or":
            r.extend(_SPread2)
            r.extend(["M=D|M"])
            return r

        if self.type == "not":
            r.extend(_SPfollow)
            r.extend(["M=!M"])
            return r

        if self.type == "eq":
            r.extend(self.comparison("JEQ"))
            return r

        if self.type == "lt":
            r.extend(self.comparison("JGT"))
            return r

        if self.type == "gt":
            r.extend(self.comparison("JLT"))
            return r

        # Default Case
        print(
            Fore.RED + f"ERROR: unknown arithmetic operation ({self.JackOP})")
        return r

    def comparison(self, type: str):
        return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=D-M", f"@TRUE_{self.jumpID}", f"D;{type}",
                "@SP", "A=M-1", "M=0", f"@END_{self.jumpID}", "0;JMP",
                f"(TRUE_{self.jumpID})", "@SP", "A=M-1", "M=-1", f"(END_{self.jumpID})"]

    def parse(self) -> bool:
        # Length
        if len(self.sOP) != 1:
            return False

        # Check for Type (add, sub, gt, ...)
        if self.sOP[0] in ATypes:
            self.type = self.sOP[0]
        else:
            return False

        return True


class Invalid(Operation):
    def __init__(self):
        pass
    pass


class Comment(Operation):
    def __init__(self):
        pass
    pass


# Common Stuff
_SPdec = ["@SP", "M=M-1"]
_SPinc = ["@SP", "M=M+1"]
_SPfollowAndDec = ["@SP", "AM=M-1"]
_SPfollow = ["@SP", "A=M-1"]
_SPread2 = ["@SP", "AM=M-1", "D=M", "A=A-1"]
