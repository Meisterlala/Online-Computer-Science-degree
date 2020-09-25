#!/usr/bin/env python
import sys
import os.path


def main():
    # Check Argumets
    if "-v" in sys.argv:
        sys.argv.remove("-v")
        verbose = True
    else:
        verbose = False

    if len(sys.argv) != 2:
        print("Usage: assembler.py filename (-v)")
        print(f"Given: {str(sys.argv)}")
        sys.exit(1)

    # Load file
    filename = str(sys.argv[1])
    # If File doesn't exits
    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        sys.exit(1)
    # Check for wrong format
    if not os.path.splitext(filename)[1] == ".asm":
        print(f"Wrong File extenstion, please use .asm")
        sys.exit(0)  # Should be a 1

    # Open File
    file = open(filename, "r").read()

    # Remove comments and white space
    file = removeWhite(file)

    # Process symbols
    file = resolveSymbols(file)

    if verbose:
        print(file)

    # Select Instruction
    binary = ""
    for instruction in file.splitlines():
        if instruction[0] == "@":
            binary += assembleA(instruction[1:]) + "\n"
        else:
            binary += assembleC(instruction) + "\n"
    # Remove trailing new line
    binary = binary[:-1]

    # Write output
    out = open(os.path.splitext(filename)[0] +
               ".hack", "w")
    out.write(binary)
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
            if char == " ":
                continue
            resultLine += char
        if resultLine != "":
            result += resultLine + "\n"
    # Remove trailing newline
    return result[:-1]


def assembleA(op):
    # Convert from Decimal to Binary
    return "{0:016b}".format(int(op))


def assembleC(op: str):
    # Start Code for C-Instruction
    result = "111"

    # Check if there is a dest
    if op.find("=") != -1:
        dest = op.split("=")[0]
        rest = op.split("=")[1]
    else:
        dest = "NULL"
        rest = op

    # Check if there is a jmp
    if rest.find(";") != -1:
        comp = rest.split(";")[0]
        jmp = rest.split(";")[1]
    else:
        comp = rest
        jmp = "NULL"

    # Normalize strings to upper
    dest = dest.upper()
    comp = comp.upper()
    jmp = jmp.upper()

    # Set "a" Bit
    if comp.find("M") != -1:
        comp = comp.replace("M", "A")
        result += "1"
    else:
        result += "0"

    # Lookup in Dictinary, to translate to "binary"
    result += Dcomp.get(comp, "ERROR")
    result += Ddest.get(dest, "ERROR")
    result += Djump.get(jmp, "ERROR")

    # Exit if Error
    if result.find("ERROR") != -1:
        print(f"Could not decode instruction: {op}")
        sys.exit(1)

    return result


Dcomp = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101"
}

Ddest = {
    "NULL": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

Djump = {
    "NULL": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


def resolveSymbols(code):

    # Load labels
    linenumber = 0
    codeclean = ""
    for line in code.splitlines():
        if line[0] == "(" and line[-1] == ")":
            label = line[1:-1].strip()

            # Throw error
            if label in Dsym:
                print(f"Label dumplicate or System value: {label}")
                sys.exit(1)

            Dsym[label] = linenumber
        else:
            codeclean += f"{line}\n"
            linenumber += 1

    # Replace labels
    nextAdress = 16
    result = ""
    for line in codeclean.splitlines():
        if line[0] == "@":
            name = line[1:]

            # Skip if a number
            if name.isdigit():
                result += f"{line}\n"
                continue

            # Check if exists
            if name in Dsym:
                result += f"@{Dsym[name]}\n"
                continue

            Dsym[name] = nextAdress
            result += f"@{nextAdress}\n"
            nextAdress += 1
        else:
            result += f"{line}\n"

    return result.strip()


Dsym = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
}


if __name__ == "__main__":
    main()
