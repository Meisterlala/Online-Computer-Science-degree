""" Handels a Single File for compiling """
import os
from concurrent.futures import ProcessPoolExecutor, wait
from typing import List

from colorama import Fore

import translator.instructions as op
import translator.function as fc


def filenames_to_objects(filenames: List[str]):
    """Takes a List of Filenames and generates vm_file objects

    Args:
        filenames (List[str]): input files

    Returns:
        List[vm_file]: objects
    """
    vm_files: List[VMFile] = []
    for file in filenames:
        vm_files.append(VMFile(file))

    # Read all File Contents
    for obj in vm_files:
        obj.read_file()

    return vm_files


class VMFile():
    """A File, containing VM Code """
    uid = 0

    def __init__(self, filename: str) -> None:
        self.file_path = filename
        self.ops = []
        self.file_name = ""
        self.file_content = []
        self.assembly = []

    def read_file(self):
        """Read File Contents"""
        # Read all lines
        with open(self.file_path, "r") as file:
            self.file_content = file.readlines()

        # Get RealFileName
        self.file_name = os.path.basename(self.file_path)

    def parse(self):
        """Parse File Contents"""
        print(f"Parsing {self.file_name}")

        # Multi threading
        pool = ProcessPoolExecutor()
        futures = []

        # start Threads
        line_number = 0
        for line in self.file_content:
            uid = VMFile._get_uid()
            file_name_no_extension = os.path.splitext(self.file_name)[0]
            futures.append(pool.submit(
                _parse_line, line, uid, file_name_no_extension))
            line_number += 1

        # Filter Invalids
        wait(futures)
        invalid_counter = 0
        comment_counter = 0

        # Put results in list
        for future in futures:
            result = future.result()
            # Remove invalid lines
            if isinstance(result, op.Invalid):
                invalid_counter += 1
                continue
            # Remove comments
            if isinstance(result, op.Comment):
                comment_counter += 1
                continue
            self.ops.append(result)

        # Print for Debug
        if comment_counter > 0:
            print(f"\tIgnoring {comment_counter} comments/empty lines")
        if invalid_counter > 0:
            print(Fore.YELLOW + f"\tWARNING: {invalid_counter} invalid lines")

    def translate(self):
        """ Translate Parsed OP codes to Assembly """
        # Multi threading
        pool = ProcessPoolExecutor()
        futures = []

        # Start Thread to translate
        for op_code in self.ops:
            futures.append(pool.submit(op_code.translate))

        # Put results in list
        wait(futures)
        self.assembly: List[str] = []
        for future in futures:
            result = future.result()
            self.assembly.extend(result)

        print(Fore.GREEN +
              f"\tTranslated to {len(self.assembly)} OPs")

    @staticmethod
    def _get_uid():
        VMFile.uid += 1
        return VMFile.uid


def _pre_parse(line: str) -> str:
    """ Remove comments and new line """
    line = line.rstrip("\n")

    comment_index = line.find("/")

    # no comment found
    if comment_index == - 1:
        return line

    # truncate
    return line[0:comment_index]


def _parse_line(line: str, jump_id: int, file_name: str):
    pre_parsed = _pre_parse(line)

    if len(pre_parsed) == 0:
        return op.Comment()

    stack = op.Stack(pre_parsed, file_name, jump_id)
    if stack.parse():
        return stack

    arithmetic = op.Arithmetic(pre_parsed, file_name, jump_id)
    if arithmetic.parse():
        return arithmetic

    goto = op.GoTo(pre_parsed, file_name, jump_id)
    if goto.parse():
        return goto

    label = op.Label(pre_parsed, file_name, jump_id)
    if label.parse():
        return label

    function = fc.Function(pre_parsed, file_name, jump_id)
    if function.parse():
        return function

    return_op = fc.Return(pre_parsed, file_name, jump_id)
    if return_op.parse():
        return return_op

    return op.Invalid()
