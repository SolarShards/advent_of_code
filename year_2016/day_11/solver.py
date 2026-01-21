import re


def read_input(filename: str) -> list[int]:
    plan = open(filename).read()
    return [
        len([m for m in re.findall(r"(\w+) g|(\w+)-", floor)])
        for floor in plan.split("\n")
    ]


def min_moves(plan: list[int]):
    return sum(
         max(2 * sum(plan[:floor+1]) - 3, 1)
         for floor in range(len(plan)-1)
    )


def part_one(filename: str) -> int:
    return min_moves(read_input(filename))


def part_two(filename: str) -> int:
    plan = read_input(filename)
    plan[0] += 4
    return min_moves(plan)
