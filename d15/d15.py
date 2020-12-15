
inp = [0,5,4,1,10,14,7]

seen = {n: i for i, n in enumerate(inp[:-1])}
ind = inp[-1]

for i in range(i-1, 30000000-1):
    nind = i - seen.get(ind, i)
    seen[ind] = i
    ind = nind

print()
print(f"Part 2: {ind}")
