
from .symbol_table import SymbolTable


def test_simple():

    table = SymbolTable()
    table.add("x", "int", SymbolTable.Entry.Kind.STATIC)
    assert len(table.table_class) == 1
    table.add("y", "int", SymbolTable.Entry.Kind.VAR)
    assert len(table.table_class) == 1
    assert len(table.table_sub) == 1

    assert table.kind_of("x") == SymbolTable.Entry.Kind.STATIC
    assert table.kind_of("y") == SymbolTable.Entry.Kind.VAR
