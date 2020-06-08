from cs50 import get_float

while True:
    try:
        h = int(get_float("Change owed: ") * 100)
        if 0 <= h:
            break
    except ValueError:
        continue

count = 0


for val in [25, 10, 5, 1]:
    while h >= val:
        h -= val
        count += 1
print(count)