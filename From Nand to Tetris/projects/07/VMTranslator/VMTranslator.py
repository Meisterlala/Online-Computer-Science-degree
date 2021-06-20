#!/usr/bin/env python
import sys
import os.path
from typing import List
from concurrent.futures import ProcessPoolExecutor, wait

import Instructions as op
import Parser


def main():

    # Handle arguments
    arg = ArgumentsCheck()
    filename = arg[0]

    # Parse
    parsed = Parser.Parse(filename)

    # Translate
    translated: List[str] = Parser.Translate(parsed)

    # Write output
    outFilename = os.path.splitext(filename)[0] + ".asm"
    print(f"Writing {outFilename}")
    out = open(outFilename, "w")
    out.write(OutputString(translated, outFilename))
    out.close()

    sys.exit(0)


def OutputString(lines: List[str], filename):
    # Header
    outp = f"// Generated from {filename}"

    for outLine in lines:
        # Indent if not a label
        if outLine[0] == "(":  # label
            outp += "\r\n"
        elif outLine[0] == "/":
            outp += "\r\n\r\n\t"
        else:    # Code
            outp += "\r\n\t"
        outp += outLine
    return outp


def ArgumentsCheck():
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
        sys.exit(1)

    return (filename,)


if __name__ == "__main__":
    main()
