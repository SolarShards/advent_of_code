def read_input(filename: str) -> list[list[bool]]:
    return [[c == "#" for c in line.strip()] for line in open(filename)]


def count_on_neighbours(grid: list[list[bool]], row: int, col: int) -> int:
    return sum(
        sum(grid[r][max(0, col - 1):col + 2])
        for r in range(
            max(0, row - 1),
            min(len(grid[0]), row + 2)
        )
    ) - grid[row][col]


def step(grid: list[list[bool]]) -> list[list[bool]]:
    return [
        [
            count_on_neighbours(grid, row, col)
            in ((2, 3) if grid[row][col] else (3,))
            for col in range(len(grid[row]))
        ]
        for row in range(len(grid))
    ]


def part_one(filename: str) -> int:
    grid = read_input(filename)
    for _ in range(100):
        grid = step(grid)
    return sum(light for row in grid for light in row)


def part_two(filename: str) -> int:
    grid = read_input(filename)
    grid[0][0] = grid[0][-1] = grid[-1][0] = grid[-1][-1] = True
    for _ in range(100):
        grid = step(grid)
        grid[0][0] = grid[0][-1] = grid[-1][0] = grid[-1][-1] = True
    return sum(light for row in grid for light in row)
