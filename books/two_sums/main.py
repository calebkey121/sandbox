test_cases = {
    ((tuple([2, 7, 11, 15]), 9)): [0, 1],
    ((tuple([-1, -2, -3, -4, -5]), -8)): [2, 4],
    ((tuple([3, 0, -2, 4]), 1)): [0, 2],
    ((tuple([10, 5, 3, 2]), 8)): [1, 2],
    ((tuple([3, 3]), 6)): [0, 1],
}

def two_sum(nums, target) -> list:
    comps = {}
    for i, num in enumerate(nums):
        comp = target - num
        comps[comp] = i
        if num in comps:
            return [ comps[num], i ]
    return None

for case, expected_output in test_cases.items():
    nums, target = case
    result = two_sum(nums, target)
    assert result == expected_output, f"Incorrect: got {result}, expected {expected_output}"
    print("pass")
