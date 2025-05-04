def parse_input_files(input_filenames: list) -> dict:
    parsed_input = {}
    for filename in input_filenames:
        parsed_input[filename] = {}
        with open(filename) as file:
            lines = file.readlines()
            rules = []
            updates = []
            for line in lines:
                if '|' in line: # page ordering rules
                    rules.append(line.rstrip())
                elif line.strip() != "": # update (not a blank line)
                    updates.append(line.rstrip())
            parsed_input[filename]["rules"] = rules
            parsed_input[filename]["updates"] = updates
                
    return parsed_input

def check_order(rules: list, updates: list) -> list:
    # return list of incorrect updates
    correct_updates = []
    incorrect_updates = []

    # lets make a hash table for rules where the key is the second number and the value is the list of numbers it must not appear after
    rules_table = {}
    for rule in rules:
        before, after = [ int(a) for a in rule.split('|') ]

        # make an entry for 'after' if it doesn't exist
        if before not in rules_table:
            rules_table[before] = set()
        rules_table[before].add(after)
    
    # Now we have our rules table, we can loop through update, check the current number and compare its table entry with numbers weve encountered
    for update in updates:
        correct = True
        update = [ int(a) for a in update.split(',')]
        encountered = set()
        for num in update:
            incompatible_nums = rules_table.get(num) # find the numbers we can't have already encountered
            # see if they intersect
            if incompatible_nums and (encountered & incompatible_nums):
                # intersection
                correct = False
                incorrect_updates.append(update)
                break
            encountered.add(num)
        if correct:
            correct_updates.append(update)

    return correct_updates

# sum of the middle number of a list of updates
def middle_num_sum(updates: list) -> int:
    # problem doesn't state if the updates are all odd num length, but there are even ones
    # we still just do len//2
    total = 0
    for update in updates:
        middle = len(update) // 2
        total += update[middle]
    return total

def main():
    input_filenames = [
        "test_input.txt",
        "input.txt",
    ]
    parsed_input = parse_input_files(input_filenames)
    for test_case, parsed_input in parsed_input.items():
        rules = parsed_input["rules"]
        updates = parsed_input["updates"]
        incorrect_updates = check_order(rules, updates)
        result = middle_num_sum(incorrect_updates)
        print(f"For input '{test_case}' got {result}")

if __name__ == "__main__":
    main()
