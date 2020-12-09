import itertools

with open("input") as f:
    inp = tuple(int(x) for x in f)

for i in range(25, len(inp)):
    target = inp[i]
    poss = set()
    for n in inp[i-25:i]:
        if n in poss: break
        poss.add(target-n)
    else:
        print(f"Part 1: {target}")
        break

j = 0
k = 1
while j < k <= i:
    s = sum(inp[j:k])
    if s < target: k += 1
    elif s == target: break
    else: j += 1

print(f"Part 2: {min(inp[j:k]) + max(inp[j:k])}")
