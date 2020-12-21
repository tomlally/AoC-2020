import itertools

class Space():
    def __init__(self, dims):
        self.active = set()
        self.dims = dims
        self.min = [0] * self.dims
        self.max = [0] * self.dims

    def load(dims, string):
        space = Space(dims)
        for y, line in enumerate(string.splitlines(keepends=False)):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    coord = [0] * space.dims
                    coord[0] = x
                    coord[1] = y
                    space.activate(coord)
        return space

    def activate(self, coord):
        for i in range(self.dims):
            if coord[i] > self.max[i]:
                self.max[i] = coord[i]
            if coord[i] < self.min[i]:
                self.min[i] = coord[i]
        self.active.add(tuple(coord))

    def count(self):
        return len(self.active)

    def extent(self, dim):
        return range(self.min[dim]-1, self.max[dim]+1+1)
    
    def simulate(self):
        new = Space(self.dims);
        for xs in itertools.product(*[self.extent(dim) for dim in range(self.dims)]):        
            ns = sum(tuple(x+d for (x, d) in zip(xs, ds)) in self.active for ds in itertools.product(*([range(-1, 1+1)] * self.dims)) if any(ds))

            if xs in self.active:
                if ns == 2 or ns == 3:
                    new.activate(xs)
            elif ns == 3:
                new.activate(xs)
        
        return new

    def boot(self):
        return self.simulate().simulate().simulate().simulate().simulate().simulate()

def read_input(path):
    with open(path, "r") as file:
        return file.read()

def main():
    input = read_input("input.txt")

    print(Space.load(3, input).boot().count())
    print(Space.load(4, input).boot().count())

if __name__ == "__main__":
    main()
