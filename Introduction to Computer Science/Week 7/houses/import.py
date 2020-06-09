# TODO

from sys import argv
from cs50 import SQL
import csv



db = SQL("sqlite:///students.db")
db.execute("DELETE FROM students")

if len(argv) != 2:
    print("Err")
    exit(1)

with open(argv[1], "r") as csvFile:
    csvReader = csv.DictReader(csvFile)

    r = 0
    for row in csvReader:       
        spli = row["name"].split()

        nf = spli[0]
        if len(spli) == 2:
            nm = None
            nl = spli[1]
        else:
            nm = spli[1]
            nl = spli[2]
            
        db.execute("INSERT INTO students (id, first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?, ?)", r, nf, nm, nl, row["house"], row["birth"])
        r += 1


