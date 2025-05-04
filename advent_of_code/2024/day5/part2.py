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
                    rule = [ int(a) for a in line.rstrip().split('|') ]
                    if rule[0] == rule[1]:
                        raise ValueError(f"hey look at this rule! {rule[0]}|{rule[1]}")
                    rules.append(rule)
                elif line.strip() != "": # update (not a blank line)
                    updates.append([ int(a) for a in line.rstrip().split(',')])
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
        before, after = rule

        # make an entry for 'after' if it doesn't exist
        if before not in rules_table:
            rules_table[before] = set()
        rules_table[before].add(after)
    
    # Now we have our rules table, we can loop through update, check the current number and compare its table entry with numbers weve encountered
    for update in updates:
        correct = True
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

    return rules_table, correct_updates, incorrect_updates

# sum of the middle number of a list of updates
def middle_num_sum(updates: list) -> int:
    # problem doesn't state if the updates are all odd num length, but there are even ones
    # we still just do len//2
    total = 0
    for update in updates:
        middle = len(update) // 2
        total += update[middle]
    return total

def correct_invalid_updates(rules_table: dict, incorrect_updates: list) -> list:
    corrected_updates = []

    for update in incorrect_updates:
        corrected_update = []
        for idx, num in enumerate(update):
            corrected_update.append(num) # don't worry, we'll swap when we need to
            incompatible_nums = rules_table.get(num) # find the numbers we can't have already encountered
            if incompatible_nums:
                # we will call our own little sorting method
                # last number will be the one we're bubbling up
                sort_idx = len(corrected_update) - 1
                bubble(sort_idx, corrected_update, rules_table)
        corrected_updates.append((update, corrected_update))
    
    return corrected_updates

# return the corrected update list after sorting the given list
def bubble(sort_idx: int, corrected_update: list, rules_table: dict) -> list:
    if sort_idx == 0:
        # base case, must be sorted
        return corrected_update

    # walk backwards from the current sort_idx
    sort_num = corrected_update[sort_idx]
    incompatible_nums = rules_table[sort_num]
    for i in range(sort_idx - 1, -1, -1):
        check = corrected_update[i]
        # if you find an incompatible num
        if check in incompatible_nums:
            # swap and call again with current idx
            corrected_update[i] = sort_num
            corrected_update[sort_idx] = check
            bubble(sort_idx - 1, corrected_update, rules_table)
            break
    
    # if you make it to the end, no incompatible nums were found, youre good
    return corrected_update

def main():
    input_filenames = [
        "test_input.txt",
        "input.txt",
    ]
    parsed_input = parse_input_files(input_filenames)
    for test_case, parsed_input in parsed_input.items():
        rules = parsed_input["rules"]
        updates = parsed_input["updates"]
        rules_table, correct_updates, incorrect_updates = check_order(rules, updates)
        corrected_update_pairs = correct_invalid_updates(rules_table, incorrect_updates)
        # Lets print the updates and their relevant rules
        for pair in corrected_update_pairs:
            original_update, corrected_update = pair
            #print(f"{original_update} -> {corrected_update}")
            #print(f"Rules: {[f"{a}|{rules_table[a]}" for a in original_update if a in rules_table]}\n")

        corrected_updates = [ corrected for original, corrected in corrected_update_pairs ]
        result = middle_num_sum(corrected_updates)
        print(f"For input '{test_case}' got {result}")

if __name__ == "__main__":
    main()

# 6257 too low!
# 6890 too high!