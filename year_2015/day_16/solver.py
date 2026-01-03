def read_input(filename: str) -> tuple[dict[str, int], list[dict[str, int]]]:
    return {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1
    }, [
        {
            sp[2][:-1]: int(sp[3][:-1]),
            sp[4][:-1]: int(sp[5][:-1]),
            sp[6][:-1]: int(sp[7])
        }
        for sp in [line.split() for line in open(filename)]
    ]


def part_one(filename: str) -> int:
    target, sues = read_input(filename)
    compatibility = [
        sum(v == target[k] for k, v in sue.items())
        for sue in sues
    ]
    return compatibility.index(max(compatibility)) + 1


def part_two(filename: str) -> int:
    target, sues = read_input(filename)
    compatibility = [
        sum(
            v > target[k] if k in ("cats", "trees")
            else v < target[k] if k in ("pomeranians", "goldfish")
            else v == target[k]
            for k, v in sue.items()
        )
        for sue in sues
    ]
    return compatibility.index(max(compatibility)) + 1
