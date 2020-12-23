
class Solve:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self, values, length):
        self.nodes = [self.Node(i+1) for i in range(length)]
        
        for i in range(1, length):
            self[i].next = self[i+1]
        self[length].next = self[values[0]]

        for i in range(len(values)-1):
            self[values[i]].next = self[values[i+1]]
        
        if length > len(values):
            self[values[-1]].next = self[len(values) + 1]
        else:
            self[values[-1]].next = self[values[0]]

        self.curr = self[values[0]]

        self.min = 1
        self.max = length

    def __getitem__(self, i):
        return self.nodes[i-1]

    def src(self):
        return [self.curr.next, self.curr.next.next, self.curr.next.next.next]

    def dst(self):
        def dcr(x):
            x -= 1
            if x < self.min:
                x = self.max
            return x

        x = dcr(self.curr.value)
        while x in map(lambda x: x.value, self.src()):
            x = dcr(x)
        
        return self[x]
        
    def run(self):
        src = self.src()
        dst = self.dst()

        self.curr.next = src[-1].next

        src[-1].next = dst.next
        dst.next = src[0]

        self.curr = self.curr.next

    def result1(self):
        x = ""
        node = self[1].next
        for _ in range(8):
            x += str(node.value)
            node = node.next
        return x

    def result2(self):
        return self[1].next.value * self[1].next.next.value

def read_input(path):
    with open(path, "r") as file:
        return [int(x) for x in file.read()]

def p1(input):
    solve = Solve(input, len(input))
    for _ in range(100):
        solve.run()
    return solve.result1()

def p2(input):
    solve = Solve(input, 1000000)
    for _ in range(10000000):
        solve.run()
    return solve.result2()

def main():
    input = read_input("input.txt")
    
    print(p1(input))
    print(p2(input))

if __name__ == "__main__":
    main()