#!/usr/bin/env python
"""Translates VMcode to Hack Assembly"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List

from colorama import Fore, init

import translator.vmfile as vmfile
import translator.function as fc


def main():
    """Main function"""

    # init colorama Color output
    init()

    # Handle arguments
    files = arguments_parse()
    print("Translating:")
    for file in files:
        print(f"\t{file}")

    # Read Files
    vm_files = vmfile.filenames_to_objects(files)

    # Multi threading
    main_pool = ThreadPoolExecutor()

    # Parse Files Multi threaded
    file_futures = []
    for vm_object in vm_files:
        file_futures.append(main_pool.submit(vm_object.parse))
    wait(file_futures)

    # Translate Files Multi threaded
    translate_futures = []
    for vm_object in vm_files:
        translate_futures.append(main_pool.submit(vm_object.translate))
    wait(translate_futures)
    main_pool.shutdown(True)

    # Combine Outputs
    translated = bootstrap_code()
    for vm_object in vm_files:
        translated.extend(vm_object.assembly)

    # Write output
    if os.path.isdir(sys.argv[1]):  # If folder
        dirname = os.path.relpath(sys.argv[1]) + os.path.sep
        out_filename = dirname + \
            os.path.basename(sys.argv[1].rstrip("/").rstrip("\\")) + ".asm"
    else:  # If file
        dirname = os.path.dirname(sys.argv[1]) + os.path.sep
        out_filename = dirname + \
            os.path.splitext(os.path.basename(sys.argv[1]))[0] + ".asm"
    print(f"Writing {out_filename}")

    with open(out_filename, "w", newline=os.linesep) as out_file:
        out_file.write(output_string(translated, out_filename))

    sys.exit(0)


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
    call = fc.Call("call Sys.init 0", "Sys.init", 0)
    call.parse()
    retrun_value.extend(call.translate())

    return retrun_value


if __name__ == "__main__":
    main()
