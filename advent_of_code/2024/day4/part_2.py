def check(check_string: str, search_word: str) -> bool:
    if check_string == search_word or check_string == search_word[::-1]: # forwards or backwards
        return True
    return False

def x_mas_count(puzzle_input: str) -> int:
    search_word = "MAS" # lets hard code
    search_length = len(search_word)
    investigate = [(0,1), (2,1)]
    puzzle_input = puzzle_input.strip().split()

    count = 0
    num_rows = len(puzzle_input)
    num_cols = len(puzzle_input[0])

    print(puzzle_input)
    for row, line in enumerate(puzzle_input):
        for col, char in enumerate(line):
            diagonal_right = [ puzzle_input[row + i][col + i] for i, _ in enumerate(puzzle_input[row:row + search_length]) if col + i < num_cols ]
            diagonal_left = [ puzzle_input[row + i][col + 2 - i] for i, _ in enumerate(puzzle_input[row:row + search_length]) if col + 2 - i >= 0 and col + 2 - i < num_cols ] # plus 2 for the required cross structure

            # Convert each from list to str
            diagonal_right = "".join(diagonal_right)  
            diagonal_left = "".join(diagonal_left)
            if (row, col) in investigate:
                print(f"Investigate: [right: {diagonal_right}, left: {diagonal_left}] at ({row}, {col})")

            # Check each of the directions to see if they match
            if check(diagonal_right, search_word) and check(diagonal_left, search_word):
                count += 1
                print(f"Found cross match [right: {diagonal_right}, left: {diagonal_left}] at ({row}, {col})")
            
    return count

# return puzzle input
def read_input(filename: str) -> str:
    with open(filename) as f:
        return f.readlines()

def main():
    puzzle_input = """
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """
    count = x_mas_count(puzzle_input)
    expected = 9
    assert count == expected, f"Test Failed: expected {expected}, got {count}"

    puzzle_input = read_input("advent_of_code/2024/day4/input.txt")
    count = x_mas_count('\n'.join(puzzle_input))
    print(f"Word count for puzzle input: {count}")


if __name__ == "__main__":
    main()
