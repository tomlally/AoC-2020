from math import prod

def read_input(path):
  
    def read_ticket(string):
        return list(int(x) for x in string.split(","))

    def read_your(string):
        return read_ticket(string[13:])

    def read_others(string):
        for ticket in string[16:].strip().split("\n"):
            yield read_ticket(ticket)

    def read_fields(string):
        for field in string.split("\n"):
            name, ranges = field.split(": ")
            yield name, list(list(int(y) for y in x.split("-")) for x in ranges.split(" or "))
    
    with open(path, "r") as file:
        fields_str, your_str, others_str = file.read().split("\n\n")
        return list(read_fields(fields_str)), read_your(your_str), list(read_others(others_str))

# check that a given value is valid in a given field
def check_field(value, field):
        range0, range1 = field[1]
        min0, max0 = range0
        min1, max1 = range1
        return min0 <= value <= max0 or min1 <= value <= max1

# check that a given value is valid in at least one field in a list of given fields
def check_fields(value, fields):
    return any(check_field(value, field) for field in fields)
   
# check that a ticket is valid, i.e. all of its field values are valid for at least one field
# NB: this doesn't check that the field values aren't valid in the same field
def check_ticket(ticket, fields):
    return all(check_fields(field_value, fields) for field_value in ticket)

# find a mapping of field names to ticket field value indices.
def find_mapping(your, others, fields):
    
    mapping = { }
    mapped = set()

    # remove invalid tickets and append your ticket
    tickets = [ticket for ticket in others if check_ticket(ticket, fields)]
    tickets.append(your)
    
    # while the mapping is incomplete
    while len(mapping) != len(fields):
        
        # look over every 'set' of enties
        for i in range(len(tickets[0])):
            if i not in mapped:
                
                could_be = [field for field in fields if (all(check_field(ticket[i], field) for ticket in tickets) and field[0] not in mapping)]

                if len(could_be) == 1:
                    mapping[could_be[0][0]] = i
                    mapped.add(i)

    return mapping

def p1(others, fields):
    return sum(sum(field_value for field_value in other if not check_fields(field_value, fields)) for other in others)

def p2(your, others, fields):
    return prod(your[idx] for key, idx in find_mapping(your, others, fields).items() if key.startswith("departure"))

def main():
    fields, your, others = read_input("input.txt")
    
    print(p1(others, fields))
    print(p2(your, others, fields))

if __name__ == "__main__":
    main()