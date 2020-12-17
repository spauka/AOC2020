import itertools
from collections import defaultdict
import copy

cube = defaultdict(int)

with open("input.txt") as f:
    for y, line in enumerate(f):
        for x, c in enumerate(line.strip()):
            cube[(x, y, 0, 0)] = (c == "#")

def adjacency(cube, pos):
    active = 0
    for offs in itertools.product((-1, 0, 1), repeat=len(pos)):
        npos = tuple(i+j for i, j in zip(pos, offs))
        active += cube[npos]
    return active

def bounding_cube(cube, extend=True):
    minbound, maxbound = None, None
    for pos in cube:
        if not cube[pos]:
            continue
        if minbound is None:
            minbound = pos
            maxbound = pos
        else:
            minbound = tuple(min(i, j) for i, j in zip(minbound, pos))
            maxbound = tuple(max(i, j) for i, j in zip(maxbound, pos))
    if extend:
        minbound = tuple(i-1 for i in minbound)
        maxbound = tuple(i+1 for i in maxbound)
    return (minbound, maxbound)

def print_cube(cube):
    minbound, maxbound = bounding_cube(cube, False)
    print(minbound, maxbound)
    for z, w in itertools.product(range(minbound[2], maxbound[2]+1), range(minbound[3], maxbound[3]+1)):
        print(f"z = {z}, w = {w}")
        for y in range(minbound[1], maxbound[1]+1):
            print("".join("#" if cube[(x,y,z,0)] else "." for x in range(minbound[0], maxbound[0]+1)))

for i in range(12):
    ncube = defaultdict(int)
    for pos in itertools.product(*(range(a, b+1) for a, b in zip(*bounding_cube(cube)))):
        nadj = adjacency(cube, pos)
        if cube[pos] and nadj in (3, 4):
            ncube[pos] = True
        if not cube[pos] and nadj == 3:
            ncube[pos] = True
    cube = ncube

    print(f"After {i+1} cycles, {sum(cube.values())} active")
