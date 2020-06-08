


text = input("Text: ")
wordc = 1
sentencec = 0
letterc = 0

for c in text:
    if c == " ":
        wordc += 1
    elif c in [".", "!", "?"]:
        sentencec += 1
    elif c.isalpha():
        letterc +=1


ln = float(letterc) / float(wordc) * 100.0
sn = float(sentencec) / float(wordc) * 100.0

grade = int(round(0.0588 * ln - 0.296 * sn - 15.8,0))


if grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {grade}")


# print(f"words:{wordc}  sentence:{sentencec}   letterc:{letterc}")