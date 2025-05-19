passwords = []
password_substrings = {}

def add_password(password: str) -> bool:
    passwords.append(password)

    # Since we only want one match per password, we can have a separate list to track current password substrings
    curr_substrings = []

    # Add substrings to make query very simple
    length = len(password)
    for i in range(length):
        for j in range(i, length):
            substring = password[i:j + 1] # slicing doesn't go out of index here even with the plus 1
            
            # skip if already in curr_substrings, since only one per password is allowed
            if substring in curr_substrings:
                continue
            # otherwise track it in case we run into it later
            curr_substrings.append(substring)

            # Now just increment hash table tracker
            if substring not in password_substrings:
                password_substrings[substring] = 0
            password_substrings[substring] += 1

    return True

def query_password(q_password: str) -> int:
    if not q_password in password_substrings:
        return 0
    return password_substrings[q_password]

def solve(q: int, ops: tuple) -> bool:
    if q != len(ops):
        return False
    for op in ops:
        op_type, password = op
        if op_type == 1:
            add_password(password)
        elif op_type == 2:
            matches = query_password(password)
            print(matches)

def main():
    q = 6
    ops = [(2, "dish"), (1, "brandish"), (1,"radishes"), (1, "aaa"), (2, "dish"), (2, "a")]
    solve(q, ops)

main()
