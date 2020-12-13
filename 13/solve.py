from math import prod

def read_input(path):
    with open(path, "r") as file:
        ts = int(file.readline().strip())
        ids = [(i, int(x)) for i, x in enumerate(file.readline().split(",")) if x != "x"]
        return ts, ids

def min_wait(curr, id):
    i = 1
    while (id * i < curr):
        i += 1
    return (id * i) - curr

def min_time(ids):
    
    # start with a step of 1, having considered none of the ids yet.
    step = 1
    considered = [False for _ in ids]

    # check timestep ts.
    def check(ids, ts):
        nonlocal step
    
        # get a list of which ids are here at this step
        here = list(((ts + idx) % x) == 0 for idx, x in ids)
    
        # for each bus that's here, if it has not already been considered, multiply the step by its period
        for i, (h, (_, v)) in enumerate(zip(here, ids)):
            if (h and not considered[i]):
                considered[i] = True
                step *= v
        
        # if they're all here then the search is done
        return all(here)

    # start at timestep 0
    ts = 0
    while not check(ids, ts):
        ts += step
    
    return ts

def main():
    curr, ids = read_input("input.txt")
    
    print(prod(min((min_wait(curr, x), x) for _, x in ids)))
    print(min_time(ids))

if __name__ == "__main__":
    main()