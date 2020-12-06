all_answers = []
with open("input.txt") as f:
    answers = set()
    for line in f:
        if not (line := line.strip()):
            all_answers.append(answers)
            answers = set()
        answers.update(list(line))
all_answers.append(answers)

print(sum(len(x) for x in all_answers))

all_answers = []
with open("input.txt") as f:
    answers = None
    for line in f:
        if not (line := line.strip()):
            all_answers.append(answers)
            answers = None
            continue
        if answers is None:
            answers = set(list(line))
        else:
            answers.intersection_update(list(line))
all_answers.append(answers)

print(sum(len(x) for x in all_answers))