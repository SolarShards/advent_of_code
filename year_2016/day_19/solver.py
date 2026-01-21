from math import log


def read_input(filename: str) -> int:
    return int(open(filename).read().strip())


def part_one(filename: str) -> int:
    elves = bin(read_input(filename))
    return int(elves[3:] + elves[2], 2)


def part_two(filename: str) -> int:
    elves = read_input(filename)
    return elves - 3**int(log(elves, 3))
