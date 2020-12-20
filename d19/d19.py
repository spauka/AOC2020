from collections import defaultdict
import itertools

grammar = {}
rgrammar = defaultdict(set)
inputs = []

with open("input_2") as f:
    while (line := f.readline().strip()):
        rnum, defn = line.split(":")
        rnum = int(rnum)
        defn = defn.split('|')
        grammar[rnum] = [tuple(int(x) if x.isnumeric() else x.strip("\"") for x in d.split()) for d in defn]

        # Ensure CNF form
        if len(grammar[rnum]) == 1 and isinstance(grammar[rnum][0][0], str):
            grammar[rnum] = grammar[rnum][0][0]
            rgrammar[grammar[rnum]].add(rnum)
        else:
            for rule in grammar[rnum]:
                rgrammar[rule].add(rnum)
    for line in f:
        inputs.append(line.strip())

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

def cnf(inp, grammar, rgrammar):
    check = defaultdict(set)
    for offs, c in enumerate(inp):
        check[(1, offs)].update(rgrammar[c])
    for strlen in range(2, len(inp)+1):
        for offs in range(len(inp)-strlen+1):
            for part in range(1, strlen):
                for comb in itertools.product(check[(part, offs)], check[(strlen-part, offs+part)]):
                    check[(strlen, offs)].update(rgrammar[comb])
    return 0 in check[(len(inp), 0)]

part1 = 0
for i, inp in enumerate(inputs):
    part1 += cnf(inp, grammar, rgrammar)
    print(i, inp, part1)
print(f"Part 2: {part1}")