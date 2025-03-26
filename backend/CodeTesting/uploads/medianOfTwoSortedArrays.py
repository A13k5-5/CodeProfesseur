def answer(nums1, nums2):
    i = j = 0
    curLen = 0
    n = len(nums1) + len(nums2)
    median = n / 2
    curArr = []
    while curLen < n:
        if i >= len(nums1):
            curArr.append(nums2[j])
            j += 1
        elif j >= len(nums2):
            curArr.append(nums1[i])
            i += 1
        elif nums1[i] < nums2[j]:
            curArr.append(nums1[i])
            i += 1
        else:
            curArr.append(nums2[j])
            j += 1
        curLen += 1
    # Median of two vals
    if n % 2 == 0:
        return (curArr[n // 2] + curArr[n // 2 - 1]) / 2
    return curArr[n // 2]


if __name__ == "__main2__":
    print(answer([1, 2], [3, 4]))  # 2.5
    print(answer([1, 1], [1, 1]))  # 1.0


import random
import json

# test cases
# edge cases:
# [1], []
# [], [1]
# [1], [1]
# different size
# odd/even length

# Generate test cases
if __name__ == "__main__":
    tests = [([1], []), ([], [1]), ([1], [1])]
    # different size
    for _ in range(10):
        lst1 = []
        lst2 = []
        size1 = random.randint(0, 10**3)
        size2 = random.randint(0, 10**3)

        for i in range(size1):
            lst1.append(random.randint(0, 10**5))

        for i in range(size2):
            lst2.append(random.randint(0, 10**5))

        lst1.sort()
        lst2.sort()
        tests.append((lst1, lst2))

    with open("medianOfTwoSortedListsTestCases.json", "w") as file:
        file.write(json.dumps(tests))

    # generate expected outputs
    outputs = []
    for test in tests:
        outputs.append([answer(*test)])

    with open("medianOfTwoSortedListsOutputs.json", "w") as file:
        file.write(json.dumps(outputs))

    print(outputs)
