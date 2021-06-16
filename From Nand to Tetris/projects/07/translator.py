#!/usr/bin/env python
import sys
import os.path
from concurrent.futures import ProcessPoolExecutor, wait


def main():

    if len(sys.argv) != 2:
        print("Usage: translator.py filename")
        print(f"Given: {str(sys.argv)}")
        sys.exit(1)

    # If File doesn't exits
    filename = str(sys.argv[1])
    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        sys.exit(1)
    # Check for wrong format
    if not os.path.splitext(filename)[1] == ".vm":
        print(f"Wrong File extenstion, please use .vm")
        sys.exit(0)  # Should be a 1

    # Open File
    file = open(filename, "r").read()

    # Remove comments and white space
    file = removeWhite(file)

    # Translate
    asm = translate(file)

    # Write output
    out = open(os.path.splitext(filename)[0] +
               ".asm", "w")
    out.write(asm)
    out.close()

    sys.exit(0)


def removeWhite(code):
    result = ""
    # Hanle each line seperate
    for line in code.splitlines():
        # Remove whitespaces
        line = line.strip()
        resultLine = ""
        for char in line:
            if char == "/":
                break
            resultLine += char
        if resultLine != "":
            result += resultLine + "\n"
    # Remove trailing newline
    return result[:-1]


def translate(code: str):
    # Multi threading
    pool = ProcessPoolExecutor()
    futures = []

    stack = ["push", "pop"]
    logic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or"]
    branch = ["label", "goto", "if-goto"]
    funtion = ["function", "call", "return"]

    jmpID = 0
    for line in code.splitlines():

        words = line.split()

        if words[0] in stack:
            futures.append(pool.submit(translateStack, words))
            continue

        if words[0] in logic:
            jmpID += 1
            futures.append(pool.submit(translateLogic, words, jmpID))
            continue

    # Join Threads
    wait(futures)
    result = ""
    for f in futures:
        result += str(f.result())

    return result[:-1]


segmentAdresses = {
    "local": 1,
    "argument": 2,
    "this": 3,
    "that": 4
}


def translateStack(op):
    result = f"// {op[0]} {op[1]} {op[2]}\n"

    # local, argument, this, that
    if op[1] in segmentAdresses.keys():
        segPointer = segmentAdresses.get(op[1])
        result += (f"@{segPointer}\n"
                   "D=M\n"
                   f"@{op[2]}\n"
                   "D=D+A\n"
                   "@addr\n"
                   "M=D")

        if op[0] == "push":
            result += ("@addr\n"
                       "A=M\n"
                       "D=M\n"
                       "@SP\n"
                       "A=M\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M+1\n")
        else:  # pull
            pass
        return result

    # constant
    if op[1] == "constant":
        result += (f"@{op[2]}\n"
                   "D=A\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n")
        return result

    return "sta\n"


def translateLogic(op, jmpID):
    result = f"// {op[0]}\n"
    if op[0] == "add":
        result += """@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
M=M-1
"""
    elif op[0] == "sub":
        result += """@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
"""
    elif op[0] == "neg":
        result += """@SP
A=M-1
M=!M
"""
    elif op[0] == "eq":
        result += ("@SP\n"
                   "A=M-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "D=D-M\n"
                   f"@label_{str(jmpID)}\n"
                   "D;JEQ\n"
                   "@SP\n"
                   "M=M-1\n"
                   "A=M-1\n"
                   "M=0\n"
                   f"@labeln_{str(jmpID)}\n"
                   "0;JMP\n"
                   f"(label_{str(jmpID)})\n"
                   "@SP\n"
                   "M=M-1\n"
                   "A=M-1\n"
                   "M=1\n"
                   f"(labeln_{str(jmpID)})\n")

    elif op[0] == "gt":
        result += ("@SP\n"
                   "A=M-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "D=D-M\n"
                   f"@label_{str(jmpID)}\n"
                   "D;JGT\n"
                   "@SP\n"
                   "M=M-1\n"
                   "A=M-1\n"
                   "M=0\n"
                   f"@labeln_{str(jmpID)}\n"
                   "0;JMP\n"
                   f"(label_{str(jmpID)})\n"
                   "@SP\n"
                   "M=M-1\n"
                   "A=M-1\n"
                   "M=1\n"
                   f"(labeln_{str(jmpID)})\n")
    elif op[0] == "lt":
        result += ("@SP\n"
                   "A=M-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "D=D-M\n"
                   f"@label_{str(jmpID)}\n"
                   "D;JLT\n"
                   "@SP\n"
                   "M=M-1\n"
                   "A=M-1\n"
                   "M=0\n"
                   f"@labeln_{str(jmpID)}\n"
                   "0;JMP\n"
                   f"(label_{str(jmpID)})\n"
                   "@SP\n"
                   "M=M-1\n"
                   "A=M-1\n"
                   "M=1\n"
                   f"(labeln_{str(jmpID)})\n")
    elif op[0] == "and":
        result += """@SP
A=M-1
D=M
@SP
M=M-1
A=M-1
M=D|M
"""
    elif op[0] == "or":
        result += """@SP
A=M-1
D=M
@SP
M=M-1
A=M-1
M=D&M
"""
    elif op[0] == "not":
        result += """@SP
A=M-1
M=!M
"""
    return result


if __name__ == "__main__":
    main()
