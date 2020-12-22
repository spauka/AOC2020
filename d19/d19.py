from collections import defaultdict
import itertools
from functools import lru_cache

grammar = {}
rgrammar = defaultdict(set)
inputs = []

with open("input_2") as f:
    while (line := f.readline().strip()):
        rnum, defn = line.split(":")
        rnum = int(rnum)
        defn = defn.split('|')
        grammar[rnum] = [tuple(int(x) if x.isnumeric() else x.strip("\"") for x in d.split()) for d in defn]

        # Create lookup table for rules
        if len(grammar[rnum]) == 1 and isinstance(grammar[rnum][0][0], str):
            grammar[rnum] = grammar[rnum][0][0]
            rgrammar[grammar[rnum]].add(rnum)
        else:
            for rule in grammar[rnum]:
                rgrammar[rule].add(rnum)
    for line in f:
        inputs.append(line.strip())
inputs.sort(key=lambda x: len(x), reverse=True)

# Transform to CNF form
# Eliminate unit rules
for rnum, rules in grammar.items():
    i = 0
    while i < len(rules):
        if len(rules[i]) == 1 and isinstance(rules[i][0], int):
            rules.extend(grammar[rules[i][0]])
            old_rule = rules.pop(i)
            rgrammar[old_rule].remove(rnum)
            for rule in grammar[old_rule[0]]:
                rgrammar[rule].add(rnum)
        elif len(rules[i]) > 2:
            raise RuntimeError("Need to implement TERM rule for CNF")
        else:
            i += 1

def gen_cyk(grammar, rgrammar):
    @lru_cache(maxsize=(1<<16))
    def cyk_mem(inp):
        if len(inp) == 1:
            return rgrammar[inp]
        generating_rules = set()
        for part in range(1, len(inp)):
            for comb in itertools.product(cyk_mem(inp[:part]), cyk_mem(inp[part:])):
                generating_rules.update(rgrammar[comb])
        return generating_rules
    return cyk_mem

mem_cyk = gen_cyk(grammar, rgrammar)

part1 = 0
for i, inp in enumerate(inputs):
    part1 += (0 in mem_cyk(inp))
    print(i, inp, part1)
print(f"Part 2: {part1}")