input = [1,12,0,20,8,16]
example1 = [1,3,2]
example2 = [2,1,3]
example3 = [1,2,3]

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
    print(solve(input, 2020))
    print(solve(input, 30000000))

if __name__ == "__main__":
    main()