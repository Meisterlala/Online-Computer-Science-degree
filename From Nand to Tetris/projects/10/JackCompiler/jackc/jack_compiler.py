""" Main, it handels everything"""

import os
import sys

from jackc import tokens

from .jack_file import JackFile
from .tokenizer import Tokenizer


def main():
    """Entry Point of Module/Prorgamm
    """

    jack_files = handle_input(sys.argv)

    for file in jack_files:
        tokenizer = Tokenizer(file)
        print(file)
        token_list = tokenizer.tokenize()
        file.append(tokenizer.to_xml())

    for file in jack_files:
        file.save()


OUTPUT_FORMAT = ".xml"


def handle_input(argv) -> list[JackFile]:
    """ Creates an List of Files"""

    # If no argument
    if len(argv) != 2:
        print("Usage: JackC (Filename|Directory))")
        print(f"Given: {str(sys.argv[1:])}")
        sys.exit(1)

    # Check if File or dir
    file_or_dir = argv[1]
    is_file = os.path.isfile(file_or_dir)

    # if not a File or Folder
    if not is_file:
        if not os.path.isdir(file_or_dir):
            print("Not a valid File or Directory")
            sys.exit(1)

    # If File
    if is_file:
        filename = os.path.basename(file_or_dir)
        inp = os.path.abspath(file_or_dir)
        outp = os.path.abspath(os.path.dirname(
            file_or_dir) + os.path.sep + os.path.splitext(filename)[0] + OUTPUT_FORMAT)
        return [JackFile(filename, inp, outp)]
    else:  # Is Folder
        files = []
        for root, _, file_list in os.walk(file_or_dir):
            for file in file_list:
                if os.path.splitext(file)[1] == ".jack":
                    files.append(os.path.join(root, file))
        jack_files = []
        for file in files:
            filename = os.path.basename(file)
            inp = os.path.abspath(file)
            outp = os.path.abspath(os.path.dirname(
                file) + os.path.sep + os.path.splitext(filename)[0] + OUTPUT_FORMAT)
            jack_files.append(JackFile(filename, inp, outp))
        return jack_files
