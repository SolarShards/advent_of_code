from typing import Callable


def read_input(
        filename: str,
        action_map: dict[str, Callable]
               ) -> list[tuple[
                       tuple[int, ...],
                       tuple[int, ...],
                       Callable
                    ]]:
    return [
        (
            tuple(map(int, sp[-3].split(","))),
            tuple(map(int, sp[-1].split(","))),
            action_map[sp[0] if sp[0] in action_map else " ".join(sp[:2])]
        )
        for sp in [line.split() for line in open(filename)]
    ]


def part_one(filename: str) -> int:
    grid = [[False for _ in range(1000)] for _ in range(1000)]
    action_map = {
        "turn on": lambda g, r, c: True,
        "turn off": lambda g, r, c: False,
        "toggle": lambda g, r, c: not g[r][c]
    }
    for (ul_corner, lr_corner, action) in read_input(filename, action_map):
        for row in range(ul_corner[0], lr_corner[0] + 1):
            for col in range(ul_corner[1], lr_corner[1] + 1):
                grid[row][col] = action(grid, row, col)
    return sum(row.count(True) for row in grid)


def part_two(filename: str) -> int:
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    action_map = {
        "turn on": lambda g, r, c: g[r][c] + 1,
        "turn off": lambda g, r, c: max(g[r][c] - 1, 0),
        "toggle": lambda g, r, c: g[r][c] + 2
    }
    for (ul_corner, lr_corner, action) in read_input(filename, action_map):
        for row in range(ul_corner[0], lr_corner[0] + 1):
            for col in range(ul_corner[1], lr_corner[1] + 1):
                grid[row][col] = action(grid, row, col)
    return sum(light for row in grid for light in row)
