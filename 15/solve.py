def read_input(path):
    with open(path, "r") as file:
        return [int(x) for x in file.read().split(",")]

def solve(input, count):

    numbers = { }
    turn = 1
    for n in input:
        numbers[n] = (turn, None)
        turn += 1
    last = input[len(input)-1]

    def say(n):
        nonlocal last
        if n in numbers:
            l, r = numbers[n]
            numbers[n] = (turn, l)
        else:
            numbers[n] = (turn, None)
        last = n

    while turn <= count:
        l, r = numbers[last]
        say(0 if r is None else l-r)
        turn += 1

    return last

def main():
    input = read_input("input.txt");
    print(solve(input, 2020))
    print(solve(input, 30000000))

if __name__ == "__main__":
    main()