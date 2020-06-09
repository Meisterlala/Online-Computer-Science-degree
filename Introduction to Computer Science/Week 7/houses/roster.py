# TODO

from sys import argv
from cs50 import SQL

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Err")
    exit(1)

hname = argv[1]

students = db.execute("SELECT * FROM students WHERE house LIKE ? ORDER BY last ASC, first ASC", hname)

for s in students:
    print(s["first"], end=" ")
    if s["middle"]:
        print(s["middle"], end=" ")
    print(f"{s['last']}, born {s['birth']}")
