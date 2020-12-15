
inp = [0,5,4,1,10,14,7]

seen = {n: i for i, n in enumerate(inp[:-1])}
i = len(inp)
ind = inp[-1]

for i in range(i, 30000000):
    nind = (i - 1) - seen.get(ind, i - 1)
    seen[ind] = i - 1
    ind = nind

    if i%10000 == 0:
        print(f"N: {i:7}", end="\r")

print()
print(f"Part 2: {ind}")
