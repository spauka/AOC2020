from collections import defaultdict
from functools import lru_cache

inp = [0]
with open("input.txt") as f:
    inp.extend(int(x) for x in f)
inp.sort()
inp.append(inp[-1]+3)

counts = defaultdict(int)
for i1, i2 in zip(inp, inp[1:]):
    counts[i2-i1] += 1
print(f"Part 1: {counts[1] * counts[3]}")

@lru_cache
def count_poss(start_ind):
    if start_ind == len(inp)-1:
        return 1 # Only 1 possibility for last charger
    poss = 0
    ind = start_ind + 1
    while ind < len(inp) and inp[ind]-inp[start_ind] <= 3:
        poss += count_poss(ind)
        ind += 1
    return poss
print(f"Part 2: {count_poss(0)}")
print(count_poss.cache_info())

# Part 2 iterative - just for practice
counts = [0] * len(inp)
counts[-1] = 1
for ind in range(len(inp)-2, -1, -1):
    for end_ind in range(ind+1, min(len(inp), ind+4)):
        if inp[end_ind] <= inp[ind] + 3:
            counts[ind] += counts[end_ind]
print(f"Part 2 (iterative): {counts[0]}")