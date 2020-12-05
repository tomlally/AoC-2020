from functools import reduce

def read_input(path):
    with open(path, "r") as file:
        for line in file.readlines():
            yield [c == 'B' or c == 'R' for c in line.strip()]

def bsp(x):
    return sum(2 ** (len(x)-i-1) for i, c in enumerate(x) if c)

def id(x):
    return bsp(x[:7]) * 8 + bsp(x[-3:])

def main():
    ids = list(id(x) for x in read_input("input.txt"))

    print(max(ids))
    print(next(x for x in range(min(ids), max(ids)) if x not in ids and x+1 in ids and x-1 in ids))

if __name__ == "__main__":
    main()