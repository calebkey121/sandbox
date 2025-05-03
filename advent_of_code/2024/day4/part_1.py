def check(check_string: str, search_word: str) -> bool:
    if check_string == search_word or check_string == search_word[::-1]: # forwards or backwards
        return True
    return False

def word_count(puzzle_input: str, search_word: str) -> int:
    puzzle_input = puzzle_input.strip().split()

    count = 0
    num_rows = len(puzzle_input)
    num_cols = len(puzzle_input[0])

    print(puzzle_input)
    for row, line in enumerate(puzzle_input):
        for col, char in enumerate(line):
            horizontal = [ i for i in puzzle_input[row][col:col+4] ]
            vertical = [ row[col] for row in puzzle_input[row:row+4] ]
            diagonal_right = [ puzzle_input[row + i][col + i] for i, _ in enumerate(puzzle_input[row:row+4]) if col + i < num_cols ]
            diagonal_left = [ puzzle_input[row + i][col - i] for i, _ in enumerate(puzzle_input[row:row+4]) if col - i >= 0 ]

            # Convert each from list to str
            horizontal = "".join(horizontal)
            vertical = "".join(vertical)
            diagonal_right = "".join(diagonal_right)  
            diagonal_left = "".join(diagonal_left)

            # Check each of the directions to see if they match
            if check(horizontal, search_word):
                count += 1
                # print(f"Found horizontal match '{horizontal}' at ({row}, {col})")
            if check(vertical, search_word):
                count += 1
                # print(f"Found vertical match '{vertical}' at ({row}, {col})")
            if check(diagonal_right, search_word):
                count += 1
                # print(f"Found diagonal_right match '{diagonal_right}' at ({row}, {col})")
            if check(diagonal_left, search_word):
                count += 1
                # print(f"Found diagonal_left match '{diagonal_left}' at ({row}, {col})")
            
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
    search_word = "XMAS" # not worried about case rn
    count = word_count(puzzle_input, search_word)
    expected = 18
    assert count == expected, f"Test Failed: expected {expected}, got {count}"

    puzzle_input = read_input("advent_of_code/2024/day4/input.txt")
    count = word_count('\n'.join(puzzle_input), "XMAS")
    print(f"Word count for puzzle input: {count}")


if __name__ == "__main__":
    main()
