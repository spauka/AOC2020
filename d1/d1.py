import re
import itertools

def qp(line):
    m = re.findall(r"([-+\d]+)", line)
    return tuple(int(x) for x in m)

with open("input.txt") as inp:
    d = qp(inp.read())

n = 3
for i in itertools.combinations(d, n):
    if sum(i) == 2020:
        prod = 1
        for num in i:
            prod *= num
        print(i, prod)