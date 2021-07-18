""" Moduale for Describing different Files"""

from os import path

from colorama import Fore


class JackFile():
    """ A Class Describing a File"""

    def __init__(self, filename, inp, outp) -> None:
        self.filename = filename
        self.input_path = inp
        self.output_path = outp
        self.compiled_content = ["some", "thisng"]

    def __repr__(self) -> str:
        return_value = f"From {self.input_path} to {self.output_path}"
        if len(self.compiled_content) > 0:
            return_value += "\n"
            return_value += "\n".join(self.compiled_content)
        return return_value

    def append(self, content):
        """Append to new file contend

        Args:
            content (List[str]): List of text to be appended
        """
        self.compiled_content.extend(content)

    def save(self):
        """Save the File to Disk
        """

        rel_path = path.relpath(self.output_path)
        print(Fore.GREEN +
              f"Writing {rel_path} with {len(self.compiled_content)} Lines")

        with open(self.output_path, "w") as out_file:
            out_file.writelines(self.compiled_content)
