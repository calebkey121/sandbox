def candy(ratings):
    total = 0
    prev_change = None

    for first, second in zip(ratings, ratings[1:]):
        # special case for first child
        total += 1 # base for every candy
        # first find the change
        if first == second:
            change = 'equal'
        elif first < second:
            change = 'increase'
        else:
            change = 'decrease'

        if change in ('increase', 'decrease') and change == prev_change:
            consecutive += 1
            total += consecutive
    return total # we can instead just increment a total counter and avoid the runtime of sum

if __name__ == "__main__":
    candy([2,1,0])
