def read_input(filename: str) -> list[list[int]]:
    data_map = {'.': 0, 'S': 1, '^': -1}
    return [
        [data_map[c] for c in line.rstrip()]
        for line in open(filename).readlines()
    ]


def run_manifold(manifold: list[list[int]]) -> tuple[int, int]:
    splits = 0
    for i, line in enumerate(manifold[1:], start=1):
        for j, obj in enumerate(line):
            if (obj) == -1:
                line[j-1] += manifold[i-1][j]
                line[j+1] += manifold[i-1][j]
                splits += 1 if manifold[i-1][j] != 0 else 0
            elif manifold[i-1][j] != -1:
                line[j] += manifold[i-1][j]
    return splits, sum(manifold[-1])


def part_one(filename: str) -> int:
    return run_manifold(read_input(filename))[0]


def part_two(filename: str) -> int:
    return run_manifold(read_input(filename))[1]
