from itertools import permutations
from functools import reduce
from operator import mul

def conv(path):
    with open(path, 'r') as file:
        return list(map(lambda x: int(x), file.readlines()))

def run(list, n):
    for tup in permutations(list, n):
        if sum(tup) == 2020:
            return reduce(mul, tup)

def main():
    list = conv('input.txt')
    print(run(list, 2))
    print(run(list, 3))
    
if __name__ == '__main__':
    main()
