import sys
import numpy as np
from numpy.lib.stride_tricks import as_strided
import itertools

with open("input.txt") as f:
    seats = np.array(list(list(c=="L" for c in l.strip()) for l in f), dtype="int").T
filled = np.zeros((seats.shape[0]+2, seats.shape[1]+2), dtype="int")

sub_shape = (3, 3)
view_shape = tuple(np.subtract(filled.shape, sub_shape) + 1) + sub_shape
strides = filled.strides + filled.strides

psum = -1
new_filled = filled.copy()
while (nsum := np.sum(filled)) != psum:
    filled_view = as_strided(filled, view_shape, strides, writeable=False)
    na = np.sum(filled_view, axis=(2,3))
    for coord in itertools.product(*map(range, seats.shape)):
        fcoord = tuple(i+1 for i in coord)
        if seats[coord] and na[coord] == 0:
            new_filled[fcoord] = 1
        elif filled[fcoord] and na[coord] >= 5:
            new_filled[fcoord] = 0
    filled = new_filled.copy()
    psum = nsum

print(f"Part 1: {nsum}")
sys.exit(0)

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
