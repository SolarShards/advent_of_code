def read_input(filename: str) -> list[list[int]]:
    return [
        list(map(int, line.strip().replace("@", "1").replace(".", "0")))
        for line in open(filename)
    ]


def find_rolls(plan: list[list[int]]) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i in range(len(plan))
        for j in range(len(plan[0]))
        if plan[i][j]
    ]


def get_square(
        plan: list[list[int]],
        row: int,
        col: int,
        distance: int = 1
        ) -> list[list[int]]:
    return [
        plan[i][max(0, col - distance):col + distance + 1]
        for i in range(
            max(0, row - distance),
            min(len(plan[0]), row + distance + 1)
        )
    ]


def count_accessible_rolls(
        plan: list[list[int]],
        rolls: list[tuple[int, int]]
        ):
    accessible_rolls = 0
    for (row, col) in rolls:
        sq = get_square(plan, row, col)
        if sum([row.count(1) for row in sq]) < 5:
            accessible_rolls += 1
    return accessible_rolls


def remove_accessible_rolls(
        plan: list[list[int]],
        rolls: list[tuple[int, int]]
        ) -> int:

    rolls_to_remove: list[tuple[int, int]] = []
    removable_rolls = 0
    it = 1

    while it != 0:

        for (row, col) in rolls:
            sq = get_square(plan, row, col)
            if sum([row.count(1) for row in sq]) < 5:
                rolls_to_remove.append((row, col))

        it = len(rolls_to_remove)
        removable_rolls += it

        for (row, col) in rolls_to_remove:
            plan[row][col] = 0
            rolls.remove((row, col))

        rolls_to_remove.clear()

    return removable_rolls


def part_one(filename: str) -> int:
    plan = read_input(filename)
    rolls = find_rolls(plan)
    return count_accessible_rolls(plan, rolls)


def part_two(filename: str) -> int:
    plan = read_input(filename)
    rolls = find_rolls(plan)
    return remove_accessible_rolls(plan, rolls)
