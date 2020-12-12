import itertools
import numpy as np
from numpy.lib.stride_tricks import as_strided

with open("input.txt") as f:
    seats: np.ndarray = np.array(list(list(c=="L" for c in l.strip()) for l in f), dtype="int").T
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

def num_visible(seats, filled, coord):
    count = 0
    for offs in itertools.product(range(-1, 2), repeat=2):
        if all(i == 0 for i in offs):
            continue
        new_coord = list(coord)
        while True:
            new_coord[0] += offs[0]
            new_coord[1] += offs[1]
            if (new_coord[0] not in range(seats.shape[0]) or
                new_coord[1] not in range(seats.shape[1])):
                break
            if filled.item(*new_coord):
                count += 1
                break
            elif seats.item(*new_coord):
                break
    return count

filled = np.zeros_like(seats, dtype="int")
new_filled = filled.copy()
psum = -1
while (nsum := np.sum(filled)) != psum:
    changed = False
    for coord in itertools.product(*map(range, seats.shape)):
        na = num_visible(seats, filled, coord)
        if seats[coord] and na == 0:
            new_filled[coord] = 1
        elif filled[coord] and na >= 5:
            new_filled[coord] = 0
    filled = new_filled.copy()
    psum = nsum
print(f"Part 2: {nsum}")
