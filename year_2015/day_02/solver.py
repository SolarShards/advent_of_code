from math import prod


def read_input(filename: str) -> list[tuple[int, ...]]:
    return [
        tuple(map(int, line.strip().split("x"))) for line in open(filename)
    ]


def part_one(filename: str) -> int:
    return sum(
        [
            2*sum(s) + min(s)
            for s in [
                (l*w, w*h, h*l)
                for (l, w, h) in read_input(filename)
            ]
        ]
    )


def part_two(filename: str) -> int:
    return sum(
        [
            2 * (sum(dimensions) - max(dimensions)) + prod(dimensions)
            for dimensions in read_input(filename)
        ]
    )
