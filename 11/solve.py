
def read_input(path):
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]

def count1(layout, ix, iy):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dy != 0 or dx != 0):
                ny = iy + dy
                nx = ix + dx
                if ny >= 0 and ny < len(layout) and nx >= 0 and nx < len(layout[iy]):
                    if layout[ny][nx] == '#':
                        count += 1
    return count

def count2(layout, ix, iy):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dy != 0 or dx != 0):
                i = 1
                while (True):
                    ny = iy + (i * dy)
                    nx = ix + (i * dx)
                    if ny >= 0 and ny < len(layout) and nx >= 0 and nx < len(layout[iy]):
                        if layout[ny][nx] == '#':
                            count += 1
                            break
                        elif layout[ny][nx] == 'L':
                            break
                        else:
                            i += 1
                    else:
                        break
    return count

def rule(layout, ix, iy, heuristic, threshold):
    state = layout[iy][ix]
    if state == 'L' and heuristic == 0:
        return '#'
    elif state == '#' and heuristic >= threshold:
        return 'L'
    else:
        return state

def rule1(layout, ix, iy, heuristic):
    return rule(layout, ix, iy, heuristic, 4)

def rule2(layout, ix, iy, heuristic):
    return rule(layout, ix, iy, heuristic, 5)

def apply1(layout, ix, iy):
    return rule1(layout, ix, iy, count1(layout, ix, iy))

def apply2(layout, ix, iy):
    return rule2(layout, ix, iy, count2(layout, ix, iy))

def iterate(layout, f):
    output = [[None for col in row] for row in layout]

    for iy in range(len(layout)):
        for ix in range(len(layout[iy])):
            output[iy][ix] = f(layout, ix, iy)

    return output

def stabilise(layout, f):
    next_layout = iterate(layout, f)
    while (next_layout != layout):
        layout = next_layout
        next_layout = iterate(layout, f)

    return layout

def countOccupied(layout):
    return sum(map(lambda row: len(list(filter(lambda col: col == '#', row))), layout))

def main():
    layout = read_input("input.txt")

    print(countOccupied(stabilise(layout, apply1)))
    print(countOccupied(stabilise(layout, apply2)))

if __name__ == "__main__":
    main()