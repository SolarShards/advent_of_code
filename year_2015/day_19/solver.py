from re import finditer


def read_input(filename: str) -> tuple[dict[str, list[str]], str]:
    inp = [line.split() for line in open(filename)]
    replacements: dict[str, list[str]] = {}
    for m, _, r in inp[:-2]:
        if m not in replacements:
            replacements[m] = []
        replacements[m].append(r)
    return replacements, inp[-1][0]


def part_one(filename: str) -> int:
    replacements, molecule = read_input(filename)
    return len(set([
        molecule[:m] + molecule[m:].replace(atom, rep, 1)
        for atom, reps in replacements.items()
        for m in [m.start() for m in finditer(atom, molecule)]
        for rep in reps
    ]))


def part_two(filename: str) -> int:
    replacements, medicine = read_input(filename)
    rev_replacements = {r: m for m, reps in replacements.items() for r in reps}
    reps = sorted(rev_replacements.keys(), key=len, reverse=True)
    steps = 0
    while medicine != "e":
        for rep in reps:
            cnt = medicine.count(rep)
            if cnt:
                medicine = medicine.replace(rep, rev_replacements[rep])
                steps += cnt
                break
    return steps
