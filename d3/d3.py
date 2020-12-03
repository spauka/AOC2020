import numpy as np

with open("input.txt") as f:
    g = np.array(list(list(l.strip()) for l in f), dtype="object").T

def traverse(g, slope):
    pos = np.array((0, 0))
    count = 0
    while pos[1] < g.shape[1]:
        count += (g[pos[0]%g.shape[0], pos[1]] == '#')
        pos += slope
    return count

# Part 1
print(f"Part 1: {traverse(g, (3, 1))}")

prod = 1
for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    prod *= traverse(g, slope)
print(f"Part 2: {prod}")