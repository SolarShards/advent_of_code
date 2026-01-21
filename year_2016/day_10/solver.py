from math import prod


def read_input(
        filename: str
        ) -> tuple[dict[str, list[int]], dict[str, tuple[str, str]]]:
    holders: dict[str, list[int]] = {}
    instructions: dict[str, tuple[str, str]] = {}
    for inst in [line.split() for line in open(filename)]:
        if inst[0] == "value":
            if (holder := " ".join(inst[-2:])) not in holders:
                holders[holder] = []
            holders[holder].append(int(inst[1]))
        else:
            targets = (" ".join(inst[5:7]), " ".join(inst[-2:]))
            for holder in (giver := " ".join(inst[:2]), *targets):
                if holder not in holders:
                    holders[holder] = []
            instructions[giver] = targets

    return holders, instructions


def step(
        holders: dict[str, list[int]],
        instructions: dict[str, tuple[str, str]]):
    for holder, chips in holders.items():
        if len(chips) == 2 and "bot" in holder:
            low_target, high_target = instructions[holder]
            if len(holders[low_target]) < 2:
                holders[low_target].append(min(chips))
                chips.remove(min(chips))
            if len(holders[high_target]) < 2:
                holders[high_target].append(max(chips))
                chips.remove(max(chips))


def part_one(filename: str) -> int:
    holders, instructions = read_input(filename)
    while True:
        step(holders, instructions)
        for holder, chips in holders.items():
            if chips in ([17, 61], [61, 17]):
                return int(holder.split()[1])


def part_two(filename: str) -> int:
    holders, instructions = read_input(filename)
    values = [-1] * 3
    while True:
        step(holders, instructions)
        for output in range(3):
            if holders[holder := f"output {output}"]:
                values[output] = holders[holder][0]
        if -1 not in values:
            return prod(values)
