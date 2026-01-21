from itertools import batched


def read_input(filename: str) -> list[tuple[int, ...]]:
    return [
        tuple(map(int, lengths))
        for lengths in [line.split() for line in open(filename)]
    ]


def part_one(filename: str) -> int:
    return len([
        triangle
        for triangle in [
            tuple(sorted(triangle, reverse=True))
            for triangle in read_input(filename)
        ]
        if triangle[0] < sum(triangle[1:])
    ])


def part_two(filename: str) -> int:
    return len([
        triangle for triangle in [
            tuple(sorted(lengths, reverse=True))
            for triplet in batched(read_input(filename), 3)
            for lengths in zip(*triplet)
        ]
        if triangle[0] < sum(triangle[1:])
    ])
