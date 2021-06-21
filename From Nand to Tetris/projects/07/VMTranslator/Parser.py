from typing import List
import Instructions as op
from concurrent.futures import ProcessPoolExecutor, wait
from colorama import Fore


def Translate(ops: List[op.Operation]) -> List[str]:
    """ Translates Operations to Heck asm """
    print("Translating")

    # Multi threading
    pool = ProcessPoolExecutor()
    futures = []

    # Start Thread to translate
    for op in ops:
        futures.append(pool.submit(op.translate))

    # Put results in list
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

    # start Threads
    lineNumber = 0
    for line in lines:
        futures.append(pool.submit(_ParseLine, line,
                                   lineNumber, activeFileName))
        lineNumber += 1

    wait(futures)
    successfullyParsed = []
    invalidCounter = 0
    commentCounter = 0
    # Put results in list
    for future in futures:
        result = future.result()
        # Remove invalid lines
        if isinstance(result, op.Invalid):
            invalidCounter += 1
            continue
        # Remove comments
        if isinstance(result, op.Comment):
            commentCounter += 1
            continue
        successfullyParsed.append(result)

    # Print for Debug
    if commentCounter > 0:
        print(f"Ignoring {commentCounter} comments")
    if invalidCounter > 0:
        print(Fore.YELLOW + f"WARNING: {invalidCounter} invalid lines")

    # Close File
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


def _ParseLine(line: str, lineNumber: int, FileName: str):
    preParsed = _PreParse(line)

    if len(preParsed) == 0:
        return op.Comment()

    stack = op.Stack(preParsed, FileName, lineNumber)
    if stack.parse():
        return stack

    arithmetic = op.Arithmetic(preParsed, FileName, lineNumber)
    if arithmetic.parse():
        return arithmetic

    return op.Invalid()
