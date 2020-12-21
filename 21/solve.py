
def read_input(path):
    with open(path, "r") as file:
        for line in file.readlines():
            ingredients, allergens = line.split("(contains ")
            yield ingredients[:-1].split(" "), allergens[:-2].split(", ")      

def both(xs, ys):
    return [x for x in xs if x in ys]
        
def safe(ing, alg_map):
    for ings in alg_map.values():
        if ing in ings:
            return False;
    return True;

# "Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked;"
def solve(foods):

    alg_map = { }
    for ings, algs in foods:
        for alg in algs:
            if alg in alg_map:
                alg_map[alg] = both(alg_map[alg], ings)
            else:
                alg_map[alg] = ings

    safe_ings = []
    for ings, _ in foods:
        for ing in ings:
            if ing not in safe_ings:
                if (safe(ing, alg_map)):
                    safe_ings.append(ing)

    count = 0;
    for ings, _ in foods:
        for ing in ings:
            if ing in safe_ings:
                count += 1;
    
    ing_map = { }
    while (len(ing_map) < len(alg_map)):
        for alg, ings in alg_map.items():
            ings = [ing for ing in ings if ing not in ing_map]
            if len(ings) == 1:
                ing_map[ings[0]] = alg

    danger_list = [x[0] for x in sorted(ing_map.items(), key=lambda x: x[1])];

    print(count)
    print(",".join(danger_list))

def main():
    solve(list(read_input("input.txt")))

if __name__ == "__main__":
    main()