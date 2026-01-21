def read_input(filename: str) -> tuple[int, int]:
    line = open(filename).read().split()
    return int(line[-3][:-1]), int(line[-1][:-1])


def part_one(filename: str) -> int:
    row, col = read_input(filename)
    it = 1 + sum(range(1, row)) + sum(range(1, col)) + row * (col - 1)

    code = 20151125
    for _ in range(it - 1):
        code = (code * 252533) % 33554393

    return code


def part_two(filename: str) -> int:
    return 0
