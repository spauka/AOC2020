import itertools

instrs = []
with open("input.txt") as f:
    for line in f:
        loc, _, val = line.strip().split()
        instrs.append((loc, val))

mem = {}
mask = ""
for loc, instr in instrs:
    if loc == "mask":
        mask = instr
    else:
        loc = int(loc[4:-1])
        val = list(f"{int(instr):036b}")
        for i, m in enumerate(mask):
            if m in ('0', '1'):
                val[i] = m
        val = int("".join(val), 2)
        mem[loc] = val
print(f"Part 1: {sum(mem.values())}")

mem = {}
mask = ""
for loc, instr in instrs:
    if loc == "mask":
        mask = instr
    else:
        loc = list(f"{int(loc[4:-1]):036b}")
        val = int(instr)
        flippy = []

        for i, m in enumerate(mask):
            if m == "1":
                loc[i] = "1"
            elif m == "X":
                flippy.append(i)

        for flips in itertools.product(("0", "1"), repeat=len(flippy)):
            for l, v in zip(flippy, flips):
                loc[l] = v
            mem[int("".join(loc), 2)] = val
print(f"Part 2: {sum(mem.values())}")
