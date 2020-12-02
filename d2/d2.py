import re

def qp(line):
    m = re.findall(r"([+\d]+)", line)
    return tuple(int(x) for x in m)

with open("input") as inp:
    valid1 = 0
    valid2 = 0
    for line in inp:
        c, l, p = line.strip().split()
        c = qp(c)
        l = l[0]
        if c[0] <= p.count(l) <= c[1]:
            valid1 += 1
        if (p[c[0]-1] == l) ^ (p[c[1]-1] == l):
            valid2 += 1

    print(f"Valid Count: {valid1}")
    print(f"Valid Count: {valid2}")