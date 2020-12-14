from operator import itemgetter

with open("input.txt") as f:
    arrival = int(f.readline())
    buses = []
    for ind, bus in enumerate(f.readline().strip().split(",")):
        if bus != "x":
            bus = int(bus)
            buses.append(((bus-ind)%bus, bus))

next_bus = [(bus - arrival%bus, bus) for _, bus in buses]
next_bus.sort()
print(f"Part 1: {next_bus[0][0] * next_bus[0][1]}")

# Solve the chinese remainder theorem for x
buses.sort(key=itemgetter(1), reverse=True)
curr_prod = 1
curr_ts = buses[0][0]
for (target, modulus), (next_target, next_modulus) in zip(buses, buses[1:]):
    curr_prod *= modulus
    while curr_ts%next_modulus != next_target:
        curr_ts += curr_prod
print(f"Part 2: {curr_ts}")
