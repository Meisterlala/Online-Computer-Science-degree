""" Handels Code used for Functions and returns """
import translator.instructions as op


class Function(op.Operation):
    """ A Jack function operation
        eg: function foo 2
            function bar 0
    """

    def __init__(self, JackOP: str, SourceFile: str, lineNumber: int):
        super().__init__(JackOP, SourceFile, lineNumber)
        self.function_name = ""
        self.arguments = 0

    def parse(self) -> bool:
        # Length Check
        if len(self.s_op) != 3:
            return False

        if self.s_op[0] != "function":
            return False

        self.function_name = self.s_op[1]
        try:
            self.arguments = int(self.s_op[2])
        except ValueError:
            return False

        return True

    def translate(self):
        """ pseudo code:
            (functionName)
                for arguments:
                    push 0
        """
        return_value = super().translate()
        # Add Label
        label_name = self.function_name
        return_value.append(f"({label_name})")
        # Initilize Locals to 0
        return_value.extend(["@SP", "A=M"])
        for _ in range(self.arguments):
            return_value.extend(["M=0", "A=A+1"])
        # Incement SP
        return_value.extend([f"@{self.arguments}", "D=A", "@SP", "M=M+D"])
        return return_value


class Return(op.Operation):
    """ A Jack function operation
        eg: retun
    """

    end_frame_address = 14
    return_frame_address = 15

    def parse(self) -> bool:
        if len(self.s_op) != 1:
            return False
        if self.s_op[0] != "return":
            return False
        return True

    def translate(self):
        """
        endFrame = LCL
        retAddr = *(endFrame - 5)
        *ARG = pop()
        SP = ARG + 1
        THAT = *(endFrame - 1)
        THIS = *(endFrame - 2)
        ARG = *(endFrame - 3)
        LCL = *(endFrame - 4)
        goto retAddr
        """

        return_value = super().translate()

        def write_from_pointer(target, pointer: int, offset: int = 0):
            """ Helper for repeated reading of values of the Function frame.
                Assumes the offset is negative
                Pseudo code:
                    target = *(pointer - offset)
            Args:
                target (str): target of write
                pointer (int, optional): base address of pointer.
                offset (int, optional): pointer offset. Defaults to 0.
            """
            if offset < 0:
                print("ERROR, offset is assummed to be negative")
            return [f"@{pointer}", "D=M", f"@{offset}", "A=D-A", "D=M", f"@{target}", "M=D"]

        # endFrame = LCL
        return_value.extend(
            ["@LCL", "D=M", f"@{Return.end_frame_address}", "M=D"])
        # retAddr = *(endFrame - 5)
        return_value.extend(write_from_pointer(
            Return.return_frame_address, Return.end_frame_address, 5))
        # *ARG = pop()
        return_value.extend(["@SP", "A=M-1", "D=M", "@ARG", "A=M", "M=D"])
        # SP = ARG + 1
        return_value.extend(["@ARG", "D=M+1", "@SP", "M=D"])
        # THAT = *(endFrame - 1)
        return_value.extend(write_from_pointer(
            "THAT", Return.end_frame_address, 1))
        # THIS = *(endFrame - 2)
        return_value.extend(write_from_pointer(
            "THIS", Return.end_frame_address, 2))
        # ARG = *(endFrame - 3)
        return_value.extend(write_from_pointer(
            "ARG", Return.end_frame_address, 3))
        # LCL = *(endFrame - 4)
        return_value.extend(write_from_pointer(
            "LCL", Return.end_frame_address, 4))
        # goto retAddr
        return_value.extend(
            [f"@{Return.return_frame_address}", "A=M", "0;JMP"])
        return return_value
