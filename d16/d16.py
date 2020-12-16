import re
from collections import defaultdict

conditions = defaultdict(list)
my_ticket = []
tickets = []

with open("input.txt") as f:
    for line in f:
        if (match := re.match("([a-z ]+): ([0-9a-z -]+)", line)) is None:
            break
        name, conds = match.groups()
        for cond in re.split("or", conds):
            start, stop = cond.split('-')
            conditions[name].append(range(int(start), int(stop)+1))

    f.readline()
    my_ticket = [int(x) for x in f.readline().strip().split(',')]
    f.readline()
    f.readline()
    for line in f:
        tickets.append([int(x) for x in line.strip().split(',')])

invalid_values = []
fields = [set(conditions.keys()) for _ in conditions]
for ticket in tickets:
    ticket_valid = True
    for val in ticket:
        for conds in conditions.values():
            if any(val in cond for cond in conds):
                break
        else:
            invalid_values.append(val)
            ticket_valid = False
    if ticket_valid:
        for fnum, val in enumerate(ticket):
            poss_fields = set()
            for field_name, conds in conditions.items():
                if any(val in cond for cond in conds):
                    poss_fields.add(field_name)
            fields[fnum].intersection_update(poss_fields)

print(f"Part 1: {sum(invalid_values)}")

assignments = [None]*len(conditions)
while any(x is None for x in assignments):
    for n, poss in enumerate(fields):
        if len(poss) == 1:
            assignments[n] = poss.pop()
            for f in fields:
                f.difference_update({assignments[n]})

prod = 1
for n, field in enumerate(assignments):
    if field.startswith("departure"):
        prod *= my_ticket[n]
print(f"Part 2: {prod}")
