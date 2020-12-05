from operator import itemgetter
def partition(start, stop, part):
    mid = start + ((stop - start)>>1)
    return (mid+1, stop) if part else (start, mid)

seats = []
with open("input") as f:
    for line in f:
        if (line := line.strip()):
            pr = (0, 127)
            pc = (0, 7)
            for c in line[:7]:
                pr = partition(*pr, (c=="B"))
            for c in line[7:]:
                pc = partition(*pc, (c=="R"))
            seats.append((pr[0], pc[0], (pr[0] << 3) + pc[0]))
seats.sort(key=itemgetter(2))

print(f"Highest ID: {seats[-1][2]}")

missing = 0
for i in range(seats[-1][2]):
    if i != seats[i-missing][2]:
        missing += 1
        if (i-missing) == -1:
            continue
        print(f"Missing ID: {i}")
