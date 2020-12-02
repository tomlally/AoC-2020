
def read_input(path):

    def read_line(line):
        policy, password = line.split(':')
        policy_params, policy_char = policy.split(' ')
        a, b = policy_params.split('-')
        return int(a), int(b), policy_char, password
 
    with open(path, 'r') as file:
        return list(map(read_line, file.readlines()))

def filter_count(f, xs):
    return len(list(filter(f, xs)))

def f1(min, max, chr, pwd):
    x = filter_count(lambda x: x == chr, pwd)
    return min <= x and x <= max

def f2(cidx1, cidx2, chr, pwd):
    return (pwd[cidx1] == chr) ^ (pwd[cidx2] == chr)

def main():
    input = read_input('input.txt')

    print(filter_count(lambda tup: f1(*tup), input))
    print(filter_count(lambda tup: f2(*tup), input))

if __name__ == '__main__':
    main()