from time import time_ns
import sys


def main():

    if len(sys.argv) == 2:
        path = sys.argv[1]
        array = []
        with open(path, "r") as file:
            lines = file.readlines()
            array = list(map(int, lines))
        pass
    else:
        inp = input("Input array: \n")
        array = list(map(int, inp.split()))

    time_start = time_ns()
    count = inversions(array)
    elapsed_time = time_ns() - time_start
    print("Number of Inversions: " + str(count))

    print(f"Execution took: {elapsed_time // 1_000_000}ms")


def inversions(array):
    """Count the number of Inversions in Array
    Runtime O(n*log(n))"""
    sorted, count = __inversions_sorted(array)

    return count


def __inversions_sorted(array):
    """Count the number of Inversions in Array
    Runtime O(n*log(n))"""
    length = len(array)
    # Base case
    if length <= 1:
        return array, 0

    left, left_count = __inversions_sorted(
        array[: round(length / 2)]
    )  # Count left half
    right, right_count = __inversions_sorted(
        array[round(length / 2) :]
    )  # Count right half
    sorted, split_count = __split_inversions(left, right)

    return sorted, left_count + right_count + split_count


def __split_inversions(left, right):
    """Count split inversion with a mergesort like algotithm"""
    # Merge
    sorted = []
    splits = 0
    left_index = 0  # Index in left
    right_index = 0  # Index in right
    for k in range(len(left) + len(right)):
        # Check end of Range
        left_outofbound = left_index > (len(left) - 1)
        right_outofbound = right_index > (len(right) - 1)
        if left_outofbound:
            sorted.append(right[right_index])
            right_index += 1
            continue
        if right_outofbound:
            sorted.append(left[left_index])
            left_index += 1
            continue
        if left_outofbound and right_outofbound:
            break

        # Compare
        if left[left_index] < right[right_index]:
            sorted.append(left[left_index])
            left_index += 1
        else:  # left[i] > right[j]
            sorted.append(right[right_index])
            splits += len(left) - left_index
            right_index += 1
    return sorted, splits


if __name__ == "__main__":
    main()
