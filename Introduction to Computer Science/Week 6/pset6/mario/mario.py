


while True:
    try:
        h = int(input("Height: "))
        if 1 <= h <= 8:
            break
    except ValueError:
        continue

for i in range(h):
    print(" " * (h - 1 - i) + "#" * (i + 1))


