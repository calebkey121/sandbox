def solve(n, m, original_lines: tuple):
    lines = list(original_lines)
    joined = [] # To track the lenght of the lines we joing, for the solution
    for _ in range(m):
        # Get the shortest line information
        min_value = min(lines)
        min_index = lines.index(min_value)

        # Note the length of the line we joined for the solution
        joined.append(min_value)

        # Joined line is now one longer
        lines[min_index] += 1
    return joined

test_cases = {
    (3, 4, (3, 2, 5)): [2, 3, 3, 4],
}
for case, expected in test_cases.items():
    n, m, lines = case
    result = solve(n, m, lines)
    assert result == expected, f"Failed: solve{input} = {expected}, got {result}"
print("passed all test cases")
