TABLE_SIZE = 10000

# Return True if a match is found
def brute_force(num: int, snowflakes: list) -> bool:
    # Lets start with british museum
    for idx, snowflake in enumerate(snowflakes):
        # Lets splice the original, to compare one snowflake against the rest
        others = snowflakes[:idx] + snowflakes[idx + 1:] # gracefully hanldes out of bounds idx
        # Or we could list comprehension
        # others = [ snowflake for i, s in enumerate(snowflakes) if i != idx ]
        
        # Now we go through others to ensure none of them match our current snowflake
        for other in others:
            if snowflakes_match(snowflake, other):
                return True
            # will break/return on a match, continue otherwise
    
    # Now we have gone through every possible combination, none of the snowflakes match
    return False

def snowflakes_match(a, b):
    if (snowflake_len := len(a)) != len(b):
        raise ValueError("Snowflake lengths don't match!")
    
    for start in range(snowflake_len):
        wrapped_a = a[start:] + a[:start]
        if wrapped_a == b or wrapped_a == b[::-1]: # Can be forwards or backwards
            return True
    
    # No combination matches
    return False

# Now lets do it using a hash map
def solve(num: int, snowflakes: list) -> bool:
    # First we notice that for two snowflakes to match, they must have an equal sum
    # Lets hash based off of the sum then
    hash_table = {}
    for snowflake in snowflakes:
        # Sum will be our hash function, along with mod table_size
        hash_code = sum(snowflake) % TABLE_SIZE

        # If a bin doesn't exist yet, lets make one
        if hash_code not in hash_table:
            hash_table[hash_code] = []

        # Now just add it
        hash_table[hash_code].append(snowflake)
    
    # Now we've sorted snowflakes into bins where their matches (if any) must exist
    for bin in hash_table.values(): # Loop through the bins
        # Now its fair to brute force the bins
        if brute_force(len(bin), bin):
            return True
    # No possible combinations
    return False

test_cases = [
    [3, [[1,2,3], [2,3,4], [3,4,5]], False],
    [3, [[1,2,3], [2,3,4], [3,2,1]], True],
]

for case in test_cases:
    num, snowflakes, expected = case
    result = solve(num, snowflakes)
    assert result == expected, f"Failed: solve{case} = {expected}; got {result}"

print("All test cases pass!")
