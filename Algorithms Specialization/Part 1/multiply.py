def main():
    a = int(input("1st factor: "))
    b = int(input("2nd factor: "))

    c = multiply(a, b)
    print("Calculated:     " + str(c))
    d = a * b
    print("Correct Answer: " + str(d))


def multiply(x, y):
    """Runtime: O(n^1.58)"""
    if x < 10 and y < 10:
        return x * y

    num1_len = len(str(x))
    num2_len = len(str(y))

    n = max(num1_len, num2_len)
    nby2 = round(n / 2)

    num1 = x // (10 ** nby2)
    rem1 = x % (10 ** nby2)

    num2 = y // (10 ** nby2)
    rem2 = y % (10 ** nby2)

    ac = multiply(num1, num2)
    bd = multiply(rem1, rem2)
    ad_plus_bc = multiply(num1 + rem1, num2 + rem2) - ac - bd

    return (10 ** (2 * nby2)) * ac + (10 ** nby2) * ad_plus_bc + bd


if __name__ == "__main__":
    main()
