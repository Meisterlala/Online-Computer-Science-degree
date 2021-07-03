#!/usr/bin/env python
"""Translates VMcode to Hack Assembly"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List
import time

from colorama import Fore, init

import translator.vmfile as vmfile
from translator.instructions import Call

# Has ugly output
MULTI_TRHEADED = False
# Output time taken
PERF_TEST = True


def main():
    """Main function"""

    start_timer = time.perf_counter()

    # init colorama Color output
    init()

    # Handle arguments
    files = arguments_parse()
    print(Fore.BLUE + "Translating:")
    for file in files:
        print(Fore.RESET + f"\t{file}")

    # Read Files
    vm_files = vmfile.filenames_to_objects(files)
    if MULTI_TRHEADED:
        main_pool = ThreadPoolExecutor()
        parse_mt(vm_files, main_pool)
        translate_mt(vm_files, main_pool)
        main_pool.shutdown(True)
    else:
        for vm_object in vm_files:
            vm_object.parse()
            vm_object.translate()

    # Combine Outputs
    translated = bootstrap_code()
    for vm_object in vm_files:
        translated.extend(vm_object.assembly)

    # Perf Output
    if PERF_TEST:
        print(Fore.MAGENTA +
              f"Translating took {round( time.perf_counter() - start_timer,5)}s")

    # Write output
    if os.path.isdir(sys.argv[1]):  # If folder
        dirname = os.path.relpath(sys.argv[1]) + os.path.sep
        out_endname = os.path.basename(
            sys.argv[1].rstrip("/").rstrip("\\")) + ".asm"
        out_filename = dirname + out_endname
    else:  # If file
        dirname = os.path.dirname(sys.argv[1]) + os.path.sep
        out_endname = os.path.splitext(
            os.path.basename(sys.argv[1]))[0] + ".asm"
        out_filename = dirname + out_endname
    print(Fore.BLUE + f"Writing {dirname}" + Fore.GREEN + out_endname)

    with open(out_filename, "w", newline=os.linesep) as out_file:
        out_file.write(output_string(translated, out_filename))

    sys.exit(0)


def translate_mt(vm_files, main_pool):
    """Translate Files"""
    translate_futures = []
    for vm_object in vm_files:
        translate_futures.append(main_pool.submit(vm_object.translate))
    wait(translate_futures)


def parse_mt(vm_files, main_pool):
    """Parse Files"""
    file_futures = []
    for vm_object in vm_files:
        file_futures.append(main_pool.submit(vm_object.parse))
    wait(file_futures)


def output_string(lines: List[str], filename):
    """Formats the Output before writing a File"""
    # Header
    outp = f"// Generated from {filename}\n"

    for out_line in lines:
        # Indent if not a label
        if out_line[0] == "(":  # label
            outp += "\n"
        elif out_line[0] == "/":
            outp += "\n\n"
        else:  # Code
            outp += "\n\t"
        outp += out_line
    return outp


def arguments_parse():
    """Parses the passed commandline Arguments

    Returns:
        List[str]: Files, which need to be compiled
    """
    if len(sys.argv) != 2:
        print("Usage: VMTranslator.py (Filename|Directory))")
        print(f"Given: {str(sys.argv)}")
        sys.exit(1)

    filename = str(sys.argv[1])

    files = []

    # Remove Trailing /
    filename = filename.rstrip("\\").rstrip("/")

    # If File
    if os.path.isfile(filename):
        if not os.path.splitext(filename)[1] == ".vm":
            print("Wrong File extenstion, please use .vm")
            sys.exit(1)
        files.append(filename)
        return files

    # If Folder
    if os.path.isdir(filename):
        for root, _, file_list in os.walk(filename):
            for file in file_list:
                if os.path.splitext(file)[1] == ".vm":
                    files.append(os.path.join(root, file))
        return files

    # Not File or Folder
    print(Fore.RED + "ERROR: No File or Directory provided")
    sys.exit(1)


def bootstrap_code():
    """Generates Code to Bootstrap the first function

        SP = 256
        Call Sys.init

    Returns:
        List[str]: Assembly OP Codes
    """
    retrun_value = ["// Bootstrap"]
    # SP = 256
    retrun_value.extend(["@256", "D=A", "@SP", "M=D"])
    # -1 to Stack pointers
    retrun_value.extend(["@0", "D=A",
                         "@LCL", "M=D-1",
                         "@ARG", "M=D-1",
                         "@THIS", "M=D-1",
                         "@THAT", "M=D-1"])
    # Call Sys.init
    call = Call("call Sys.init 0", "Sys.init", 0)
    call.parse()
    retrun_value.extend(call.translate())

    return retrun_value


if __name__ == "__main__":
    main()
