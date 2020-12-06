import string

def read_input(path):
    with open(path) as file:
        for goup in file.read().split('\n\n'):
            yield goup.splitlines(keepends=False)

def p1(group):
    return sum(any(x in entry for entry in group) for x in string.ascii_lowercase)

def p2(group):
    return sum(all(x in entry for entry in group) for x in string.ascii_lowercase)

def main():
    input = list(read_input("input.txt"))
    
    print(sum(p1(x) for x in input))
    print(sum(p2(x) for x in input))
    
if __name__ == "__main__":
    main()