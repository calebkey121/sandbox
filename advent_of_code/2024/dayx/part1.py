import os

def parse_input_files(input_filenames: list, input_directory: str) -> dict:
    parsed_input = {}
    for filename in input_filenames:
        path = os.path.join(input_directory, filename)
        with open(path) as file:
            lines = file.readlines()

            parsed_input[filename] = lines
                
    return parsed_input

def solve(input):
    return 0

def main():
    input_directory = "input"
    input_filenames = [
        "test_input.txt",
        "puzzle_input.txt",
    ]
    parsed_input = parse_input_files(input_filenames, input_directory)
    for test_case, parsed_input in parsed_input.items():
        result = solve(parsed_input)

        print(f"For input '{test_case}' got {result}")

if __name__ == "__main__":
    main()
