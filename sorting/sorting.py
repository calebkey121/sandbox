class Sort:
    def __init__(self):
        self.test_cases = [
            ([], []),                                 # Empty list
            ([1], [1]),                               # Single element
            ([1, 2, 3], [1, 2, 3]),                   # Already sorted
            ([3, 2, 1], [1, 2, 3]),                   # Reverse sorted
            ([5, 3, 3, 1, 2], [1, 2, 3, 3, 5]),       # Duplicates
            ([0, -1, 5, -10, 3], [-10, -1, 0, 3, 5]), # Negative numbers
            ([10, -10, 0], [-10, 0, 10]),            # Mixed positive/negative
            ([3.5, 2.1, 5.9], [2.1, 3.5, 5.9]),       # Floating-point numbers
            ([1, 2.5, -3, 0], [-3, 0, 1, 2.5]),       # Mixed int and float
            (['b', 'a', 'c'], ['a', 'b', 'c']),       # Strings
            (['apple', 'Banana', 'banana'], ['Banana', 'apple', 'banana']), # Case sensitivity
        ]

    def sort_test(self, test_sort) -> bool:
        for case, expected in self.test_cases:
            result = test_sort(case)
            assert result == expected, f"Failed Test Case: Got {result}, expected {expected}"
        print("Passed all Test Cases!!!")
    
    def merge_sort(self, unsorted_list: list) -> list:
        length = len(unsorted_list)
        if length <= 1:
            return unsorted_list
        left = self.merge_sort(unsorted_list[:length // 2])
        right = self.merge_sort(unsorted_list[length // 2:])

        # merge the now sorted left and right
        merged = []
        l = r = 0
        while l < len(left) and r < len(right): # go until one hits the end
            if left[l] < right[r]:
                merged.append(left[l])
                l += 1
            else:
                merged.append(right[r])
                r += 1
        
        # one has hit the end of their list, add the other
        if l == len(left):
            # add rest of right
            merged.extend(right[r:])
        else:
            merged.extend(left[l:])
        
        return merged

def main():
    s = Sort()
    s.sort_test(s.merge_sort)

if __name__ == "__main__":
    main()
