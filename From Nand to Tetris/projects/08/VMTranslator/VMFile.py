from concurrent.futures.thread import ThreadPoolExecutor
from typing import List
import os
from concurrent.futures import ProcessPoolExecutor, wait
import Instructions as op
from colorama import Fore


def FilenamesToObjects(filenames: List[str]):

    VMFiles: List[VMFile] = []
    for file in filenames:
        VMFiles.append(VMFile(file))

    # Read all File Contents
    for obj in VMFiles:
        obj.ReadFile()

    return VMFiles


class VMFile():
    uid = 0

    def __init__(self, filename: str) -> None:
        self.filePath = filename
        pass

    def ReadFile(self):
        # Read all lines
        with open(self.filePath, "r") as file:
            self.fileContent = file.readlines()

        # Get RealFileName
        self.fileName = os.path.basename(self.filePath)

    def Parse(self):
        print(f"Parsing {self.fileName}")

        # Multi threading
        pool = ProcessPoolExecutor()
        futures = []

        # start Threads
        lineNumber = 0
        for line in self.fileContent:
            uid = VMFile._getUID()
            fileNameNoExtension = os.path.splitext(self.fileName)[0]
            futures.append(pool.submit(
                _ParseLine, line, uid, fileNameNoExtension))
            lineNumber += 1

        # Filter Invalids
        wait(futures)
        self.OPs = []
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
            self.OPs.append(result)

        # Print for Debug
        if commentCounter > 0:
            print(f"\tIgnoring {commentCounter} comments/empty lines")
        if invalidCounter > 0:
            print(Fore.YELLOW + f"\tWARNING: {invalidCounter} invalid lines")

    def Translate(self):

        # Multi threading
        pool = ProcessPoolExecutor()
        futures = []

        # Start Thread to translate
        for op in self.OPs:
            futures.append(pool.submit(op.translate))

        # Put results in list
        wait(futures)
        self.assembly: List[str] = []
        for future in futures:
            result = future.result()
            self.assembly.extend(result)

        print(Fore.GREEN +
              f"\tTranslated to {len(self.assembly)} OPs")

    @staticmethod
    def _getUID():
        VMFile.uid += 1
        return VMFile.uid


def _PreParse(line: str) -> str:
    """ Remove comments and new line """
    line = line.rstrip("\n")

    commentIndex = line.find("/")

    # no comment found
    if commentIndex == - 1:
        return line

    # truncate
    return line[0:commentIndex]


def _ParseLine(line: str, jumpID: int, FileName: str):
    preParsed = _PreParse(line)

    if len(preParsed) == 0:
        return op.Comment()

    stack = op.Stack(preParsed, FileName, jumpID)
    if stack.parse():
        return stack

    arithmetic = op.Arithmetic(preParsed, FileName, jumpID)
    if arithmetic.parse():
        return arithmetic

    goto = op.GoTo(preParsed, FileName, jumpID)
    if goto.parse():
        return goto

    label = op.Label(preParsed, FileName, jumpID)
    if label.parse():
        return label

    return op.Invalid()
