import glob
import subprocess
import os.path
import time

version = "1.1"
# Time Difference between PDF and NB in sec
maxTimeDifference = 900

# Check if every Notebook is converted to PDF
allAsPdf = True
nbs = glob.glob("Calculus/*/*.nb")
pdfs = glob.glob("Calculus/*/*.pdf")
for nbfile in nbs:
    nameAsPdf = nbfile.replace(".nb", ".pdf")
    if nameAsPdf in pdfs:
        mTimeNb = os.path.getmtime(nbfile)
        mTimePdf = os.path.getmtime(nameAsPdf)
        diff = mTimeNb - mTimePdf
        if diff > maxTimeDifference:
            print(nameAsPdf + " needs to be updated")
            allAsPdf = False
    else:
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

# Upload
subprocess.run(["git", "push"])

# Don't Autoclose
time.sleep(3)
