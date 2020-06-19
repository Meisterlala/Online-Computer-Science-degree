import glob
import subprocess

version = "1.0"

# Check if every Notebook is converted to PDF
allAsPdf = True
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

# Update git
subprocess.run(["git", "pull"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "status"])

message = input("Commit Message: ")

# Commit
subprocess.run(["git", "commit", "-a", "-m", message,
                "-m", "from script v" + version])

# Don't Autoclose
input()
