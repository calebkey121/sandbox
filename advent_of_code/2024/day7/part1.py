import os
import operator

# Readlines from given file
def get_file_data(filename: str, input_directory: str) -> list:
    path = os.path.join(input_directory, filename)
    with open(path) as file:
        lines = file.readlines()
        puzzle_input = [ line.strip() for line in lines ]      
    return puzzle_input

# Put the puzzle input into the form you want
def parse_input(puzzle_input: list):
    parsed_input = []
    for line in puzzle_input:
        line = line.split()
        # take the last char off the first string of the line we just added
        line[0] = line[0][:-1]
        parsed_input.append([int(x) for x in line])

    return parsed_input

def compute(operators, operands) -> int:
    total = operands[0]
    for i, operator in enumerate(operators):
        total = operator(total, operands[i + 1])
    return total

# Solve the puzzle
def solve(puzzle_input: list):
    parsed_input = parse_input(puzzle_input)
    for line in parsed_input:
        solution = line[0]
        operands = line[1:]
        operators = [ operator.add ] * (len(operands) - 1)
        i = 0
        while compute(operators, operands) < solution: # keep adding multipliers so we can refine our search
            operators[i] = operator.mul
            i += 1
        
        pass
    return 0

def main():
    input_directory = "input"
    input_filenames = [
        "test_input.txt",
        # "puzzle_input.txt",
    ]
    for file in input_filenames:
        puzzle_input = get_file_data(file, input_directory)
        result = solve(puzzle_input)

        print(f"For input '{file}' got {result}")

if __name__ == "__main__":
    main()
