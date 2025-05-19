

def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    # we'll build a hash table, index a course, value is the courses that can't come before it
    table = {}
    for pair in prerequisites:
        a, b = pair # a cannot come before b
        if b not in table:
            table[b] = []
        table[b].append(a)
    
    # create tiered levels for adding courses based on prereqs
    levels = []
    to_insert = list(table.keys())
    level = 0
    while len(to_insert) != 0:
        levels.append([])

        # add all keys that aren't dependent on another
        remaining_keys = set(to_insert[::]) # shallow copy
        dependencies = { dep for key in remaining_keys for dep in table[key] }
        independent = remaining_keys - dependencies
        levels[level].extend(independent)
        for key in independent:
            to_insert.remove(key)

        # check for circular dependency
        if levels[-1] == []: # circular dependency will result in no one being added to the level, even though some remain
            return []
        level += 1
    
    courses = list(range(numCourses))
    courseOrder = []
    for level in levels:
        for course in level:
            courseOrder.append(course)
            courses.remove(course)
    for course in courses:
        courseOrder.append(course)
    return courseOrder

def main():
    test_cases = [
        # (numCourses, prerequisits, expectedOutput)
        # (4, [[1,0],[2,0],[3,1],[3,2]], [[0,1,2,3], [0,2,1,3]]),
        # (2, [[1,0]], [[0,1]]),
        # (1, [], [[0]]),
        # (2, [[0,1]], [[1,0]]),
        (8, [[1,0],[2,6],[1,7],[6,4],[7,0],[0,5]], [[5,4,6,3,2,0,7,1]])

    ]
    for i, testCase in enumerate(test_cases):
        numCourses, prerequisits, expectedOutput = testCase
        actualOutput = findOrder(numCourses, prerequisits)
        assert actualOutput in expectedOutput, f"Failed test case {i}: got {actualOutput}, expected {expectedOutput}"
    print("Passed all test cases!")

if __name__ == "__main__":
    main()