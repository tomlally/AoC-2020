from enum import Enum

class InstrType(Enum):
    WRITE = 0,
    MASK = 1

def read_input(path):
    with open(path, "r") as file:
        for line in file.readlines():
            if line.startswith("mask"):
                yield InstrType.MASK, line[7:].strip()
            else:
                addr, data = line.split(" = ")
                yield InstrType.WRITE, (int(addr[4:][:-1]), int(data))

def and_mask(mask):
    return int(mask.replace("X", "1"), base=2)

def or_mask(mask):
    return int(mask.replace("X", "0"), base=2)

def floating_addrs(mask, addr):
    addr = list(bin(addr)[2:].zfill(36))
    bits = mask.count('X')
    for i in range(2 ** bits):
        fill = list(bin(i)[2:].zfill(bits))

        def combine(addr, mask):
            if mask == 'X':
                return fill.pop()
            elif mask == '1':
                return '1'
            elif mask == '0':
                return addr

        yield int("".join([combine(a, m) for a, m in zip(addr, mask)]), base=2)

def write1(mem, addr, data, mask):
    mem[addr] = data & and_mask(mask) | or_mask(mask)

def write2(mem, addr, data, mask):
    for addr in floating_addrs(mask, addr):
        mem[addr] = data

def go(instrs, f):
    mem = { }
    mask = ""
    for instr, v in instrs:
        if instr == InstrType.MASK:
            mask = v
        elif instr == InstrType.WRITE:
            f(mem, *v, mask)

    return sum(mem.values())

def main():
    input = list(read_input("input.txt"))

    print(go(input, write1))
    print(go(input, write2))

if __name__ == "__main__":
    main()