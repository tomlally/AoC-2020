import re

def read_input(path):
    with open(path, 'r') as file:
        for group in file.read().split("\n\n"):
            yield list(map (lambda x: x.split(":"), group.replace(" ", "\n").splitlines()))

def check_field(field_name, field_value):
    if field_name == "byr":
        return 1920 <= int(field_value) <= 2002
    elif field_name == "iyr":
        return 2010 <= int(field_value) <= 2020
    elif field_name == "eyr":
        return 2020 <= int(field_value) <= 2030
    elif field_name == "hgt":
        if field_value.endswith("cm"):
            return 150 <= int(field_value[:-2]) <= 193
        elif field_value.endswith("in"):
            return 59 <= int(field_value[:-2]) <= 76
        else:
            return False
    elif field_name == "hcl":
        return re.match("#[0-9a-f]{6}$", field_value) != None
    elif field_name == "ecl":
        return any(x == field_value for x in [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    elif field_name == "pid":
        return re.match("[0-9]{9}$", field_value) != None
    else:
        return True

def check_presence(passport):
    return all(any(x == y[0] for y in passport) for x in [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid" ])

def check_valid(passport):
    return all(check_field(field_name, field_value) for field_name, field_value in passport)
        

def main():
    input = list(read_input("input.txt"))

    print(sum(check_presence(passport) for passport in input))
    print(sum(check_presence(passport) and check_valid(passport) for passport in input))

if __name__ == "__main__":
    main()