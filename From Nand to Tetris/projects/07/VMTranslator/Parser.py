from io import TextIOWrapper
from typing import List
import Instructions as op
import os.path
from concurrent.futures import ProcessPoolExecutor, wait


activeFileName = ""


def Translate(ops: List[op.Operation]) -> List[str]:
    """ Translates Operations to Heck asm """
    print("Translating")

    # Multi threading
    pool = ProcessPoolExecutor()
    futures = []

    for op in ops:
        futures.append(pool.submit(op.translate))

    wait(futures)
    translated: List[str] = []
    for future in futures:
        result = future.result()
        translated.extend(result)

    return translated


def Parse(filename: str) -> List[op.Operation]:
    """Parses a file to a List of Instructions"""

    # Open File
    file = open(filename, "r")

    # Get real file name
    index = filename.rfind("/")
    if index == -1:
        index = filename.rfind("\\")
    if index == -1:
        activeFile = filename
    else:
        activeFile = filename[index + 1:len(filename)]
    activeFileName = activeFile.split(sep=".")[0]

    print(f"Parsing {activeFile}")

    # Multi threading
    pool = ProcessPoolExecutor()
    futures = []

    lines = file.readlines()

    lineNumber = 0
    for line in lines:
        futures.append(pool.submit(_ParseLine, line, lineNumber))
        lineNumber += 1

    wait(futures)
    successfullyParsed = []
    # Remove Invalid Parsings
    for future in futures:
        result = future.result()
        if isinstance(result, op.Invalid):
            continue
        successfullyParsed.append(result)

    print(f"Ignored {len(futures) - len(successfullyParsed)} lines")

    file.close()

    return successfullyParsed


def _PreParse(line: str) -> str:
    """ Remove comments and new line """
    line = line.rstrip("\n")

    commentIndex = line.find("/")

    # no comment found
    if commentIndex == - 1:
        return line

    # truncate
    return line[0:commentIndex]


def _ParseLine(line: str, lineNumber: int):
    preParsed = _PreParse(line)

    if len(line) == 0:
        return op.Invalid()

    stack = op.Stack(preParsed, activeFileName, lineNumber)
    if stack.parse():
        return stack

    arithmetic = op.Arithmetic(preParsed, activeFileName, lineNumber)
    if arithmetic.parse():
        return arithmetic

    return op.Invalid()
