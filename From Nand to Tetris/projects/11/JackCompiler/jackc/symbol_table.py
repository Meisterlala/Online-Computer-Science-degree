""" a Symbol table containing names of variables """

from enum import Enum
from typing import Union


class SymbolTable():
    """ Contains class and sub level symbol tabels """
    class Entry():
        """ Represents a Entry in the Symbol table (without name) """
        class Kind(Enum):
            """ STATIC and FIELD are class scope
                VAR and ARG are sub scope """
            FIELD = 0
            STATIC = 1
            ARG = 2
            VAR = 3

        def __init__(self, j_type: str, kind: Kind, index: int) -> None:
            self.j_type = j_type
            self.kind = kind
            self.index = index

    def __init__(self, class_name) -> None:
        self.table_class: dict[str, SymbolTable.Entry] = {}
        self.table_sub: dict[str, SymbolTable.Entry] = {}
        self.class_name: str = class_name

    def add(self, name: str, j_type: str, kind: Entry.Kind):
        """ Add an entry to the table """

        new_index = self.var_count(kind) + 1
        new_entry = SymbolTable.Entry(j_type, kind, new_index)

        # if class scope
        if kind in (SymbolTable.Entry.Kind.FIELD, SymbolTable.Entry.Kind.STATIC):
            self.table_class[name] = new_entry
        else:  # sub scope
            self.table_sub[name] = new_entry

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

    def index_of(self, name) -> int:
        """ returns the index assigned to the named identifier """
        # Get Entry
        entry = self.get_entry(name)
        if entry is None:
            return 0
        return entry.index

    def var_count(self, kind: Entry.Kind):
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

        return None
