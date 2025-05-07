import os

# Readlines from given file
def get_file_data(filename: str, input_directory: str) -> list:
    path = os.path.join(input_directory, filename)
    with open(path) as file:
        lines = file.readlines()
        puzzle_input = [ line.strip() for line in lines ]      
    return puzzle_input

# Put the puzzle input into the form you want
def parse_input(puzzle_input: list):
    parsed_input = puzzle_input

    return parsed_input

# Solve the puzzle
def solve(puzzle_input: list):
    parsed_input = parse_input(puzzle_input)
    return 0

def main():
    input_directory = "input"
    input_filenames = [
        "test_input.txt",
        "puzzle_input.txt",
    ]
    for file in input_filenames:
        puzzle_input = get_file_data(file, input_directory)
        result = solve(puzzle_input)

        print(f"For input '{file}' got {result}")

if __name__ == "__main__":
    main()
