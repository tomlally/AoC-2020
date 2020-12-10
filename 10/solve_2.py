
def read_input(path):
    with open(path, "r") as file:
        return list(map (lambda x: int(x), file.readlines()))

def go(input):
    tgt = max(input) + 3
    input =  [0] + sorted(input) + [tgt]
    
    cache = { }
    def paths_to(x, xs):
        if x == 0:
            return 1
        elif x in cache:
            return cache[x]
        else:
            come_from = list(filter(lambda y: x-3 <= y and y <= x-1, input))
            v = sum(map(lambda y: paths_to(y, xs), come_from))
            cache[x] = v
            return cache[x] 
            
    return paths_to(tgt, input)

def main():
    input = read_input("input.txt")
    print(go(input))    

if __name__ == "__main__":
    main()