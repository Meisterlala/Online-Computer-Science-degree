from sys import argv
import csv

def main():
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    with open(argv[1]) as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_count = 0
        nomatch = True
        with open(argv[2]) as secfile:
            content = secfile.read()
            values = {}        
            firstRow = True;   
            for row in csvreader:
                match = True
                for sec in row:
                    if sec == "name":
                        continue
                    if firstRow:
                        values[sec] = str(rep(sec, content))
                    if values[sec] != row[sec]:
                        match = False
                if match:
                    print(row["name"])
                    exit(0)
                    nomatch = False     
                firstRow = False
    if nomatch:        
        print("No match")               



def rep(sec, toSearch):
    max = 0
    for i in range(int(len(toSearch) / len(sec))):
        if (sec * i) in toSearch and i > max:
            max = i
    return max

main()