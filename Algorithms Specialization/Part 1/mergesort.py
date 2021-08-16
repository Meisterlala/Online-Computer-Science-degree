from time import time_ns


def main():
    # Read Input
    elements = input("Enter unsorted Array:\n")
    unsorted = list(map(int, elements.split()))

    # Time MergeSort
    t1 = time_ns()
    sorted = mergesort(unsorted)
    t2 = time_ns()

    # Output
    print(sorted)
    print(f"Sorting took {t2-t1}ns")


def mergesort(arr: list[int]) -> list[int]:
    # Base case
    if len(arr) == 2:
        if arr[0] < arr[1]:
            return arr
        else:
            return [arr[1], arr[0]]

    if len(arr) <= 1:
        return arr

    # Recursivly sort
    split = int(len(arr)/2)
    left = mergesort(arr[0:split])
    right = mergesort(arr[split:])

    # Merge
    left_index = 0  # Index in left
    right_index = 0  # Index in right
    for k in range(len(arr)):
        # Check end of Range
        left_outofbound = left_index > (len(left) - 1)
        right_outofbound = right_index > (len(right) - 1)
        if left_outofbound:
            arr[k] = right[right_index]
            right_index += 1
            continue
        if right_outofbound:
            arr[k] = left[left_index]
            left_index += 1
            continue
        if left_outofbound and right_outofbound:
            break

        # Compare
        if left[left_index] < right[right_index]:
            arr[k] = left[left_index]
            left_index += 1
        else:  # left[i] > right[j]
            arr[k] = right[right_index]
            right_index += 1
    return arr


if __name__ == "__main__":
    main()
