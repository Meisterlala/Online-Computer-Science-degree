""" a Symbol table containing names of variables """

from enum import Enum
from typing import Union


class SymbolTable():
    """ Contains class and sub level symbol tabels """
    class Entry():
        """ Represents a Entry in the Symbol table (without name) """
        class Kind(Enum):
            """ STATIC and FIELD are class scope
                LOCAL and ARG are sub scope """
            FIELD = 0
            STATIC = 1
            ARG = 2
            LOCAL = 3
            INVALID = 4

        def __init__(self, j_type: str, kind: Kind, index: int) -> None:
            self.j_type = j_type
            self.kind = kind
            self.index = index

    def __init__(self, class_name) -> None:
        self.table_class: "dict[str, SymbolTable.Entry]" = {}
        self.table_sub: "dict[str, SymbolTable.Entry]" = {}
        self.class_name: str = class_name
        self.label_index: int = -1

    def add(self, name: str, j_type: str, kind: Entry.Kind):
        """ Add an entry to the table """

        counted = self.var_count(kind)
        if counted == 0:
            # needed to start counting from 0
            new_index = 0
        else:
            new_index = counted

        new_entry = SymbolTable.Entry(j_type, kind, new_index)

        # if class scope
        if kind in (SymbolTable.Entry.Kind.FIELD, SymbolTable.Entry.Kind.STATIC):
            self.table_class[name] = new_entry
        else:  # sub scope
            self.table_sub[name] = new_entry

    def get_unique_index(self) -> str:
        """ Gets a class unique int for creating labels """
        self.label_index += 1
        index = str(self.label_index).zfill(8)
        return f"{self.class_name}_{index}"

    def reset_table_sub(self):
        """ Clears the Sub scope table """
        self.table_sub.clear()

    def kind_of(self, name: str) -> Union[Entry.Kind, None]:
        """ returns Kind or None """
        # Get Entry
        entry = self.get_entry(name)
        if entry is None:
            return None

        return entry.kind

    def j_type_of(self, name: str) -> Union[str, None]:
        """ returns the j_type or None"""
        # Get entry
        entry = self.get_entry(name)
        if entry is None:
            return None
        return entry.j_type

    def index_of(self, name) -> int:
        """ returns the index assigned to the named identifier or -1"""
        # Get Entry
        entry = self.get_entry(name)
        if entry is None:
            return -1
        return entry.index

    def var_count(self, kind: Entry.Kind) -> int:
        """ Returns the number of variables with a given type """
        # Select which table to search based on Entry.Kind
        if kind in (SymbolTable.Entry.Kind.FIELD, SymbolTable.Entry.Kind.STATIC):
            table = self.table_class
        else:
            table = self.table_sub

        # Count
        count = 0
        for entry in table.values():
            if entry.kind == kind:
                count += 1
        return count

    def get_entry(self, name) -> Union[Entry, None]:
        """ returns None or Entry if found """
        # if in sub table
        sub_entry = self.table_sub.get(name, None)
        if sub_entry is not None:
            return sub_entry

        # if in class table
        class_entry = self.table_class.get(name, None)
        if class_entry is not None:
            return class_entry

        # Error, unknown var
        return None
