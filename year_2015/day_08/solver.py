import re


def read_input(filename: str) -> list[str]:
    return [line.strip() for line in open(filename)]


def part_one(filename: str) -> int:
    return sum(
        len(line) - len(line.encode().decode('unicode_escape')[1:-1])
        for line in read_input(filename)
    )


def part_two(filename: str):
    return sum(
        len(list(re.finditer(r"(\")|(\\)", line))) + 2
        for line in read_input(filename)
    )
