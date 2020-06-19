import glob
import subprocess

allAsPdf = True
version = "1.0"

nbs = glob.glob("Calculus/*/*.nb")
pdfs = glob.glob("Calculus/*/*.pdf")
for nbfile in nbs:
    nameAsPdf = nbfile.replace(".nb", ".pdf")
    if nameAsPdf not in pdfs:
        print(nameAsPdf + " was not found")
        allAsPdf = False

if not allAsPdf:
    print("Please save notebooks as PDF's")
    input()
    exit(1)

subprocess.run(["git", "pull"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "status"])

message = input("Commit Message: ")

subprocess.run(["git", "commit", "-a", "-m", message,
                "-m", "from script v" + version])
