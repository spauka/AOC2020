import re
from collections import defaultdict

what_contains = defaultdict(set)
counts = defaultdict(list)
with open("input") as f:
    for line in f:
        out_bag, in_bags = re.fullmatch(r"(.*) bags? contain (.*).", line.strip()).groups()
        for count, bag in re.findall(r"([0-9]+) ([^,]+) bags?", in_bags):
            counts[out_bag].append((int(count), bag))
            what_contains[bag].add(out_bag)

poss = {"shiny gold"}
tested = set()
while poss:
    tested.add(cbag := poss.pop())
    poss.update(what_contains[cbag].difference(tested))
print(f"Part 1: {len(tested)-1}")

def count_nested(bag):
    ccount = 1 # 1 for this bag
    for bag_count, in_bag in counts[bag]:
        ccount += bag_count * count_nested(in_bag)
    return ccount
print(f"Part 2: {count_nested('shiny gold')-1}")
