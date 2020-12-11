import numpy as np
import itertools

with open("input.txt") as f:
    inp = np.array(list(list(l.strip()) for l in f), dtype="object").T
inp2 = inp.copy()

def num_adjacent(inp, coord):
    count = 0
    for offs in itertools.product(range(-1, 2), repeat=2):
        new_coord = tuple(i+j for i, j in zip(coord, offs))
        if any(i < 0 or i >= l for i, l in zip(new_coord, inp.shape)):
            continue
        if all(i == 0 for i in offs):
            continue
        if inp[new_coord] == "#":
            count += 1
    return count

def num_visible(inp, coord):
    count = 0
    for offs in itertools.product(range(-1, 2), repeat=2):
        if all(i == 0 for i in offs):
            continue
        new_coord = coord
        while True:
            new_coord = tuple(i+j for i, j in zip(new_coord, offs))
            if any(i < 0 or i >= l for i, l in zip(new_coord, inp.shape)):
                break
            if inp[new_coord] == "#":
                count += 1
                break
            elif inp[new_coord] == "L":
                break
    return count

changed = True
inp = inp.copy()
while changed:
    changed = False
    new = inp.copy()
    for coord in itertools.product(*map(range, inp.shape)):
        na = num_adjacent(inp, coord)
        if inp[coord] == "L" and na == 0:
            new[coord] = "#"
            changed = True
        elif inp[coord] == "#" and na >= 4:
            new[coord] = "L"
            changed = True
    inp = new.copy()

print(f"Part 1: {np.sum(inp == '#')}")

changed = True
inp = inp2.copy()
iterc = 0
while changed:
    changed = False
    new = inp.copy()
    for coord in itertools.product(*map(range, inp.shape)):
        na = num_visible(inp, coord)
        if inp[coord] == "L" and na == 0:
            new[coord] = "#"
            changed = True
        elif inp[coord] == "#" and na >= 5:
            new[coord] = "L"
            changed = True
    inp = new.copy()
print(f"Part 2: {np.sum(inp == '#')}")
