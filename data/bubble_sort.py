def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def main():
    arr = [5, 2, 9, 1, 5, 6]
    sorted_arr = bubble_sort(arr)
    print(sorted_arr)


if __name__ == "__main__":
    main()