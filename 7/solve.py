
def read_input(path):
    rules = { }
    with open(path) as file:
        for line in file.readlines():
            outer, inner = line.strip().split(" bags contain ")
            contents = [] if inner == "no other bags." else [(x.replace(" bags", "").replace(" bag", "").replace(".", "")[2:], int(x[:1])) for x in inner.split(", ")]
            rules[outer] = contents
    return rules

def can_contain(rules, parent, desired):
    return any(child == desired or can_contain(rules, child, desired) for child, _ in rules[parent])

def must_contain(rules, parent):
    return sum(n * (1 + must_contain(rules, child)) for child, n in rules[parent])
    
def main():
    rules = read_input("input.txt")
    print(sum(can_contain(rules, parent, "shiny gold") for parent in rules))
    print(must_contain(rules, "shiny gold"))

if __name__ == "__main__":
    main()
