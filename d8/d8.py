import re

instr = []

with open("input") as f:
    instr = [line.strip().split() for line in f]
    instr = [(i[0], int(i[1])) for i in instr]

def run_prog(instr):
    pos = acc = 0
    run = set()
    while True:
        if pos in run:
            return "rep", pos, acc
        if pos == len(instr):
            return "fixed", pos, acc
        if pos > len(instr):
            return "fail", pos, acc

        run.add(pos)
        i, arg = instr[pos]
        if i == "nop":
            pos += 1
        elif i == "acc":
            acc += arg
            pos += 1
        elif i == "jmp":
            pos += arg

print(f"Part 1: {run_prog(instr)[2]}")

for p, i in enumerate(instr):
    if i[0] in ("nop", "jmp"):
        new_instr = instr.copy()
        new_instr[p] = ("nop" if i[0] == "jmp" else "jmp", i[1])
        res = run_prog(new_instr)
        if res[0] == "fixed":
            print(f"Changed instr at pos {p} from {instr[p]} to {new_instr[p]}.")
            print(f"Part 2: {res[2]}")
            break
