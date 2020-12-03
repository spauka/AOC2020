import numpy as np

with open("input.txt") as f:
    lines = [l.strip() for l in f]
    g = np.ndarray((len(lines[0]), len(lines)), dtype="object")
    for i, line in enumerate(lines):
        g[:,i] = list(line)

def traverse(g, slope):
    pos = np.array((0, 0))
    count = 0
    while pos[1] < g.shape[1]:
        if g[pos[0]%g.shape[0], pos[1]] == '#':
            count += 1
        pos += slope
    return count

# Part 1
print(f"Part 1: {traverse(g, (3, 1))}")

prod = 1
for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    prod *= traverse(g, slope)
print(f"Part 2: {prod}")