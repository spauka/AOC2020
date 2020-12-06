import re

reqd = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
count = 0
passports = []

with open("input.txt") as inp:
    d = {}
    for line in inp:
        if not line.strip():
            if reqd.intersection(d.keys()) == reqd:
                count += 1
                passports.append(d)
            d = {}
            
        for k, v in re.findall(r"([a-z]+):([#a-zA-Z0-9]+)", line):
            d[k] = v

print(f"Count: {count}")

count2 = 0
for d in passports:
    if not (1920 <= int(d["byr"]) <= 2002):
        continue
    if not (2010 <= int(d["iyr"]) <= 2020):
        continue
    if not (2020 <= int(d["eyr"]) <= 2030):
        continue

    if d["hgt"].endswith("cm"):
        if not (150 <= int(d["hgt"][:-2]) <= 193):
            continue
    elif d["hgt"].endswith("in"):
        if not (59 <= int(d["hgt"][:-2]) <= 76):
            continue
    else:
        continue

    if not re.match("^#[0-9a-zA-Z]{6}$", d["hcl"]):
        continue

    if not d["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        continue
    
    if not re.match("^[0-9]{9}$", d["pid"]):
        continue

    count2 += 1
print(f"Count: {count2}")