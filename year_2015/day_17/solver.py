from itertools import combinations


def read_input(filename: str) -> list[int]:
    return [int(line.strip()) for line in open(filename)]


def find_combinations(containers: list[int]) -> list[tuple[int, ...]]:
    return [
        cmb
        for i in range(2, len(containers))
        for cmb in combinations(containers, i)
        if sum(cmb) == 150
    ]


def part_one(filename: str) -> int:
    return len(find_combinations(read_input(filename)))


def part_two(filename: str) -> int:
    cmbs = sorted(find_combinations(read_input(filename)), key=len)
    minimal = len(cmbs[0])
    return len([cmb for cmb in cmbs if len(cmb) == minimal])
