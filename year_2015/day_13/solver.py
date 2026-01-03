from itertools import permutations, pairwise


def read_input(
        filename: str
        ) -> tuple[set[str], dict[tuple[str, str], int]]:
    lines = [line.split() for line in open(filename)]
    return set(list(zip(*lines))[0]), {
        (ln[0], ln[-1][:-1]): int(ln[3]) * (-1 if ln[2] == "lose" else 1)
        for ln in lines
    }


def optimize_seating(
        people: set[str],
        relations: dict[tuple[str, str], int]) -> int:
    best = int(-1e9)
    for arrangement in permutations(people):
        happiness = 0
        for p1, p2 in pairwise(arrangement + (arrangement[0],)):
            happiness += relations[(p1, p2)] + relations[(p2, p1)]
        if happiness > best:
            best = happiness
    return best


def part_one(filename: str) -> int:
    return optimize_seating(*read_input(filename))


def part_two(filename: str) -> int:
    people, relations = read_input(filename)
    for person in people:
        relations[("self", person)] = 0
        relations[(person, "self")] = 0
    people.add("self")

    return optimize_seating(people, relations)


if __name__ == "__main__":
    import os
    print(read_input(os.path.dirname(__file__) + "\\input.txt"))
    print(part_one(os.path.dirname(__file__) + "\\input.txt"))
    print(part_two(os.path.dirname(__file__) + "\\input.txt"))
