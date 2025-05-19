def happy_number(a: int) -> bool:
    num = a
    happy = True
    tortise = sum([int(i) * int(i) for i in str(num)])
    hare = sum([int(i) * int(i) for i in str(tortise)])
    while (total := sum([int(i) * int(i) for i in str(num)])) != 1:
        if tortise == hare:
            return not happy
        # iter tortise and hare
        tortise = sum([int(i) * int(i) for i in str(tortise)])
        hare = sum([int(i) * int(i) for i in str(hare)])
        hare = sum([int(i) * int(i) for i in str(hare)])
        num = total
    return happy


def main():
    print(f"happy_number(19) = {happy_number(19)}")
    print(f"happy_number(2) = {happy_number(2)}")
    print(f"happy_number(7) = {happy_number(7)}")

if __name__ == "__main__":
    main()