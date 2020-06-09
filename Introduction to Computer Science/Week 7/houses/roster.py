# TODO

from sys import argv
from cs50 import SQL
import csv



db = SQL("sqlite:///students.db")

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
            nm = ""
            nl = spli[2]
        else:
            nm = spli[2]
            nl = spli[3]
            
        db.execute("INSTERT INTO students (id first middle last house birth) VALUES (? ? ? ? ? ?)", 
                        r, spli[0], spli[1], spli[2], row["house"], row["birth"])
        r += 1


